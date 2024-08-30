from domain.model.core.chunk import TextChunk
from pydantic import BaseModel


class CreateFlashCard(BaseModel):
    chunk: TextChunk
    exam_code: str


class CreateMultipleChoice(BaseModel):
    chunk: TextChunk
    exam_code: str
