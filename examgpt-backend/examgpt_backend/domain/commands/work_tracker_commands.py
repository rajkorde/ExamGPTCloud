from pydantic import BaseModel


class AddExamTracker(BaseModel):
    exam_code: str


class GetExamTracker(BaseModel):
    exam_code: str


class ResetExamTracker(BaseModel):
    exam_code: str


class UpdateTotalWorkers(BaseModel):
    exam_code: str


class IncrementCompletedWorkers(BaseModel):
    exam_code: str
