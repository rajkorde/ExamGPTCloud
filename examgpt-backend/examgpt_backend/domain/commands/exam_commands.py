from domain.model.core.exam import Exam, ExamState
from pydantic import BaseModel


class SaveExam(BaseModel):
    exam: Exam


class UpdateExamState(BaseModel):
    exam_code: str
    state: ExamState


class GetExam(BaseModel):
    exam_code: str
