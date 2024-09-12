from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class CreateUploadURLs(BaseModel):
    sources: list[str] = Field(default_factory=list)


class DownloadFile(BaseModel):
    source: str
    destination: str = Field(default_factory=lambda: str(f"/tmp/{uuid4()}.pdf"))
    bucket_name: Optional[str] = Field(default=None)


class UploadFile(BaseModel):
    source: str
    destination: str
    bucket_name: Optional[str] = Field(default=None)
