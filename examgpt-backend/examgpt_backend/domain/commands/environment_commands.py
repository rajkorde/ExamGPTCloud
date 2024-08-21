from pydantic import BaseModel, Field


class GetParameter(BaseModel):
    name: str
    is_encrypted: bool = Field(default=False)
