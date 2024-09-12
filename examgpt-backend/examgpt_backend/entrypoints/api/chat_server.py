from __future__ import annotations

import asyncio
import json
import os
import traceback
from typing import Any

import boto3
from botocore.exceptions import ClientError
from domain.chat.handlers import (
    QUIZZING,
    cancel,
    quiz_mc,
    start,
    start_mc,
    whoami,
)
from domain.chat.helper import ChatServices
from domain.command_handlers.environments_commands_handler import get_parameter
from domain.commands.environment_commands import GetParameter
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry
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
s3 = boto3.client("s3")
bucket_name = os.environ["CHAT_BUCKET"]


def log_pkl_filesize(message: str, filename: str):
    if os.path.exists(filename):
        logger.debug(f"{message}: {os.path.getsize(filename)}")
    else:
        logger.debug(f"{message}: File doesnt exist yet")


def upload_file(source: str, destination: str, bucket_name: str):
    if not os.path.exists(source):
        return
    try:
        s3.upload_file(source, bucket_name, destination)
    except ClientError as e:
        logger.error(e)
        raise e
    return destination


def download_file(source: str, destination: str, bucket_name: str) -> bool:
    try:
        s3.download_file(bucket_name, source, destination)
    except ClientError as e:
        if (
            "Error" in e.response
            and "Code" in e.response["Error"]
            and e.response["Error"]["Code"] == "404"
        ):
            logger.debug("Chat File does not exist remotely.")
        else:
            logger.error(e)
            raise e
    return os.path.exists(destination)


async def async_handler(event: dict[Any, Any], context: Any):
    env_service = CommandRegistry().get_environment_service()
    tg_bot_token = get_parameter(
        GetParameter(name=tg_bot_token_name, is_encrypted=True), env_service
    )

    obj = TelegramObject.de_json(json.loads(event["body"])).to_dict()
    user_id = str(obj["message"]["from"]["id"])

    pickle_file_path = "/tmp/chat.pkl"
    pickle_object_key = f"chat/{user_id}/chat.pkl"
    download_file(
        source=pickle_object_key, destination=pickle_file_path, bucket_name=bucket_name
    )

    application = (
        ApplicationBuilder()
        .token(tg_bot_token)
        .persistence(persistence=PicklePersistence(pickle_file_path))
        .build()
    )

    update = Update.de_json(json.loads(event["body"]), application.bot)
    try:
        logger.debug(f"User command: {update.message.text}")
    except Exception as e:
        logger.debug("Could not parse update.")
        logger.debug(e)

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

    application.add_handler(mc_handler)
    # TODO: Remove whoami
    application.add_handler(CommandHandler("whoami", whoami))
    application.add_handler(CommandHandler(["start", "help"], start))

    # Process the update
    async with application:
        await application.process_update(update)
        await application.update_persistence()
        upload_file(
            source=pickle_file_path,
            destination=pickle_object_key,
            bucket_name=bucket_name,
        )


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    command_registry = CommandRegistry()
    exam_service = command_registry.get_exam_service()
    qa_service = command_registry.get_qa_service()
    content_service = command_registry.get_content_service()
    ChatServices.initialize(exam_service, qa_service, content_service)

    logger.info("Starting chat server.")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(async_handler(event, context))
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        return {"statusCode": 500, "body": json.dumps("Something went wrong")}
    return {"statusCode": 200, "body": json.dumps("Message processed successfully")}
