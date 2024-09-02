from enum import Enum
from uuid import uuid4

from codenamize import codenamize  # type: ignore
from domain.model.utils.misc import get_current_time
from langchain_core.pydantic_v1 import BaseModel, Field


class AnswerOption(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class FlashCard(BaseModel):
    question: str = Field(description="An exam question on a flash card question ")
    answer: str = Field(description="Answer to the flash card question")

    def __str__(self) -> str:
        return f"Question: {self.question}\nAnswer: {self.answer}"


class MultipleChoice(BaseModel):
    question: str = Field(description="An exam question with a multiple choice answers")
    answer: str = Field(
        description="""
            Answer key to a multiple choice question.
            Possible values are A, B, C, D"""
    )
    choices: dict[str, str] = Field(
        description="""
            A dict of key and value for 4 choices for an exam question, out of which one is corrrect. 
            The possible key values are A, B, C, D and value contains the possible answer""",
    )

    def __str__(self) -> str:
        return "\n".join(
            [
                f"Question: {self.question}",
                "Choices:",
                *[f"{key}: {value}" for key, value in self.choices.items()],
                f"Answer: {self.answer}",
            ]
        )


class FlashCardEnhanced(FlashCard):
    chunk_id: str
    exam_code: str
    qa_id: str = Field(default_factory=lambda: codenamize(str(uuid4())))
    last_updated: str = Field(default_factory=get_current_time)


class MultipleChoiceEnhanced(MultipleChoice):
    chunk_id: str
    exam_code: str
    qa_id: str = Field(default_factory=lambda: codenamize(str(uuid4())))
    last_updated: str = Field(default_factory=get_current_time)
