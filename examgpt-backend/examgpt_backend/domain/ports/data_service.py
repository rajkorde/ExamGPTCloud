import os
from abc import ABC, abstractmethod
from typing import Optional

from domain.model.core.chunk import TextChunk
from domain.model.core.exam import Exam, ExamState


class ExamService(ABC):
    @staticmethod
    def create_exam(name: str, filenames: list[str], exam_code: str | None) -> Exam:
        exam = (
            Exam(
                name=name,
                exam_code=exam_code,
            )
            if exam_code
            else Exam(name=name)
        )

        for filename in filenames:
            filename = f"{exam.exam_code}/sources/{os.path.basename(filename)}"
            exam.sources.append(filename)

        return exam

    @abstractmethod
    def put_exam(self, exam: Exam, overwrite: bool = False) -> bool: ...

    @abstractmethod
    def get_exam(self, exam_code: str) -> Optional[Exam]: ...

    @abstractmethod
    def update_state(self, exam_code: str, newstate: ExamState) -> bool: ...


class ChunkService(ABC):
    @abstractmethod
    def save_chunks(self, chunks: list[TextChunk]) -> bool: ...

    @abstractmethod
    def get_chunks(self, chunk_ids: list[str]) -> Optional[list[TextChunk]]: ...
