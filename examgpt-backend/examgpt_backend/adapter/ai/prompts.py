from pathlib import Path
from typing import Optional

import yaml
from domain.ai.base import BasePromptProvider, Prompt, Scenario


class PromptProvider(BasePromptProvider):
    prompts_file: str = "prompts.yaml"

    def __init__(self):
        current_dir = Path(__file__).parent
        filename = current_dir / self.prompts_file
        with open(filename, "r") as f:
            prompts = yaml.safe_load(f)
            # adding type ignore because pylance doesnt work with dataclass_json
            self.prompts = [Prompt.from_dict(prompt) for prompt in prompts]  # type: ignore

    def get_prompt(self, scenario: Scenario, model: str) -> Optional[str]:
        for prompt in self.prompts:
            if prompt.scenario == scenario and prompt.model == model:
                return prompt.prompt  # return first hit

        return None
