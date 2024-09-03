from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import tiktoken
from dataclasses_json import dataclass_json
from langchain.chat_models.base import BaseChatModel


class Scenario(Enum):
    FLASHCARD = "flash_card"
    MULTIPLECHOICE = "multiple_choice"
    ANSWER = "answer"
    CONTEXTCHECK = "context_check"


@dataclass_json
@dataclass
class Prompt:
    scenario: Scenario
    model: str
    prompt: str


class BasePromptProvider:
    prompts_file: str = "prompts.yaml"

    def get_prompt(self, scenario: Scenario, model: str) -> Optional[str]: ...


@dataclass
class BaseModelProvider(ABC):
    model_family: Enum
    model_name: Enum
    cost_ppm_token: int
    temperature: float = 0.7
    # bump the cost of by this amount to factor in input and output tokens being different price
    fuzz_factor: float = 1.3
    chunk_size: int = 2500

    def estimate_cost(self, token_count: int) -> float:
        return round(
            (token_count * self.fuzz_factor * self.cost_ppm_token) / 1_000_000, 2
        )

    def get_token_count(self, text: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model(self.model_name.value)
        num_tokens = len(encoding.encode(text))
        return num_tokens

    @abstractmethod
    def get_chat_model(self) -> BaseChatModel: ...

    def get_model_name(self) -> str:
        return self.model_name.value

    def get_model_family(self) -> str:
        return self.model_family.value
