# RouteWise

**A modular model-routing and task-orchestration MVP.**

RouteWise classifies incoming requests, selects a model category, executes tasks through interchangeable providers, retries transient failures, falls back to another provider, and records basic cost/latency telemetry.

The default configuration uses deterministic mock providers, so the project runs locally without API keys. An optional OpenAI-compatible chat-completions adapter is included for providers exposing that API shape.

## Architecture

```text
Client
  |
  v
FastAPI (`src/routewise/api.py`)
  |
  v
Orchestrator (`orchestrator.py`)
  |-- ModelRouter (`router.py`)
  |      |-- capability + complexity heuristics
  |      `-- RoutingDecision
  |
  |-- Task / DependencyExecutor (`tasks.py`)
  |      |-- task state
  |      `-- dependency readiness
  |
  |-- ProviderRegistry (`providers/registry.py`)
  |      |-- primary provider
  |      |-- fallback provider
  |      `-- provider adapters
  |
  `-- Telemetry (`telemetry.py`)
         |-- latency
         |-- estimated cost
         `-- execution counters
```

## Features

- Capability-based routing: `fast`, `coding`, and `reasoning`.
- Complexity estimation using transparent heuristics.
- Structured task representation and dependency validation.
- Retry handling with configurable attempts.
- Provider fallback after primary-provider failure.
- Mock providers for deterministic local development.
- Optional OpenAI-compatible HTTP provider.
- FastAPI endpoints for health, routing, orchestration, and metrics.
- Unit tests and a small routing evaluation dataset.

## Quick start

### 1. Create and activate a virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run tests

```bash
pytest -q
```

### 4. Start the API

```bash
uvicorn src.routewise.api:app --reload
```

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API examples

### Health

```bash
curl http://127.0.0.1:8000/health
```

### Inspect a routing decision

```bash
curl -X POST http://127.0.0.1:8000/route \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain gradient descent intuitively"}'
```

### Run an orchestration request

```bash
curl -X POST http://127.0.0.1:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write a Python function that calculates factorial"}'
```

### Metrics

```bash
curl http://127.0.0.1:8000/metrics
```

## Optional real provider

Copy `.env.example` to `.env` and configure:

```env
ROUTEWISE_PROVIDER_MODE=openai_compatible
ROUTEWISE_API_BASE_URL=https://api.openai.com/v1
ROUTEWISE_API_KEY=your_api_key
ROUTEWISE_FAST_MODEL=gpt-4o-mini
ROUTEWISE_CODING_MODEL=gpt-4o
ROUTEWISE_REASONING_MODEL=o3
ROUTEWISE_FALLBACK_MODEL=gpt-4o-mini
```

Model names and endpoint compatibility depend on your provider and account. Use models actually available to your API account. Never commit `.env`.

For an OpenAI-compatible endpoint, RouteWise sends requests to `/chat/completions`. Some providers may require small adapter changes.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `ROUTEWISE_PROVIDER_MODE` | `mock` | `mock` or `openai_compatible` |
| `ROUTEWISE_API_BASE_URL` | `https://api.openai.com/v1` | API base URL |
| `ROUTEWISE_API_KEY` | empty | Provider credential |
| `ROUTEWISE_FAST_MODEL` | `fast-mock` | Fast model identifier |
| `ROUTEWISE_CODING_MODEL` | `coding-mock` | Coding model identifier |
| `ROUTEWISE_REASONING_MODEL` | `reasoning-mock` | Reasoning model identifier |
| `ROUTEWISE_FALLBACK_MODEL` | `fallback-mock` | Fallback model identifier |
| `ROUTEWISE_MAX_RETRIES` | `1` | Retries after the first attempt |

## Project structure

```text
RouteWise/
├── src/
│   └── routewise/
│       ├── __init__.py
│       ├── api.py
│       ├── config.py
│       ├── orchestrator.py
│       ├── router.py
│       ├── schemas.py
│       ├── tasks.py
│       ├── telemetry.py
│       └── providers/
│           ├── __init__.py
│           ├── base.py
│           ├── mock.py
│           ├── openai_compatible.py
│           └── registry.py
├── tests/
│   ├── test_api.py
│   ├── test_orchestrator.py
│   ├── test_router.py
│   └── test_tasks.py
├── evaluation/
│   └── routing_cases.json
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Design notes

- `Task` owns task state; the runner/orchestrator owns execution policy.
- `ModelRouter` selects a capability category; it does not call a model.
- Provider adapters hide provider-specific HTTP details behind a common interface.
- `ProviderRegistry` maps categories to providers and supplies a fallback.
- The mock provider makes tests repeatable and avoids API costs.
- The current classifier is heuristic, not an ML classifier or LLM-based judge.
- The MVP orchestrates one user request as one task. The task/dependency primitives are included as the foundation for multi-step DAG execution.

## Limitations and next engineering steps

This is a working MVP, not production infrastructure. Before production use, add authentication, rate limiting, durable task storage, async/background execution, robust provider-specific error classification, token-accurate cost accounting, structured output validation, observability, and stronger evaluation.

Potential next milestones:

1. LLM-based task decomposition into a dependency graph.
2. Concurrent execution of independent tasks.
3. Cycle detection and DAG validation.
4. Provider-specific retry/backoff policies.
5. Token usage and real billing integration.
6. Evaluation of routing quality against a labeled benchmark.
7. Model escalation based on validation results.

## Author

Yash Gughane
