from dataclasses import dataclass, field

from ai.base import ModelConfig, ModelProvider
from ai.constants import ModelFamily, ModelName
from langchain_openai import ChatOpenAI


@dataclass
class OpenAIConfig(ModelConfig):
    family: ModelFamily = field(default=ModelFamily.OPENAI)
    name: ModelName = field(default=ModelName.GPT4OMINI)
    cost_ppm_token: int = 50
    chunk_size: int = 2500


class OpenAIProvider(ModelProvider):
    def __init__(self, model_config: ModelConfig = OpenAIConfig()):
        self.model_config = model_config
        self.chat = ChatOpenAI(model=str(self.model_config.name.value))
        # logger.info(
        #     f"Setting model provider to {model_config.name} from {model_config.family}."
        # )

    def get_chat_model(self) -> ChatOpenAI:
        return self.chat

    def get_model_name(self) -> ModelName:
        return ModelName.DEFAULT
