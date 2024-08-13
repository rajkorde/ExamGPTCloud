from pydantic import BaseModel, Field


class CreateUploadURLs(BaseModel):
    sources: list[str] = Field(default_factory=list)
