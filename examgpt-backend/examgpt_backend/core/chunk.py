from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4

from utils.misc import get_current_time


@dataclass
class TextChunk:
    exam_id: str
    text: str
    page_number: int | None
    chunk_id: str = field(default_factory=lambda: str(uuid4()))
    last_updated: str = field(default_factory=get_current_time)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(chunk_dict: dict[str, Any]) -> "TextChunk":
        return TextChunk(**chunk_dict)
