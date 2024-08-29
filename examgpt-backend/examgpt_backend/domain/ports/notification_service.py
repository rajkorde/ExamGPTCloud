from abc import ABC, abstractmethod


class ChunkNotificationService(ABC):
    @abstractmethod
    def send_notification(self, chunk_ids: list[str]) -> bool: ...
