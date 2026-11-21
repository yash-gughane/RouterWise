from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProviderResult:
    text: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, model: str) -> ProviderResult:
        \"\"\"Generate a response for prompt using model.\"\"\"
        raise NotImplementedError
