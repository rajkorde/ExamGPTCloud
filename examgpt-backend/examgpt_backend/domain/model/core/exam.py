from enum import Enum
from typing import Optional
from uuid import uuid4

# Ignoring PylanceReportMissingTypeStubs for codenamize package
from codenamize import codenamize  # type: ignore
from domain.model.utils.misc import get_current_time
from pydantic import BaseModel, EmailStr, Field


class ExamState(Enum):
    CREATED = "created"
    SAVED = "saved"
    UPLOADED = "uploaded"
    CHUNKED = "chunked"
    READY = "ready"  # QAs have been generated


class Exam(BaseModel):
    name: str
    email: EmailStr
    sources: list[str] = Field(default_factory=list)
    exam_code: Optional[str] = Field(default_factory=lambda: codenamize(str(uuid4())))
    last_updated: str = Field(default_factory=get_current_time)
    state: ExamState = Field(default=ExamState.CREATED)
