from time import perf_counter
from uuid import uuid4

from .tasks import Task, DependencyExecutor


class OrchestrationError(RuntimeError):
    pass


class Orchestrator:
    def __init__(self, router, providers, telemetry, default_max_retries: int = 1):
        self.router = router
        self.providers = providers
        self.telemetry = telemetry
        self.default_max_retries = default_max_retries

    def run(self, prompt: str, max_retries: int | None = None) -> dict:
        task = Task(
            task_id=f"task_{uuid4().hex[:10]}",
            description=prompt,
            capability="auto",
            max_retries=self.default_max_retries if max_retries is None else max_retries,
        )
        executor = DependencyExecutor([task])
        started = perf_counter()
        total_cost = 0.0
        used_fallback = False
        decision = self.router.route_task(task)
        task.status = "running"
        last_error = None

        while task.attempts <= task.max_retries:
            task.attempts += 1
            try:
                provider = self.providers.get(decision.category)
                result = provider.generate(prompt, decision.model)
                task.result = result.text
                task.status = "completed"
                total_cost += result.estimated_cost_usd
                break
            except Exception as primary_error:
                last_error = primary_error
                # One fallback attempt is made after the primary retry budget.
                if task.attempts <= task.max_retries:
                    continue
                try:
                    used_fallback = True
                    fallback_result = self.providers.fallback_provider.generate(
                        prompt, self.router.models["fast"]
                    )
                    task.result = fallback_result.text
                    task.status = "completed"
                    total_cost += fallback_result.estimated_cost_usd
                    break
                except Exception as fallback_error:
                    task.status = "failed"
                    last_error = fallback_error
                    break

        latency_ms = (perf_counter() - started) * 1000
        success = task.status == "completed"
        self.telemetry.record(latency_ms, total_cost, success)

        if not success:
            raise OrchestrationError(
                f"Task {task.task_id} failed after {task.attempts} attempt(s): {last_error}"
            )

        return {
            "task_id": task.task_id,
            "status": task.status,
            "category": decision.category,
            "model": decision.model,
            "attempts": task.attempts,
            "result": task.result,
            "latency_ms": round(latency_ms, 2),
            "estimated_cost_usd": round(total_cost, 8),
            "used_fallback": used_fallback,
            "routing_reason": decision.reason,
            "complexity": decision.complexity,
        }
