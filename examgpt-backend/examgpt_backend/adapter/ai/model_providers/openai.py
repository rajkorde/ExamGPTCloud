from dataclasses import dataclass, field
from enum import Enum

from adapter.ai.constants import ModelFamily, ModelName
from domain.ai.base import BaseModelProvider
from langchain_openai import ChatOpenAI


@dataclass
class OpenAIProvider(BaseModelProvider):
    model_family: Enum = field(default=ModelFamily.OPENAI)
    model_name: Enum = field(default=ModelName.GPT4OMINI)
    temperature: float = 0.7
    cost_ppm_token: int = 50
    chunk_size: int = 2500

    def __init__(self):
        self.chat = ChatOpenAI(model=str(self.model_name.value))

    def get_chat_model(self) -> ChatOpenAI:
        return self.chat
