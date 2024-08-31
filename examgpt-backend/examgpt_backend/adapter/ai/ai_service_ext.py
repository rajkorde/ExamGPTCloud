from enum import Enum
from typing import Optional

from domain.model.core.chunk import TextChunk
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.ports.ai_service import AIService
from adapters.prompt_provider import PromptProvider
from from adapter.ai.constants import Scenario


class AIServiceExt(AIService):
    def _context_check(self, chunk: str, exam_name: str) -> bool:
        scenario, model = Scenario.CONTEXTCHECK, self.model_name
        prompt = self._prompt_provider.get_prompt(scenario=scenario, model=model)
        if prompt is None:
            raise PromptNotFound(
                f"Prompt not found. Scenario: {scenario}, model: {model}"
            )

        prompt = PromptTemplate(
            template=prompt,
            input_variables=["exam_name", "context"],
        )
        prompt_and_model = (
            prompt | self.chat | BooleanOutputParser(true_val="True", false_val="False")
        )
        output = prompt_and_model.invoke({"exam_name": exam_name, "context": chunk})

        return output

    def create_flash_card(
        self, chunk: TextChunk, exam_code: str
    ) -> Optional[list[FlashCardEnhanced]]: ...

    def create_multiple_choice(
        self, chunk: TextChunk, exam_code: str
    ) -> Optional[list[MultipleChoiceEnhanced]]: ...
