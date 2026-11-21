import httpx
from .base import ModelProvider, ProviderResult


class OpenAICompatibleProvider(ModelProvider):
    \"\"\"Adapter for APIs exposing the OpenAI chat-completions request shape.\"\"\"

    def __init__(self, base_url: str, api_key: str, timeout: float = 45.0):
        if not api_key:
            raise ValueError("ROUTEWISE_API_KEY is required for API provider mode.")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def generate(self, prompt: str, model: str) -> ProviderResult:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            response = httpx.post(
                url, headers=headers, json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage") or {}
            return ProviderResult(
                text=content,
                model=data.get("model", model),
                input_tokens=int(usage.get("prompt_tokens", 0)),
                output_tokens=int(usage.get("completion_tokens", 0)),
                # Provider pricing differs; zero until a pricing table is configured.
                estimated_cost_usd=0.0,
            )
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
            raise RuntimeError(f"Provider request failed: {exc}") from exc
