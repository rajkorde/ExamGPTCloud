from abc import ABC, abstractmethod
from typing import Any


class ContentService(ABC):
    @abstractmethod
    def create_upload_url(self, filename: str, expires_in: int = 3600) -> Any: ...

    @abstractmethod
    def download_file(self, source: str, destination: str) -> Any: ...
