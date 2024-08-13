from domain.model.core.exam import Exam
from pydantic import BaseModel


class SaveExam(BaseModel):
    exam: Exam
