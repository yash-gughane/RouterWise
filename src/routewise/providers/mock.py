from .base import ModelProvider, ProviderResult


class MockProvider(ModelProvider):
    \"\"\"Deterministic provider used for local development and tests.\"\"\"

    def __init__(self, name: str = "mock"):
        self.name = name

    def generate(self, prompt: str, model: str) -> ProviderResult:
        answer = (
            f"[{self.name}:{model}] Simulated response. "
            f"Received request: {prompt[:500]}"
        )
        # Mock token counts/costs are illustrative, not billing data.
        input_tokens = max(1, len(prompt.split()))
        output_tokens = max(1, len(answer.split()))
        return ProviderResult(
            text=answer,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost_usd=0.0,
        )


class FailingProvider(ModelProvider):
    \"\"\"Test utility that always fails.\"\"\"

    def generate(self, prompt: str, model: str) -> ProviderResult:
        raise RuntimeError("Simulated provider failure")
