from typing import Protocol

from domain.model.core.chunk import TextChunk


class Chunker(Protocol):
    def chunk(self, location: str, exam_code: str) -> list[TextChunk]: ...
