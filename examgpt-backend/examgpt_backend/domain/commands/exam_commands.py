from domain.model.core.exam import Exam, ExamState
from pydantic import BaseModel, EmailStr


class SaveExam(BaseModel):
    exam: Exam


class UpdateExamState(BaseModel):
    exam_code: str
    state: ExamState


class GetExam(BaseModel):
    exam_code: str


class NotifyValidateExam(BaseModel):
    exam_code: str


class EmailUserExamReady(BaseModel):
    exam_code: str
    email: EmailStr
    bot_link: str
