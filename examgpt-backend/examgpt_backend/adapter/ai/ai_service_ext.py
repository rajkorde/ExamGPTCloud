from typing import Optional

from adapter.ai.prompts import PromptProvider
from domain.ai.aimodel import AIModel
from domain.ai.base import BaseModelProvider
from domain.model.core.chunk import TextChunk
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.model.utils.logging import app_logger
from domain.ports.ai_service import AIService

logger = app_logger.get_logger()


class AIServiceExt(AIService):
    def create_flash_card(
        self,
        chunk: TextChunk,
        exam_code: str,
        exam_name: str,
        model_provider: BaseModelProvider,
    ) -> Optional[list[FlashCardEnhanced]]:
        prompt_provider = PromptProvider()
        model = AIModel(
            model_provider=model_provider,
            prompt_provider=prompt_provider,
        )

        flashcards = model.generate_flashcard_qa(chunk, exam_name)
        if not flashcards:
            return None

        return [
            FlashCardEnhanced(
                **flashcard.dict(),
                chunk_id=chunk.chunk_id,
                exam_code=exam_code,
                model_family=model_provider.model_family.value,
                model_name=model_provider.model_name.value,
            )
            for flashcard in flashcards
        ]

    def create_multiple_choice(
        self,
        chunk: TextChunk,
        exam_code: str,
        exam_name: str,
        model_provider: BaseModelProvider,
    ) -> Optional[list[MultipleChoiceEnhanced]]:
        prompt_provider = PromptProvider()
        model = AIModel(
            model_provider=model_provider,
            prompt_provider=prompt_provider,
        )

        multiplechoices = model.generate_multiplechoice_qa(chunk, exam_name)
        if not multiplechoices:
            return None
        return [
            MultipleChoiceEnhanced(
                **multiplechoice.dict(),
                chunk_id=chunk.chunk_id,
                exam_code=exam_code,
                model_family=model_provider.model_family.value,
                model_name=model_provider.model_name.value,
            )
            for multiplechoice in multiplechoices
        ]
