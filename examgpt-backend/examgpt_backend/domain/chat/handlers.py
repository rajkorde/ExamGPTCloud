from __future__ import annotations

from typing import NamedTuple, Optional

from domain.chat.helper import ChatBotDataState, ChatServices
from domain.model.core.question import (
    FlashCardEnhanced,
    MultipleChoiceEnhanced,
    QuestionType,
)
from domain.model.utils.exceptions import NotEnoughQuestionsInExam
from domain.model.utils.logging import app_logger
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

logger = app_logger.get_logger()

QUIZZING = 1

start_keyboard = [["Start", "Cancel"]]
answer_keyboard_mc = [["A", "B", "C", "D"]]
answer_keyboard_fc = [["Show Answer", "Cancel"]]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)
answer_markup_mc = ReplyKeyboardMarkup(answer_keyboard_mc, one_time_keyboard=True)
answer_markup_fc = ReplyKeyboardMarkup(answer_keyboard_fc, one_time_keyboard=True)


class CommandParser(NamedTuple):
    question_count: int
    question_topic: Optional[str]

    @staticmethod
    def _parse_command(args: list[str]) -> CommandParser:
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

        return CommandParser(question_count=count, question_topic=topic)

    @staticmethod
    async def parse(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> Optional[CommandParser]:
        # Parse question count and topic here
        if context.args:
            try:
                command = CommandParser._parse_command(context.args)
            except Exception:
                reply_text = f"Incorrect format. Correct format is {update.message.text.split()[0]} [question_count] [topic]"
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=reply_text
                )
                return None
        else:
            command = CommandParser(question_count=1, question_topic=None)

        return command


async def exam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    exam_obj = await ChatServices.get_exam(update=update, context=context)
    if not exam_obj:
        return

    chat_state = ChatBotDataState(exam_code=exam_obj.exam_code)

    chat_payload = {update.effective_chat.id: chat_state.model_dump()}
    context.bot_data.update(chat_payload)

    message = f"Welcome to {exam_obj.name} practice!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def start_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""

    # Parse question count and topic here
    command = await CommandParser.parse(update, context)
    if not command:
        return ConversationHandler.END

    chat_payload = await ChatBotDataState.get_bot_data(update, context)
    if not chat_payload or not chat_payload.exam_code:
        return ConversationHandler.END

    try:
        questions = await ChatServices.get_questions(
            exam_code=chat_payload.exam_code,
            question_count=command.question_count,
            question_type=QuestionType.MULTIPLECHOICE,
            update=update,
            context=context,
        )
    except NotEnoughQuestionsInExam as e:
        error_msg = f"No enough questions in this exam. Max questions allowed: {e.max_questions}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=error_msg)
        return ConversationHandler.END

    if not questions or len(questions) == 0:
        return ConversationHandler.END
    logger.info(f"Got {len(questions)} multiple choice questions.")

    logger.info(
        "Multiple Choice Scenario.",
        f"Count: {command.question_count}, ",
        f"Topic: {command.question_topic}, ",
        f"Exam Code: {chat_payload.exam_code}, ",
        f"Total Questions: {len(questions)}",
    )

    question_count = command.question_count
    chat_payload.total_question_count = question_count
    chat_payload.asked_question_count = 0
    chat_payload.correct_answer_count = 0
    chat_payload.last_answer = "X"
    chat_payload.question_list = [question.dict() for question in questions]

    chat_payload = {update.effective_chat.id: chat_payload.model_dump()}
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

    chat_payload = await ChatBotDataState.get_bot_data(update, context)
    if not chat_payload or not chat_payload.exam_code:
        return ConversationHandler.END

    chat_id = update.effective_chat.id
    user_answer = update.effective_message.text

    assert chat_payload.question_list is not None
    assert chat_payload.total_question_count is not None
    assert chat_payload.asked_question_count is not None
    assert chat_payload.correct_answer_count is not None
    assert chat_payload.last_answer is not None

    if not chat_payload.last_answer == "X":
        if user_answer == chat_payload.last_answer:
            await update.message.reply_text("Correct! ✅")
            chat_payload.correct_answer_count += 1
            context.bot_data.update({chat_id: chat_payload.model_dump()})
        else:
            await update.message.reply_text(
                f"Incorrect! The correct answer is {chat_payload.last_answer}"
            )

    if chat_payload.asked_question_count >= chat_payload.total_question_count:
        return await completed_mc(update, context)

    question_dict = chat_payload.question_list[chat_payload.asked_question_count]
    question_obj = MultipleChoiceEnhanced(**question_dict)
    question = question_obj.question
    choices = "\n".join([f"{k}: {v}" for k, v in question_obj.choices.items()])

    await update.message.reply_text(
        f"{question}\n{choices}",
        reply_markup=answer_markup_mc,
    )

    chat_payload.asked_question_count += 1
    chat_payload.last_answer = question_obj.answer

    context.bot_data.update({chat_id: chat_payload.model_dump()})

    return QUIZZING


