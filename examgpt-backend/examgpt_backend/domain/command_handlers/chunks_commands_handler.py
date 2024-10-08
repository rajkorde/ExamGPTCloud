from typing import Optional

from domain.commands.chunks_commands import (
    GetChunks,
    GetChunksByExamCode,
    NotifyChunks,
    SaveChunks,
)
from domain.model.core.chunk import TextChunk
from domain.ports.data_service import ChunkService
from domain.ports.notification_service import ChunkNotificationService


def save_chunks(command: SaveChunks, chunk_service: ChunkService) -> bool:
    return chunk_service.save_chunks(command.chunks)


def get_chunks(
    command: GetChunks, chunk_service: ChunkService
) -> Optional[list[TextChunk]]:
    return chunk_service.get_chunks(command.chunk_ids, command.exam_code)


def get_chunks_by_exam_code(
    command: GetChunksByExamCode, chunk_service: ChunkService
) -> Optional[list[TextChunk]]:
    return chunk_service.get_chunks_by_exam_code(command.exam_code)


def notify_chunks(
    command: NotifyChunks, chunk_notification_service: ChunkNotificationService
) -> bool:
    return chunk_notification_service.send_notification(
        command.chunk_ids, command.exam_code, command.last_chunk
    )
