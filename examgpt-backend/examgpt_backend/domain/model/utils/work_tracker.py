from __future__ import annotations

from pydantic import BaseModel, Field


class WorkTracker(BaseModel):
    exam_code: str
    total_workers: int = Field(default=0)
    completed_workers: int = Field(default=0)