async def completed_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id

    chat_payload = await ChatBotDataState.get_bot_data(update, context)
    if not chat_payload or not chat_payload.exam_code:
        return ConversationHandler.END
    assert chat_payload.question_list is not None
    assert chat_payload.total_question_count is not None
    assert chat_payload.asked_question_count is not None
    assert chat_payload.correct_answer_count is not None
    assert chat_payload.last_answer is not None

    correct = chat_payload.correct_answer_count
    total = chat_payload.total_question_count

    chat_payload.reset()
    context.bot_data.update({chat_id: chat_payload.model_dump()})

    reply_text = f"You got {correct} out of {total} right!"

    await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def start_fc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""

    # Parse question count and topic here
    command = await CommandParser.parse(update, context)
    if not command:
        return ConversationHandler.END

    chat_payload = await ChatBotDataState.get_bot_data(update, context)
    if not chat_payload or not chat_payload.exam_code:
        return ConversationHandler.END

    try:
        questions = await ChatServices.get_questions(
            exam_code=chat_payload.exam_code,
            question_count=command.question_count,
            question_type=QuestionType.FLASHCARD,
            update=update,
            context=context,
        )
    except NotEnoughQuestionsInExam as e:
        error_msg = f"No enough questions in this exam. Max questions allowed: {e.max_questions}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=error_msg)
        return ConversationHandler.END

    if not questions or len(questions) == 0:
        return ConversationHandler.END
    logger.info(f"Got {len(questions)} flash card questions.")

    logger.info(
        "Flash Card Scenario.",
        f"Count: {command.question_count}, ",
        f"Topic: {command.question_topic}, ",
        f"Exam Code: {chat_payload.exam_code}, ",
        f"Total Questions: {len(questions)}",
    )

    question_count = command.question_count
    chat_payload.total_question_count = question_count
    chat_payload.asked_question_count = 0
    chat_payload.last_answer = "X"
    chat_payload.question_list = [question.dict() for question in questions]

    chat_payload = {update.effective_chat.id: chat_payload.model_dump()}
    context.bot_data.update(chat_payload)

    question_str = "question" if question_count == 1 else "questions"
    reply_text = f"Ready for {question_count} flash card {question_str}?\n/cancel anytime to cancel quiz."
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


async def quiz_fc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""

    chat_payload = await ChatBotDataState.get_bot_data(update, context)
    if not chat_payload or not chat_payload.exam_code:
        return ConversationHandler.END

    chat_id = update.effective_chat.id

    assert chat_payload.question_list is not None
    assert chat_payload.total_question_count is not None
    assert chat_payload.asked_question_count is not None
    assert chat_payload.last_answer is not None

    if not chat_payload.last_answer == "X":
        await update.message.reply_text(f"{chat_payload.last_answer}\n-----")
    if chat_payload.asked_question_count >= chat_payload.total_question_count:
        return await completed_fc(update, context)

    question_dict = chat_payload.question_list[chat_payload.asked_question_count]
    question_obj = FlashCardEnhanced(**question_dict)
    question = question_obj.question

    await update.message.reply_text(
        f"{question}",
        reply_markup=answer_markup_fc,
    )

    chat_payload.asked_question_count += 1
    chat_payload.last_answer = question_obj.answer

    context.bot_data.update({chat_id: chat_payload.model_dump()})

    return QUIZZING


async def completed_fc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id

    chat_payload = await ChatBotDataState.get_bot_data(update, context)
    if not chat_payload or not chat_payload.exam_code:
        return ConversationHandler.END
    assert chat_payload.total_question_count is not None
    reply_text = f"You practiced on {chat_payload.total_question_count} flash cards!"
    chat_payload.reset()
    context.bot_data.update({chat_id: chat_payload.model_dump()})

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
/fc [n] [topic]. Start a flash card quiz of n questions (default 1) on an optional topic.
/mc [n] [topic]. Start a multiple choice quiz of n questions (default 1) on an optional topic.
You can also ask general questions for the exam to refresh your memory.
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text)
