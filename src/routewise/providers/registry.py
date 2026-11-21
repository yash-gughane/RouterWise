from .mock import MockProvider
from .openai_compatible import OpenAICompatibleProvider


class ProviderRegistry:
    \"\"\"Maps model categories to provider adapters and exposes a fallback.\"\"\"

    def __init__(self, mode: str, settings):
        if mode == "mock":
            self.providers = {
                "fast": MockProvider("fast-mock"),
                "coding": MockProvider("coding-mock"),
                "reasoning": MockProvider("reasoning-mock"),
            }
            self.fallback_provider = MockProvider("fallback-mock")
        elif mode == "openai_compatible":
            provider = OpenAICompatibleProvider(
                settings.api_base_url, settings.api_key
            )
            self.providers = {
                "fast": provider,
                "coding": provider,
                "reasoning": provider,
            }
            self.fallback_provider = provider
        else:
            raise ValueError(
                "ROUTEWISE_PROVIDER_MODE must be 'mock' or 'openai_compatible'."
            )

    def get(self, category: str):
        try:
            return self.providers[category]
        except KeyError as exc:
            raise ValueError(f"No provider configured for category: {category}") from exc
