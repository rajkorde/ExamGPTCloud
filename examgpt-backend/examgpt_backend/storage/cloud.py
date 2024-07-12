from abc import ABC, abstractmethod
from typing import Any

import boto3
from examgpt_backend.core.exam import Exam
from examgpt_backend.sources.filetypes.base import Source


class Storage(ABC):
    @abstractmethod
    def copy(self, sources: list[Source]) -> None: ...

    @abstractmethod
    def save_to_json(self, data: dict[Any, Any], filename: str) -> None: ...

    @abstractmethod
    def get_exam(self, location: str) -> Exam: ...
