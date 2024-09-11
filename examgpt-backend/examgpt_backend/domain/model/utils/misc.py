import datetime
import os
from dataclasses import dataclass, field
from typing import Optional

from domain.model.core.chunk import TextChunk
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.model.utils.logging import app_logger

logger = app_logger.get_logger()


class ChunksStats:
    def __init__(self, chunks: list[TextChunk]):
        total_chunks = len(chunks)
        self.total_chunks_with_context = len(
            [chunk for chunk in chunks if not chunk.is_empty_context]
        )
        self.chunks_with_flash_cards = len(
            [chunk for chunk in chunks if chunk.flash_card_generated]
        )
        self.chunks_with_multiple_choice = len(
            [chunk for chunk in chunks if chunk.multiple_choice_generated]
        )

        self.chunks_with_context_ratio = self.total_chunks_with_context / total_chunks
        self.chunks_with_flash_cards_ratio = (
            self.chunks_with_flash_cards / self.total_chunks_with_context
        )
        self.chunks_with_multiple_choice_ratio = (
            self.chunks_with_multiple_choice / self.total_chunks_with_context
        )


class FlashCardsStats:
    def __init__(self, flash_cards: list[FlashCardEnhanced]):
        self.total_flash_cards = len(flash_cards)
        self.chunk_count = len({flash_card.chunk_id for flash_card in flash_cards})


class MultipleChoicesStats:
    def __init__(self, multiple_choices: list[MultipleChoiceEnhanced]):
        self.total_multiple_choices = len(multiple_choices)
        self.chunk_count = len(
            {multiple_choice.chunk_id for multiple_choice in multiple_choices}
        )


@dataclass
class ErrorMessage:
    message: str = field(default="Something went wrong")


def get_env_var(name: str) -> Optional[str]:
    value = os.getenv(name)
    if not value:
        logger.error(f"Could not find environment variable: {name}")
        return None
    return value


def get_current_time() -> str:
    """Gets the current date and time as a string."""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return str(timestamp)
