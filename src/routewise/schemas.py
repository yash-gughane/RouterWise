from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)


class OrchestrateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    max_retries: int | None = Field(default=None, ge=0, le=5)


class RoutingResponse(BaseModel):
    category: str
    model: str
    complexity: float
    reason: str


class OrchestrationResponse(BaseModel):
    task_id: str
    status: str
    category: str
    model: str
    attempts: int
    result: str
    latency_ms: float
    estimated_cost_usd: float
    used_fallback: bool
