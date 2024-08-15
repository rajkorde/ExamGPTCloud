from uuid import uuid4

from pydantic import BaseModel, Field


class CreateUploadURLs(BaseModel):
    sources: list[str] = Field(default_factory=list)


class DownloadFile(BaseModel):
    source: str
    destination: str = Field(default_factory=lambda: str(f"/tmp/temp_{uuid4()}.pdf"))
