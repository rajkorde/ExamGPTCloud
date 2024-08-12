from typing import Optional
from uuid import uuid4

# Ignoring PylanceReportMissingTypeStubs for codenamize package
from codenamize import codenamize  # type: ignore
from domain.model.utils.misc import get_current_time
from pydantic import BaseModel, Field


class Exam(BaseModel):
    name: str
    sources: list[str] = Field(default_factory=list)
    exam_code: Optional[str] = Field(default_factory=lambda: codenamize(str(uuid4())))
    last_updated: str = Field(default_factory=get_current_time)
