from domain.model.core.chunk import TextChunk
from pydantic import BaseModel


class SaveChunks(BaseModel):
    chunks: list[TextChunk]


class GetChunks(BaseModel):
    chunk_ids: list[str]
    exam_code: str


class NotifyChunks(BaseModel):
    chunk_ids: list[str]
    exam_code: str
