from domain.ai.base import BaseModelProvider
from domain.model.core.chunk import TextChunk
from pydantic import BaseModel


class CreateFlashCard(BaseModel):
    chunk: TextChunk
    exam_code: str
    exam_name: str
    model_provider: BaseModelProvider


class CreateMultipleChoice(BaseModel):
    chunk: TextChunk
    exam_code: str
    exam_name: str
    model_provider: BaseModelProvider
