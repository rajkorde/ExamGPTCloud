from uuid import uuid4

# Ignoring PylanceReportMissingTypeStubs for codenamize package
from codenamize import codenamize  # type: ignore
from pydantic import BaseModel, Field
from utils.misc import get_current_time


class Exam(BaseModel):
    name: str
    exam_id: str = Field(default_factory=lambda: codenamize(str(uuid4())))
    sources: list[str] = Field(default_factory=list)
    last_updated: str = Field(default_factory=get_current_time)
