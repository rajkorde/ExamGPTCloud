from domain.model.core.chunk import TextChunk
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.model.utils.logging import app_logger

logger = app_logger.get_logger()


class ChunksStats:
    def __init__(self, chunks: list[TextChunk], exam_code: str):
        self.exam_code = exam_code
        self.total_chunks = len(chunks)
        self.total_chunks_with_context = len(
            [chunk for chunk in chunks if not chunk.is_empty_context]
        )
        self.chunks_with_flash_cards = len(
            [chunk for chunk in chunks if chunk.flash_card_generated]
        )
        self.chunks_with_multiple_choice = len(
            [chunk for chunk in chunks if chunk.multiple_choice_generated]
        )

        self.chunks_with_context_ratio = (
            self.total_chunks_with_context / self.total_chunks
        )
        self.chunks_with_flash_cards_ratio = (
            self.chunks_with_flash_cards / self.total_chunks_with_context
        )
        self.chunks_with_multiple_choice_ratio = (
            self.chunks_with_multiple_choice / self.total_chunks_with_context
        )

    def log_stats(self):
        logger.info(
            f"\nChunk stats for exam code: {self.exam_code}\n"
            f"Total chunks: {self.total_chunks}\n"
            f"Total chunks without context: {self.total_chunks-self.total_chunks_with_context}\n"
            f"Chunks with flash cards: {self.chunks_with_flash_cards}\n"
            f"Chunks with multiple choice: {self.chunks_with_multiple_choice}\n"
            f"Chunks with context ratio: {self.chunks_with_context_ratio}\n"
            f"Chunks with flash cards ratio: {self.chunks_with_flash_cards_ratio}\n"
            f"Chunks with multiple choice ratio: {self.chunks_with_multiple_choice_ratio}\n"
        )


class FlashCardsStats:
    def __init__(self, flash_cards: list[FlashCardEnhanced], exam_code: str):
        self.exam_code = exam_code
        self.total_flash_cards = len(flash_cards)
        self.chunk_count = len({flash_card.chunk_id for flash_card in flash_cards})

    def log_stats(self):
        logger.info(
            f"\nFlash card stats for exam code: {self.exam_code}\n"
            f"Total flash cards: {self.total_flash_cards}\n"
            f"Processed chunk count for flash cards: {self.chunk_count}\n"
        )


class MultipleChoicesStats:
    def __init__(self, multiple_choices: list[MultipleChoiceEnhanced], exam_code: str):
        self.exam_code = exam_code
        self.total_multiple_choices = len(multiple_choices)
        self.chunk_count = len(
            {multiple_choice.chunk_id for multiple_choice in multiple_choices}
        )

    def log_stats(self):
        logger.info(
            f"\nMultiple choice stats for exam code: {self.exam_code}\n"
            f"\nTotal multiple choices: {self.total_multiple_choices}\n"
            f"Processed chunk count for multiple choices: {self.chunk_count}\n"
        )
