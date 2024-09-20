from __future__ import annotations

import asyncio
import json
import traceback
from typing import Any

from domain.chat.handlers import (
    QUIZZING,
    cancel,
    exam,
    quiz_fc,
    quiz_mc,
    start,
    start_fc,
    start_mc,
)
from domain.chat.helper import ChatServices
from domain.command_handlers.content_commands_handler import download_file, upload_file
from domain.command_handlers.environments_commands_handler import get_parameter
from domain.commands.content_commands import DownloadFile, UploadFile
from domain.commands.environment_commands import GetParameter
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import get_env_var
from entrypoints.helpers.utils import CommandRegistry, get_error, get_success
from telegram import TelegramObject, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

logger = app_logger.get_logger()
tg_bot_token_name = "/examgpt/TG_BOT_TOKEN"
BUCKET_NAME_ENV_VAR = "BUCKET_NAME"


async def async_handler(event: dict[Any, Any], context: Any):
    env_service = CommandRegistry().get_environment_service()
    content_service = CommandRegistry().get_content_service()
    bucket_name = get_env_var(BUCKET_NAME_ENV_VAR)

    if not bucket_name:
        logger.error(
            "No bucket name provided in function call or in environment variable."
        )
        return get_error()

    tg_bot_token = get_parameter(
        GetParameter(name=tg_bot_token_name, is_encrypted=True), env_service
    )

    obj = TelegramObject.de_json(json.loads(event["body"])).to_dict()
    user_id = str(obj["message"]["from"]["id"])

    pickle_file_path = "/tmp/chat.pkl"
    pickle_object_key = f"chat/{user_id}/chat.pkl"

    download_file(
        DownloadFile(
            source=pickle_object_key,
            destination=pickle_file_path,
            bucket_name=bucket_name,
        ),
        content_service,
    )

    application = (
        ApplicationBuilder()
        .token(tg_bot_token)
        .persistence(persistence=PicklePersistence(pickle_file_path))
        .build()
    )

    update = Update.de_json(json.loads(event["body"]), application.bot)

    mc_handler = ConversationHandler(
        entry_points=[CommandHandler("mc", start_mc)],
        states={
            QUIZZING: [
                MessageHandler(filters.Regex("^(Cancel)$"), cancel),
                MessageHandler(
                    filters.Regex("^(Start|A|B|C|D)$") & ~filters.COMMAND,
                    quiz_mc,
                ),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        persistent=True,
        name="mc_conversation",
    )

    fc_handler = ConversationHandler(
        entry_points=[CommandHandler("fc", start_fc)],
        states={
            QUIZZING: [
                MessageHandler(filters.Regex("^(Cancel)$"), cancel),
                MessageHandler(
                    filters.Regex("^(Start|Show Answer)$") & ~filters.COMMAND,
                    quiz_fc,
                ),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        persistent=True,
        name="fc_conversation",
    )

    application.add_handler(mc_handler)
    application.add_handler(fc_handler)
    application.add_handler(CommandHandler("exam", exam))
    application.add_handler(CommandHandler(["start", "help"], start))

    # Process the update
    async with application:
        await application.process_update(update)
        await application.update_persistence()
        upload_file(
            UploadFile(
                source=pickle_file_path,
                destination=pickle_object_key,
                bucket_name=bucket_name,
            ),
            content_service,
        )


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    command_registry = CommandRegistry()
    exam_service = command_registry.get_exam_service()
    qa_service = command_registry.get_qa_service()
    ChatServices.initialize(exam_service, qa_service)

    logger.info("Starting chat server.")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(async_handler(event, context))
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        return get_error()
    return get_success("Message processed successfully")
