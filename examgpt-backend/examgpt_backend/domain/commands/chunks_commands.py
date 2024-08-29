from domain.model.core.chunk import TextChunk
from pydantic import BaseModel


class SaveChunks(BaseModel):
    chunks: list[TextChunk]


class NotifyChunks(BaseModel):
    chunk_ids: list[str]
