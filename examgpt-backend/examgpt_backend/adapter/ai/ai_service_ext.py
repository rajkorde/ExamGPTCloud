from typing import Optional

from domain.model.core.chunk import TextChunk
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.ports.ai_service import AIService


class AIServiceExt(AIService):
    def create_flash_card(
        self, chunk: TextChunk, exam_code: str
    ) -> Optional[list[FlashCardEnhanced]]: ...

    def create_multiple_choice(
        self, chunk: TextChunk, exam_code: str
    ) -> Optional[list[MultipleChoiceEnhanced]]: ...
