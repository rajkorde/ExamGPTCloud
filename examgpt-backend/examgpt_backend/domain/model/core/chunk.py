from uuid import uuid4

from domain.model.utils.misc import get_current_time
from pydantic import BaseModel, Field


class TextChunk(BaseModel):
    exam_code: str
    text: str
    flash_card_generated: bool = Field(default=False)
    multiple_choice_generated: bool = Field(default=False)
    is_empty_context: bool = Field(default=False)
    chunk_id: str = Field(default_factory=lambda: str(uuid4()))
    last_updated: str = Field(default_factory=get_current_time)
