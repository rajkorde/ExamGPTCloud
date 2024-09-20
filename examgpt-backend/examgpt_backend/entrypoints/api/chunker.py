from typing import Any

from domain.chunker.pdf_chunker import SimplePDFChunker
from domain.command_handlers.chunks_commands_handler import notify_chunks, save_chunks
from domain.command_handlers.content_commands_handler import download_file
from domain.command_handlers.exam_commands_handler import update_exam_state
from domain.command_handlers.work_tracker_command_handler import (
    add_exam_tracker,
    update_total_workers,
)
from domain.commands.chunks_commands import NotifyChunks, SaveChunks
from domain.commands.content_commands import DownloadFile
from domain.commands.exam_commands import UpdateExamState
from domain.commands.work_tracker_commands import AddExamTracker, UpdateTotalWorkers
from domain.model.core.exam import ExamState
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry, get_error, get_success
from entrypoints.models.api_model import ChunkerRequest

logger = app_logger.get_logger()
CHUNK_BATCH_SIZE = 10


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger.info("Starting Chunking.")
    command_registry = CommandRegistry()
    content_service = command_registry.get_content_service()
    work_tracker_service = command_registry.get_work_tracker_service()

    # Download File
    logger.info("Downloading file.")
    chunker_request = ChunkerRequest.parse_event(event)
    if not chunker_request:
        logger.error("Error: Could not parse event")
        return get_error()
    exam_code = chunker_request.exam_code

    downloaded_file = download_file(
        command=DownloadFile(
            source=chunker_request.location, bucket_name=chunker_request.bucket_name
        ),
        content_service=content_service,
    )

    # Chunk file
    logger.info("Chunking file.")
    chunker = SimplePDFChunker()
    chunks = chunker.chunk(location=downloaded_file, exam_code=exam_code)
    logger.info(f"Chunks size: {len(chunks)}")

    # Save chunks in batch
    logger.info("Saving chunks.")
    chunk_service = command_registry.get_chunk_service()
    response = save_chunks(SaveChunks(chunks=chunks), chunk_service)
    if not response:
        logger.error("Error: Could not save chunks")
        return get_error()

    # Publish chunk topic in batches
    logger.info("Notifying next service.")
    chunk_notification_service = command_registry.get_chunk_notification_service()

    # Create work tracker for exam
    logger.info("Creating work tracker for exam.")
    result = add_exam_tracker(AddExamTracker(exam_code=exam_code), work_tracker_service)
    if not result:
        logger.error(f"Error: Could not create work tracker for exam: {exam_code}")
        return get_error()
    total_workers_needed = (len(chunks) // CHUNK_BATCH_SIZE) + 1
    logger.info(f"Total workers needed: {total_workers_needed}")
    result = update_total_workers(
        UpdateTotalWorkers(exam_code=exam_code, total_workers=total_workers_needed),
        work_tracker_service,
    )
    if not result:
        logger.error(f"Error: Could not update total workers for exam: {exam_code}")
        return get_error()

    for i in range(0, len(chunks), CHUNK_BATCH_SIZE):
        last_chunk = (len(chunks) - i) <= CHUNK_BATCH_SIZE

        notify_chunks(
            NotifyChunks(
                chunk_ids=[c.chunk_id for c in chunks[i : i + CHUNK_BATCH_SIZE]],
                exam_code=exam_code,
                last_chunk=last_chunk,
            ),
            chunk_notification_service,
        )

    # test code
    # notify_chunks(
    #     NotifyChunks(
    #         chunk_ids=[c.chunk_id for c in chunks[0:CHUNK_BATCH_SIZE]],
    #         exam_code=exam_code,
    #         last_chunk=True,
    #     ),
    #     chunk_notification_service,
    # )

    # Update Exam state
    logger.info("Updating exam state.")
    exam_service = command_registry.get_exam_service()
    response = update_exam_state(
        UpdateExamState(exam_code=exam_code, state=ExamState.CHUNKED), exam_service
    )
    if not response:
        logger.error(
            f"Error: Could not update state of the exam to f{ExamState.CHUNKED}"
        )
        return get_error()

    logger.info("Chunking complete.")
    return get_success("File chunked successfully.")
