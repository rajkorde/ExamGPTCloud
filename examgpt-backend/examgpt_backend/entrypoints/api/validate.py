import time
from enum import Enum
from typing import Any

from domain.command_handlers.chunks_commands_handler import get_chunks_by_exam_code
from domain.command_handlers.exam_commands_handler import (
    email_user_exam_ready,
    get_exam,
    update_exam_state,
)
from domain.command_handlers.questions_commands_handler import (
    get_flashcards,
    get_multiplechoices,
)
from domain.command_handlers.work_tracker_command_handler import (
    get_exam_tracker,
    reset_exam_tracker,
)
from domain.commands.chunks_commands import GetChunksByExamCode
from domain.commands.exam_commands import EmailUserExamReady, GetExam, UpdateExamState
from domain.commands.questions_commands import GetFlashCards, GetMultipleChoices
from domain.commands.work_tracker_commands import GetExamTracker, ResetExamTracker
from domain.model.core.exam import ExamState
from domain.model.utils.logging import app_logger
from domain.model.utils.stats import ChunksStats, FlashCardsStats, MultipleChoicesStats
from domain.ports.data_service import WorkTrackerService
from entrypoints.helpers.utils import CommandRegistry, get_error, get_success
from entrypoints.models.api_model import ValidateRequest

logger = app_logger.get_logger()


class CompletionReason(Enum):
    COMPLETED = "completed"
    TIMEOUT = "timeout"


def poll_for_completion(
    exam_code: str,
    work_tracker_service: WorkTrackerService,
    timeout: int = 800,
    poll_interval: int = 60,
) -> CompletionReason:
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            return CompletionReason.TIMEOUT

        tracker = get_exam_tracker(
            GetExamTracker(exam_code=exam_code), work_tracker_service
        )
        logger.debug(f"Completed workers: {tracker.completed_workers}")
        if (tracker.completed_workers + 1) >= tracker.total_workers:
            return CompletionReason.COMPLETED
        else:
            sleep_duration = min(poll_interval, timeout - elapsed_time)
            time.sleep(sleep_duration)


# if more than CHUNK_PROCESSED_RATIO of chunks are processed, the exam is ready
CHUNK_PROCESSED_RATIO = 0.8
# Telegram bot link
BOT_LINK = "t.me/RSKPythonExamGPTBot"


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    logger.info("Executing validator.")
    logger.debug(f"{event=}")

    command_registry = CommandRegistry()
    exam_service = command_registry.get_exam_service()
    chunk_service = command_registry.get_chunk_service()
    qa_service = command_registry.get_qa_service()
    email_service = command_registry.get_email_service()
    work_tracker_service = command_registry.get_work_tracker_service()

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
        logger.error(
            f"Exam should be in chunked state before validate is invoked. Current state: {exam.state.value}"
        )
        return get_error()

    # Validate state of chunks if all workers have completed their work
    completion_reason = poll_for_completion(exam_code, work_tracker_service)
    if completion_reason == CompletionReason.TIMEOUT:
        logger.error("Error: Timeout while waiting for workers to complete work")
        return get_error()

    assert completion_reason == CompletionReason.COMPLETED

    # Get chunks
    chunks = get_chunks_by_exam_code(
        GetChunksByExamCode(exam_code=exam_code), chunk_service
    )
    if not chunks or len(chunks) == 0:
        logger.error(f"Error: Chunks not found for exam code: {exam_code}")
        return get_error()

    # Get QA
    flash_cards = get_flashcards(GetFlashCards(exam_code=exam_code), qa_service)
    multiple_choices = get_multiplechoices(
        GetMultipleChoices(exam_code=exam_code), qa_service
    )
    if not flash_cards:
        logger.error("Error: No Flashcards found")
        return get_error("No Flashcards found")

    if not multiple_choices:
        logger.error("Error: Multiple choices not found")
        return get_error("No Multiple choices found")

    # Log stats of chunks and QA
    chunk_stats = ChunksStats(chunks, exam_code)
    chunk_stats.log_stats()
    FlashCardsStats(flash_cards, exam_code).log_stats()
    MultipleChoicesStats(multiple_choices, exam_code).log_stats()

    # Update exam state and send email to user
    processed_flashcard_ratio = chunk_stats.chunks_with_flash_cards_ratio
    processed_multiple_choice_ratio = chunk_stats.chunks_with_flash_cards_ratio

    if (
        processed_flashcard_ratio >= CHUNK_PROCESSED_RATIO
        and processed_multiple_choice_ratio >= CHUNK_PROCESSED_RATIO
    ):
        update_exam_state(
            UpdateExamState(exam_code=exam_code, state=ExamState.READY), exam_service
        )

        response = email_user_exam_ready(
            command=EmailUserExamReady(
                exam_code=exam_code, email=exam.email, bot_link=BOT_LINK
            ),
            email_service=email_service,
        )
        if not response:
            logger.error(f"Could not send email for exam: {exam_code}")
            return get_error()

        result = reset_exam_tracker(
            ResetExamTracker(exam_code=exam_code), work_tracker_service
        )
        if not result:
            logger.warning("Error: Could not reset work tracker")

    else:
        logger.error(f"Could not generate enough QAs: {exam_code}")
        return get_error()

    return get_success()
