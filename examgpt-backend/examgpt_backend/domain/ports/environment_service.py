from abc import ABC, abstractmethod
from typing import Optional


class EnvironmentService(ABC):
    @abstractmethod
    def get_parameter(self, name: str, is_encrypted: bool = False) -> Optional[str]: ...
