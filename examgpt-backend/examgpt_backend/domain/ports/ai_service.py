from abc import ABC, abstractmethod
from typing import Optional

from domain.model.core.chunk import TextChunk
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced


class AIService(ABC):
    @abstractmethod
    def create_flash_card(
        self, chunk: TextChunk, exam_code: str
    ) -> Optional[list[FlashCardEnhanced]]: ...

    @abstractmethod
    def create_multiple_choice(
        self, chunk: TextChunk, exam_code: str
    ) -> Optional[list[MultipleChoiceEnhanced]]: ...
