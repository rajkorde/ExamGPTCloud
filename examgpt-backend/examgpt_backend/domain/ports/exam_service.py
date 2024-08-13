from abc import ABC, abstractmethod
from typing import Any

from domain.model.core.exam import Exam


class ExamService(ABC):
    @abstractmethod
    def put_exam(self, exam: Exam) -> Any: ...

    @abstractmethod
    def get_exam(self, exam_code: str) -> Any: ...
