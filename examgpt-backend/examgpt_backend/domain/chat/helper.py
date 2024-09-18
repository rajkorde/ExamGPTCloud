from __future__ import annotations

from typing import Any, Optional

from domain.command_handlers.exam_commands_handler import get_exam
from domain.command_handlers.questions_commands_handler import (
    get_multiplechoices,
)
from domain.commands.exam_commands import GetExam
from domain.commands.questions_commands import GetMultipleChoices
from domain.model.core.exam import Exam
from domain.model.core.question import MultipleChoiceEnhanced
from domain.model.utils.logging import app_logger
from domain.ports.data_service import ExamService, QAService
from pydantic import BaseModel, Field
from telegram import Update
from telegram.ext import ContextTypes

logger = app_logger.get_logger()


class ChatBotDataState(BaseModel):
    exam_code: Optional[str] = Field(default=None)
    question_list: Optional[list[dict[str, Any]]] = Field(default=None)
    total_question_count: Optional[int] = Field(default=None)
    asked_question_count: Optional[int] = Field(default=None)
    correct_answer_count: Optional[int] = Field(default=None)
    last_answer: Optional[str] = Field(default=None)

    def reset(self):
        self.question_list = None
        self.asked_question_count = None
        self.correct_answer_count = None
        self.total_question_count = None
        self.last_answer = None

    @classmethod
    async def get_bot_data(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> Optional[ChatBotDataState]:
        chat_payload = ChatBotDataState(**context.bot_data[update.effective_chat.id])

        if not chat_payload:
            error_msg = "Something went wrong. Please try again later."
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=error_msg
            )
            return None

        if not chat_payload.exam_code:
            error_msg = "No exam code provided. Did you run /exam command?"
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=error_msg
            )
            return None

        return chat_payload


class ChatServices:
    exam_service: Optional[ExamService] = None
    qa_service: Optional[QAService] = None

    @classmethod
    def initialize(
        cls,
        exam_service: ExamService,
        qa_service: QAService,
    ):
        cls.exam_service = exam_service
        cls.qa_service = qa_service

    @classmethod
    async def get_exam(
        cls,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> Optional[Exam]:
        if not context.args or len(context.args) == 0:
            error_msg = """
No exam code provided.
/exam exam_code: Initialize an exam for a given code
"""
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=error_msg
            )
            return None

        exam_code = context.args[0]
        exam_service = ChatServices.exam_service
        if not exam_service:
            logger.error("Chat service not initialized")
            error_msg = "Something went wrong. Please try again later."
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=error_msg
            )
            return None

        exam_obj = get_exam(
            command=GetExam(exam_code=exam_code), exam_service=exam_service
        )

        if not exam_obj:
            logger.warning("User provided incorrect exam code.")
            error_msg = f"No exam found for this exam code. Please provide a valid exam code: {exam_code}"
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=error_msg
            )
            return None

        return exam_obj

    @classmethod
    async def get_multiplechoices(
        cls,
        exam_code: str,
        question_count: int,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> Optional[list[MultipleChoiceEnhanced]]:
        qa_service = ChatServices.qa_service
        if not qa_service:
            logger.error("Chat service not initialized")
            error_msg = "Something went wrong. Please try again later."
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=error_msg
            )
            return None

        questions = get_multiplechoices(
            command=GetMultipleChoices(exam_code=exam_code, n=question_count),
            data_service=qa_service,
        )

        if not questions or len(questions) == 0:
            error_msg = f"No questions found for this exam: {exam_code}"
            logger.error(error_msg)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=error_msg
            )
            return None

        if len(questions) != question_count:
            error_msg = "Something went wrong. Please try again later."
            logger.error(error_msg)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=error_msg
            )
            return None

        return questions
