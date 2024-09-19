from abc import ABC, abstractmethod


class ChunkNotificationService(ABC):
    @abstractmethod
    def send_notification(self, chunk_ids: list[str], exam_code: str) -> bool: ...


class ValidationNotificationService(ABC):
    @abstractmethod
    def send_notification(self, exam_code: str) -> bool:
        return True
