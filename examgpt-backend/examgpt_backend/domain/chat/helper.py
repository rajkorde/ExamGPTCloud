from typing import Optional

from domain.ports.data_service import QAService
from pydantic import BaseModel, Field


class ChatBotDataState(BaseModel):
    exam_code: Optional[str] = Field(default=None)
    question_list: Optional[list[str]] = Field(default=None)
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


class ChatServices:
    qa_service: Optional[QAService] = None

    @classmethod
    def initialize(cls, qa_service: QAService):
        cls.qa_service = qa_service


class ChatHelper:
    def __init__(self, state: ChatBotDataState):
        self.state = state
