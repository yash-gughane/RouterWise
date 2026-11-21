from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    provider_mode: str = os.getenv("ROUTEWISE_PROVIDER_MODE", "mock").lower()
    api_base_url: str = os.getenv("ROUTEWISE_API_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    api_key: str = os.getenv("ROUTEWISE_API_KEY", "")
    fast_model: str = os.getenv("ROUTEWISE_FAST_MODEL", "fast-mock")
    coding_model: str = os.getenv("ROUTEWISE_CODING_MODEL", "coding-mock")
    reasoning_model: str = os.getenv("ROUTEWISE_REASONING_MODEL", "reasoning-mock")
    fallback_model: str = os.getenv("ROUTEWISE_FALLBACK_MODEL", "fallback-mock")
    max_retries: int = max(0, int(os.getenv("ROUTEWISE_MAX_RETRIES", "1")))


settings = Settings()
