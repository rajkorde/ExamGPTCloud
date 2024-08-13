from abc import ABC, abstractmethod
from typing import Optional

from domain.model.core.exam import Exam


class ExamService(ABC):
    @abstractmethod
    def put_exam(self, exam: Exam) -> bool: ...

    @abstractmethod
    def get_exam(self, exam_code: str) -> Optional[Exam]: ...
