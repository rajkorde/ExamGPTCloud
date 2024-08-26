from __future__ import annotations

import asyncio
import json
import os
import traceback
from typing import Any, NamedTuple, Optional

import boto3
from botocore.exceptions import ClientError
from domain.command_handlers.environments_commands_handler import get_parameter
from domain.commands.environment_commands import GetParameter
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry
from pydantic import BaseModel, Field
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, TelegramObject, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

logger = app_logger.get_logger()
tg_bot_token_name = "/examgpt/TG_BOT_TOKEN"
s3 = boto3.client("s3")
bucket_name = os.environ["CHAT_BUCKET"]

QUIZZING = 1

start_keyboard = [["Start", "Cancel"]]
answer_keyboard_mc = [["A", "B", "C", "D"]]
answer_keyboard_lf = [["Show Answer", "Cancel"]]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)
answer_markup_mc = ReplyKeyboardMarkup(answer_keyboard_mc, one_time_keyboard=True)
answer_markup_lf = ReplyKeyboardMarkup(answer_keyboard_lf, one_time_keyboard=True)


class MultipleChoice(BaseModel):
    question: str = Field(description="An exam question with a multiple choice answers")
    answer: str = Field(
        description="""
            Answer key to a multiple choice question.
            Possible values are A, B, C, D"""
    )
    choices: dict[str, str] = Field(
        description="""
            A dict of key and value for 4 choices for an exam question, out of which one is corrrect. 
            The possible key values are A, B, C, D and value contains the possible answer""",
    )

    def __str__(self) -> str:
        return "\n".join(
            [
                f"Question: {self.question}",
                "Choices:",
                *[f"{key}: {value}" for key, value in self.choices.items()],
                f"Answer: {self.answer}",
            ]
        )


the_question = MultipleChoice(
    question="Who is the highest run-getter in ODI?",
    answer="B",
    choices={
        "A": "Virat Kohli",
        "B": "Sachin Tendulkar",
        "C": "Ricky Ponting",
        "D": "Agit Agarkar",
    },
)


class CommandArgs(NamedTuple):
    question_count: int
    question_topic: Optional[str]


def command_parser(args: list[str]) -> CommandArgs:
    def is_int(s: str) -> bool:
        return s.strip().lstrip("-+").isdigit()

    count = 1
    topic = None

    if is_int(args[0]):
        count = int(args[0])
        if count < 0 or count > 25:
            raise ValueError("Invalid command format")
        if len(args) > 1:
            topic = " ".join(args[1:])
    else:
        topic = " ".join(args)

    return CommandArgs(question_count=count, question_topic=topic)


async def start_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""

    # Parse question count and topic here
    if context.args:
        try:
            command = command_parser(context.args)
        except Exception:
            reply_text = (
                "Incorrect format. Correct format is /mc [question_count] [topic]"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=reply_text
            )
            return ConversationHandler.END
    else:
        command = CommandArgs(question_count=1, question_topic=None)

    logger.info(
        f"Multiple Choice Scenario. Count: {command.question_count}, Topic:{command.question_topic}"
    )

    # if command.question_count > chat.get_question_count_mc():
    MAX_QUESTIONS = 5
    if command.question_count > MAX_QUESTIONS:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Max allowed questions are {MAX_QUESTIONS}",
        )
        return ConversationHandler.END

    question_count = command.question_count
    chat_id = update.effective_chat.id

    chat_payload = {
        chat_id: {
            "total_question_count": question_count,
            "asked_question_count": 0,
            "correct_answer_count": 0,
            "question_list": [],
            "last_answer": "X",
        }
    }

    context.bot_data.update(chat_payload)

    question_str = "question" if question_count == 1 else "questions"
    reply_text = f"Ready for {question_count} multiple choice {question_str}?\n/cancel anytime to cancel quiz."
    if command.question_topic:
        reply_text = f"{reply_text}\nAsking questions on topics is not supported yet: {command.question_topic}"

    if not update.message:
        logger.warning("Update does not have a message object")
        return await cancel(update, context)

    await update.message.reply_text(
        reply_text,
        reply_markup=start_markup,
    )

    return QUIZZING


async def quiz_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""

    chat_id = update.effective_chat.id

    try:
        chat_payload = context.bot_data[chat_id]
    except Exception:
        logger.error("Couldn't not find payload in bot data for {chat_id}")
        return await error(update, context)

    last_answer = chat_payload["last_answer"]
    user_answer = update.effective_message.text

    if not last_answer == "X":
        if user_answer == last_answer:
            await update.message.reply_text("Correct! ✅")
            chat_payload["correct_answer_count"] += 1
            context.bot_data.update({chat_id: chat_payload})
        else:
            await update.message.reply_text(
                f"Incorrect! The correct answer is {last_answer}"
            )

    if chat_payload["asked_question_count"] >= chat_payload["total_question_count"]:
        return await completed_mc(update, context)

    while True:
        multiple_choice_qa = the_question
        if not multiple_choice_qa:
            logger.error("No multiple choice questions found.")
            return await error(update, context)
        # if multiple_choice_qa.chunk_id not in question_list:
        #     break
        break

    question = multiple_choice_qa.question
    choices = "\n".join([f"{k}: {v}" for k, v in multiple_choice_qa.choices.items()])

    await update.message.reply_text(
        f"{question}\n{choices}",
        reply_markup=answer_markup_mc,
    )

    chat_payload["asked_question_count"] += 1
    chat_payload["last_answer"] = multiple_choice_qa.answer
    # chat_payload["question_list"].append(multiple_choice_qa.chunk_id)

    context.bot_data.update({chat_id: chat_payload})

    return QUIZZING


async def completed_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id

    try:
        chat_payload = context.bot_data[chat_id]
    except Exception:
        logger.error("Couldn't not find payload in bot data for {chat_id}")
        return await error(update, context)

    correct = chat_payload["correct_answer_count"]
    total = chat_payload["total_question_count"]
    reply_text = f"You got {correct} out of {total} right!"

    await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = "Quiz Cancelled."
    await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = "Something went wrong. Please try again."
    await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = """
Welcome to ExamGPT!
/exam exam_code: Initialize an exam for a given code
/mc [n] [topic]. Start a multiple choice quiz of n questions (default 1) on an optional topic.
/fc [n] [topic]. Start a flash card quiz of n questions (default 1) on an optional topic.
You can also ask general questions for the exam to refresh your memory.
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text)


async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_text = """
Rajesh Korde
https://www.linkedin.com/in/rkorde/
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


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
    logger.info("Starting chat server.")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(async_handler(event, context))
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        return {"statusCode": 500, "body": json.dumps("Something went wrong")}
    return {"statusCode": 200, "body": json.dumps("Message processed successfully")}
