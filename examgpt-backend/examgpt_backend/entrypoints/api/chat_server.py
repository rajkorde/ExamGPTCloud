import asyncio
import json
from typing import Any

from domain.command_handlers.environments_commands_handler import get_parameter
from domain.commands.environment_commands import GetParameter
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

logger = app_logger.get_logger()
tg_bot_token_name = "/examgpt/TG_BOT_TOKEN"


async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_text = """
Rajesh Korde
https://www.linkedin.com/in/rkorde/
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    echo_text = update.message  # Remove '/echo ' from the beginning
    if not echo_text:
        await update.message.reply_text(
            "Please provide some text to echo. For example: /echo Hello, World!"
        )
    else:
        await update.message.reply_text(f"You said: {echo_text}")


async def async_handler(event: dict[Any, Any], context: Any):
    env_service = CommandRegistry().get_environment_service()
    tg_bot_token = get_parameter(
        GetParameter(name=tg_bot_token_name, is_encrypted=True), env_service
    )

    application = ApplicationBuilder().token(tg_bot_token).build()
    update = Update.de_json(json.loads(event["body"]), application.bot)
    # print(f"{update=}")

    # Add handler for the /echo command
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("whoami", whoami))

    # Process the update
    await application.initialize()
    await application.process_update(update)
    await application.shutdown()


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    print("Starting chat server.")
    # print("*** Received event")
    # print(f"{event=}")
    # print(f"{context=}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_handler(event, context))
    return {"statusCode": 200, "body": json.dumps("Message processed successfully")}
