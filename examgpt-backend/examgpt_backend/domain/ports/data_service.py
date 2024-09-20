import os
from abc import ABC, abstractmethod
from typing import Optional

from domain.model.core.chunk import TextChunk
from domain.model.core.exam import Exam, ExamState
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.model.utils.work_tracker import WorkTracker


class ExamService(ABC):
    @staticmethod
    def create_exam(
        name: str, email: str, filenames: list[str], exam_code: str | None
    ) -> Exam:
        exam = (
            Exam(
                name=name,
                email=email,
                exam_code=exam_code,
            )
            if exam_code
            else Exam(name=name, email=email)
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
    def get_chunks(
        self, chunk_ids: list[str], exam_code: str
    ) -> Optional[list[TextChunk]]: ...

    @abstractmethod
    def get_chunks_by_exam_code(self, exam_code: str) -> Optional[list[TextChunk]]: ...


class QAService(ABC):
    @abstractmethod
    def save_flashcards(self, flashcards: list[FlashCardEnhanced]) -> bool: ...

    @abstractmethod
    def save_multiplechoices(
        self, multiplechoices: list[MultipleChoiceEnhanced]
    ) -> bool: ...

    @abstractmethod
    # Get n flashcards. If n is 0, return all
    def get_flashcards(
        self, exam_code: str, n: int = 0
    ) -> Optional[list[FlashCardEnhanced]]: ...

    @abstractmethod
    # Get n multiple choice questions. If n is 0, return all
    def get_multiplechoices(
        self, exam_code: str, n: int = 0
    ) -> Optional[list[MultipleChoiceEnhanced]]: ...


class WorkTrackerService(ABC):
    @abstractmethod
    def add_exam_tracker(self, exam_code: str) -> bool: ...

    @abstractmethod
    def get_exam_tracker(self, exam_code: str) -> Optional[WorkTracker]: ...

    @abstractmethod
    def reset_exam_tracker(self, exam_code: str) -> bool: ...

    @abstractmethod
    def update_total_workers(self, exam_code: str, total_workers: int) -> bool: ...

    @abstractmethod
    def increment_completed_workers(self, exam_code: str) -> bool: ...
