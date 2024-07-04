from typing import Any, Optional

class RetryQuota:
    INITIAL_CAPACITY: int = ...
    def __init__(self, initial_capacity: Any = ..., lock: Optional[Any] = ...) -> None: ...
    def acquire(self, capacity_amount: Any) -> Any: ...
    def release(self, capacity_amount: Any) -> None: ...
    @property
    def available_capacity(self) -> Any: ...
