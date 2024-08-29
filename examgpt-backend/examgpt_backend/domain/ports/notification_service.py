from abc import ABC, abstractmethod
from typing import Optional


class ChunkNotificationService(ABC):
    @abstractmethod
    def send_notification(self, chunk_ids: list[str]) -> Optional[str]: ...
