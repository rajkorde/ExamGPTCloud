from dataclasses import dataclass, field
from enum import Enum

from adapter.ai.constants import ModelFamily, ModelName
from domain.ai.base import BaseModelProvider
from langchain_openai import ChatOpenAI


@dataclass
class LlamaProvider(BaseModelProvider):
    model_family: Enum = field(default=ModelFamily.OLLAMA)
    model_name: Enum = field(default=ModelName.LLAMA3)
    temperature: float = 0.7
    cost_ppm_token: int = 50
    chunk_size: int = 2500

    def __init__(self):
        self.chat = ChatOpenAI(model=str(self.model_name.value))

    def get_chat_model(self) -> ChatOpenAI:
        return self.chat
