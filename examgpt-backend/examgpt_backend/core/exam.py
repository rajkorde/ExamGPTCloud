from dataclasses import dataclass, field
from uuid import uuid4

# Ignoring PylanceReportMissingTypeStubs for codenamize package
from codenamize import codenamize  # type: ignore
from examgpt_backend.utils.misc import get_current_time


@dataclass
class Exam:
    name: str
    exam_id: str = field(default_factory=lambda: codenamize(str(uuid4())))
    sources: list[str] = field(default_factory=list)
    last_updated: str = field(default_factory=get_current_time)
    post_event: bool = False
