from abc import ABC, abstractmethod
from typing import Any, Optional


class ContentService(ABC):
    @abstractmethod
    def create_upload_url(self, filename: str, expires_in: int = 3600) -> Any: ...

    @abstractmethod
    def download_file(
        self, source: str, destination: str, bucket_name: Optional[str] = None
    ) -> str: ...

    @abstractmethod
    def upload_file(
        self, source: str, destination: str, bucket_name: Optional[str] = None
    ) -> str: ...
