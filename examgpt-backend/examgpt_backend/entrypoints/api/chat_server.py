import asyncio
import json
from typing import Any

import boto3
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.model.utils.logging import app_logger
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

logger = app_logger.get_logger()
tg_bot_token_name = "/examgpt/TG_BOT_TOKEN"
ssm = boto3.client("ssm")


def get_parameter(parameter_name: str, with_decryption: bool = True):
    try:
        response = ssm.get_parameter(
            Name=parameter_name, WithDecryption=with_decryption
        )
        return str(response["Parameter"]["Value"])
    except ssm.exceptions.ParameterNotFound:
        print(f"The parameter {parameter_name} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


tg_bot_token = get_parameter(tg_bot_token_name)


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
    if not tg_bot_token:
        raise InvalidEnvironmentSetup(tg_bot_token_name)

    # Create the Application
    application = ApplicationBuilder().token(tg_bot_token).build()

    update = Update.de_json(json.loads(event["body"]), application.bot)
    print(f"{update=}")

    # Add handler for the /echo command
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("whoami", whoami))

    # Process the update

    await application.process_update(update)


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    print("Executing chat server.")

    print(f"{tg_bot_token=}")
    print("*** Received event")
    print(f"{event=}")
    print(f"{context=}")
    body = json.loads(event["body"])
    print(f"{body=}")

    return {"statusCode": 200, "body": json.dumps("Message processed successfully")}

    # try:
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(async_handler(event, context))
    #     return {"statusCode": 200, "body": json.dumps("Message processed successfully")}
    # except Exception as e:
    #     print(f"Error: {str(e)}")
    #     return {"statusCode": 500, "body": json.dumps("Error processing message")}
