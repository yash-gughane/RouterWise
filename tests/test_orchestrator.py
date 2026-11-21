from types import SimpleNamespace

from src.routewise.orchestrator import Orchestrator
from src.routewise.providers.base import ProviderResult
from src.routewise.providers.mock import FailingProvider
from src.routewise.providers.registry import ProviderRegistry
from src.routewise.router import ModelRouter
from src.routewise.telemetry import Telemetry


class SequenceProvider:
    def __init__(self, failures=0):
        self.failures = failures
        self.calls = 0

    def generate(self, prompt, model):
        self.calls += 1
        if self.calls <= self.failures:
            raise RuntimeError("temporary failure")
        return ProviderResult("test answer", model, 10, 5, 0.001)


class TestRegistry:
    def __init__(self, primary, fallback=None):
        self.primary = primary
        self.fallback_provider = fallback or SequenceProvider()

    def get(self, category):
        return self.primary


def make_router():
    return ModelRouter({
        "fast": "fast-model",
        "coding": "coding-model",
        "reasoning": "reasoning-model",
    })


def test_orchestrator_success():
    telemetry = Telemetry()
    registry = TestRegistry(SequenceProvider())
    orchestrator = Orchestrator(make_router(), registry, telemetry, 1)
    result = orchestrator.run("Explain a variable")
    assert result["status"] == "completed"
    assert result["attempts"] == 1
    assert telemetry.snapshot()["successful_requests"] == 1


def test_retry_then_success():
    telemetry = Telemetry()
    registry = TestRegistry(SequenceProvider(failures=1))
    orchestrator = Orchestrator(make_router(), registry, telemetry, 1)
    result = orchestrator.run("Explain a variable")
    assert result["status"] == "completed"
    assert result["attempts"] == 2


def test_fallback_after_retry_budget():
    telemetry = Telemetry()
    registry = TestRegistry(FailingProvider(), SequenceProvider())
    orchestrator = Orchestrator(make_router(), registry, telemetry, 0)
    result = orchestrator.run("Explain a variable")
    assert result["used_fallback"] is True
    assert result["status"] == "completed"
