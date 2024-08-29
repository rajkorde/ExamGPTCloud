from domain.ports.notification_service import ChunkNotificationService


class ChunkNotificationServiceSNS(ChunkNotificationService):
    def send_notification(self, chunk_ids: list[str]) -> bool: ...
