from enum import Enum
from uuid import uuid4

from domain.model.utils.misc import get_current_time
from pydantic import BaseModel, Field


class TextChunkState(Enum):
    CREATED = "created"
    PROCESSED = "processed"


class TextChunk(BaseModel):
    exam_code: str
    text: str
    state: TextChunkState = Field(default=TextChunkState.CREATED)
    chunk_id: str = Field(default_factory=lambda: str(uuid4()))
    last_updated: str = Field(default_factory=get_current_time)
