from enum import Enum


class Scenario(Enum):
    FLASHCARD = "flash_card"
    MULTIPLECHOICE = "multiple_choice"
    ANSWER = "answer"
    CONTEXTCHECK = "context_check"


class ModelFamily(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"
    GOOGLE = "google"
    DEFAULT = "default"


class ModelName(Enum):
    GPT3_5_TURBO = "gpt-3.5-turbo-0125"
    GPT4O = "gpt-4o"
    GPT4OMINI = "gpt-4o-mini"
    GEMINIPRO1_5 = "geminipro-1.5"
    GEMINI_FLASH = "gemini-1.5-flash"
    LLAMA2 = "llama2"
    LLAMA3 = "llama3"
    DEFAULT = "default"
