from fastapi import FastAPI, HTTPException

from .config import settings
from .orchestrator import Orchestrator, OrchestrationError
from .providers.registry import ProviderRegistry
from .router import ModelRouter
from .schemas import (
    RouteRequest, OrchestrateRequest, RoutingResponse, OrchestrationResponse
)
from .telemetry import Telemetry

models = {
    "fast": settings.fast_model,
    "coding": settings.coding_model,
    "reasoning": settings.reasoning_model,
}

router = ModelRouter(models)
providers = ProviderRegistry(settings.provider_mode, settings)
telemetry = Telemetry()
orchestrator = Orchestrator(
    router, providers, telemetry, settings.max_retries
)

app = FastAPI(
    title="RouteWise API",
    description="Model routing and task orchestration MVP.",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "provider_mode": settings.provider_mode}


@app.post("/route", response_model=RoutingResponse)
def route(request: RouteRequest):
    decision = router.classify(request.prompt)
    return {
        "category": decision.category,
        "model": decision.model,
        "complexity": decision.complexity,
        "reason": decision.reason,
    }


@app.post("/orchestrate", response_model=OrchestrationResponse)
def orchestrate(request: OrchestrateRequest):
    try:
        result = orchestrator.run(request.prompt, request.max_retries)
        return {
            key: result[key]
            for key in (
                "task_id", "status", "category", "model", "attempts",
                "result", "latency_ms", "estimated_cost_usd", "used_fallback"
            )
        }
    except OrchestrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/metrics")
def metrics():
    return telemetry.snapshot()
