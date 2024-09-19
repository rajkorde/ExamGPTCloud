import json
from typing import Any

from domain.chunker.pdf_chunker import SimplePDFChunker
from domain.command_handlers.chunks_commands_handler import notify_chunks, save_chunks
from domain.command_handlers.content_commands_handler import download_file
from domain.command_handlers.exam_commands_handler import update_exam_state
from domain.commands.chunks_commands import NotifyChunks, SaveChunks
from domain.commands.content_commands import DownloadFile
from domain.commands.exam_commands import UpdateExamState
from domain.model.core.exam import ExamState
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry, get_error
from entrypoints.models.api_model import ChunkerRequest

logger = app_logger.get_logger()
CHUNK_BATCH_SIZE = 10


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger.debug("Starting Chunking.")
    command_registry = CommandRegistry()
    content_service = command_registry.get_content_service()
    # exam_service = command_registry.get_exam_service()

    # Download File
    logger.debug("Downloading file.")
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
    logger.debug("Chunking file.")
    chunker = SimplePDFChunker()
    chunks = chunker.chunk(location=downloaded_file, exam_code=exam_code)
    logger.debug(f"Chunks size: {len(chunks)}")

    # Save chunks in batch
    logger.debug("Saving chunks.")
    chunk_service = command_registry.get_chunk_service()
    response = save_chunks(SaveChunks(chunks=chunks), chunk_service)
    if not response:
        logger.error("Error: Could not save chunks")
        return get_error()

    # Publish chunk topic in batches
    logger.debug("Notifying next service.")
    chunk_notification_service = command_registry.get_chunk_notification_service()

    for i in range(0, len(chunks), CHUNK_BATCH_SIZE):
        notify_chunks(
            NotifyChunks(
                chunk_ids=[c.chunk_id for c in chunks[i : i + CHUNK_BATCH_SIZE]],
                exam_code=exam_code,
            ),
            chunk_notification_service,
        )

    # test code
    # notify_chunks(
    #     NotifyChunks(
    #         chunk_ids=[c.chunk_id for c in chunks[0:CHUNK_BATCH_SIZE]],
    #         exam_code=exam_code,
    #     ),
    #     chunk_notification_service,
    # )

    # Update Exam state
    logger.debug("Updating exam state.")
    exam_service = command_registry.get_exam_service()
    response = update_exam_state(
        UpdateExamState(exam_code=exam_code, state=ExamState.CHUNKED), exam_service
    )
    if not response:
        logger.error(
            f"Error: Could not update state of the exam to f{ExamState.CHUNKED}"
        )
        return get_error()

    logger.debug("Chunking complete.")
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "File chunked successfully.",
            }
        ),
    }
