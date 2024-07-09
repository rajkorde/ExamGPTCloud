from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class Scenario(Enum):
    LONGFORM = "long_form"
    MULTIPLECHOICE = "multiple_choice"
    ANSWER = "answer"
    CONTEXTCHECK = "context_check"


class AnswerOption(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class LongForm(BaseModel):
    question: str = Field(description="An exam question with a longform answer")
    answer: str = Field(description="A longform answer to an exam question")

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


class LongformEnhanced(LongForm):
    chunk_id: str
    last_updated: str


class MultipleChoiceEnhanced(MultipleChoice):
    chunk_id: str
    last_updated: str


@dataclass
class QACollection:
    exam_id: str
    exam_name: str
    source_id: str
    long_form_qa: Optional[list[LongformEnhanced]] = field(default_factory=list)
    multiple_choice_qa: Optional[list[MultipleChoiceEnhanced]] = field(
        default_factory=list
    )

    def to_dict(self) -> dict[str, Any]:
        qa_collection_dict = asdict(self)
        if self.long_form_qa:
            qa_collection_dict["long_form_qa"] = [qa.dict() for qa in self.long_form_qa]
        if self.multiple_choice_qa:
            qa_collection_dict["multiple_choice_qa"] = [
                qa.dict() for qa in self.multiple_choice_qa
            ]
        return qa_collection_dict

    @staticmethod
    def from_dict(qa_collection_dict: dict[str, Any]) -> "QACollection":
        return QACollection(
            exam_id=qa_collection_dict["exam_id"],
            exam_name=qa_collection_dict["exam_name"],
            source_id=qa_collection_dict["source_id"],
            long_form_qa=[
                LongformEnhanced(**qa) for qa in qa_collection_dict["long_form_qa"]
            ],
            multiple_choice_qa=[
                MultipleChoiceEnhanced(**qa)
                for qa in qa_collection_dict["multiple_choice_qa"]
            ],
        )

    def __str__(self) -> str:
        return "\n".join(
            [
                f"Exam_id: {self.exam_id}",
                f"Exam_name: {self.exam_name}",
                f"Source_id: {self.source_id}",
                "Long Form QA:\n--------------",
                "\n".join([str(qa) for qa in self.long_form_qa])
                if self.long_form_qa
                else "",
                "Multiple Choice QA:\n------------------",
                "\n".join([str(qa) for qa in self.multiple_choice_qa])
                if self.multiple_choice_qa
                else "",
            ]
        )
