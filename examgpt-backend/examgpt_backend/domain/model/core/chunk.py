from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from domain.model.utils.misc import get_current_time


class TextChunkState(Enum):
    CREATED = 1
    PROCESSED = 2


@dataclass
class TextChunk:
    exam_code: str
    text: str
    state: TextChunkState = field(default=TextChunkState.CREATED)
    chunk_id: str = field(default_factory=lambda: str(uuid4()))
    last_updated: str = field(default_factory=get_current_time)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(chunk_dict: dict[str, Any]) -> "TextChunk":
        return TextChunk(**chunk_dict)
