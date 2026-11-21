from dataclasses import dataclass, field
from threading import Lock


@dataclass
class Telemetry:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency_ms: float = 0.0
    total_estimated_cost_usd: float = 0.0
    _lock: Lock = field(default_factory=Lock, repr=False)

    def record(self, latency_ms: float, estimated_cost_usd: float, success: bool):
        with self._lock:
            self.total_requests += 1
            self.total_latency_ms += latency_ms
            self.total_estimated_cost_usd += estimated_cost_usd
            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1

    def snapshot(self) -> dict:
        with self._lock:
            count = self.total_requests
            return {
                "total_requests": count,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "average_latency_ms": round(self.total_latency_ms / count, 2) if count else 0.0,
                "total_estimated_cost_usd": round(self.total_estimated_cost_usd, 8),
            }
