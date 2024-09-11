from typing import Any

from domain.command_handlers.chunks_commands_handler import get_chunks_by_exam_code
from domain.command_handlers.exam_commands_handler import get_exam
from domain.command_handlers.questions_commands_handler import (
    get_flashcards,
    get_multiplechoices,
)
from domain.commands.chunks_commands import GetChunksByExamCode
from domain.commands.exam_commands import GetExam
from domain.commands.questions_commands import GetFlashCards, GetMultipleChoices
from domain.model.core.exam import ExamState
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import ChunksStats
from entrypoints.helpers.utils import CommandRegistry, get_error, get_success
from entrypoints.models.api_model import ValidateRequest

logger = app_logger.get_logger()

# if more than CHUNK_PROCESSED_RATIO of chunks are processed, the exam is ready
CHUNK_PROCESSED_RATIO = 0.8


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    logger.info("Executing validator.")
    logger.info(f"{event=}")

    command_registry = CommandRegistry()
    exam_service = command_registry.get_exam_service()
    chunk_service = command_registry.get_chunk_service()
    qa_service = command_registry.get_qa_service()

    exam_event = ValidateRequest.parse_event(event)
    if not exam_event:
        logger.error("Error: Could not parse event")
        return get_error()

    exam_code = exam_event.exam_code

    # Get exam and validate state is at least chunked and not ready
    exam = get_exam(GetExam(exam_code=exam_code), exam_service)
    if not exam:
        logger.error("Error: Exam not found")
        return get_error()

    if exam.state == ExamState.READY:
        logger.info("Exam is in READY state already.")
        return get_success()

    if exam.state != ExamState.CHUNKED:
        logger.error("Error: Exam is not chunked")
        return get_error(
            f"Exam should be in chunked state before validate is invoked. Current state: {exam.state.value}"
        )

    # Get chunks
    chunks = get_chunks_by_exam_code(
        GetChunksByExamCode(exam_code=exam_code), chunk_service
    )
    if not chunks or len(chunks) == 0:
        logger.error("Error: Chunks not found")
        return get_error()

    # Validate state of chunks
    chunk_stats = ChunksStats(chunks)
    logger.info(
        f"\nTotal chunks: {len(chunks)}\n"
        f"Total chunks without context: {len(chunks)-chunk_stats.total_chunks_with_context}\n"
        f"Chunks with flash cards: {chunk_stats.chunks_with_flash_cards}\n"
        f"Chunks with multiple choice: {chunk_stats.chunks_with_multiple_choice}\n"
        f"Chunks with context ratio: {chunk_stats.chunks_with_context_ratio}\n"
        f"Chunks with flash cards ratio: {chunk_stats.chunks_with_flash_cards_ratio}\n"
        f"Chunks with multiple choice ratio: {chunk_stats.chunks_with_multiple_choice_ratio}\n"
    )

    # Get QA
    flash_cards = get_flashcards(GetFlashCards(exam_code=exam_code), qa_service)
    multiple_choices = get_multiplechoices(
        GetMultipleChoices(exam_code=exam_code), qa_service
    )

    # print stats of chunks and QA
    if not flash_cards:
        logger.error("Error: No Flashcards found")
        return get_error("No Flashcards found")

    if not multiple_choices:
        logger.error("Error: Multiple choices not found")
        return get_error("No Multiple choices found")

    # Set exam state to Ready
    processed_chunk_ratio = 0.3
    if processed_chunk_ratio >= CHUNK_PROCESSED_RATIO:
        exam_service.update_state(exam_code=exam_code, newstate=ExamState.READY)

    # notify user that exam is ready

    return get_success()
