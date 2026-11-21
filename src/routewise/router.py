from dataclasses import dataclass
import re


@dataclass(frozen=True)
class RoutingDecision:
    category: str
    model: str
    complexity: float
    reason: str


class ModelRouter:
    \"\"\"Transparent heuristic router; no model/API call occurs here.\"\"\"

    CODING_TERMS = {
        "code", "coding", "implement", "implementation", "debug",
        "function", "class", "python", "javascript", "sql", "program",
        "script", "algorithm", "refactor", "unit test"
    }
    REASONING_TERMS = {
        "derive", "prove", "analyze", "analyse", "compare", "evaluate",
        "trade-off", "tradeoff", "architecture", "optimize", "optimise",
        "convergence", "reason", "step by step", "multi-step"
    }
    COMPLEXITY_TERMS = {
        "complex", "comprehensive", "detailed", "multiple", "architecture",
        "convergence", "derive", "prove", "optimize", "optimise",
        "compare", "evaluate", "step by step"
    }

    def __init__(self, models: dict[str, str]):
        required = {"fast", "coding", "reasoning"}
        missing = required - set(models)
        if missing:
            raise ValueError(f"Missing model mappings: {sorted(missing)}")
        self.models = dict(models)

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z][a-zA-Z0-9_+-]*", text.lower()))

    def classify(self, prompt: str) -> RoutingDecision:
        text = prompt.lower()
        tokens = self._tokens(text)
        coding_hits = len(tokens & self.CODING_TERMS)
        reasoning_hits = len(tokens & self.REASONING_TERMS)
        complexity_hits = len(tokens & self.COMPLEXITY_TERMS)

        # A transparent baseline policy. Coding intent takes precedence when
        # implementation is explicitly requested; otherwise reasoning signals
        # select the reasoning route.
        if coding_hits:
            category = "coding"
            reason = f"Detected {coding_hits} coding-related signal(s)."
        elif reasoning_hits or complexity_hits >= 2:
            category = "reasoning"
            reason = f"Detected {reasoning_hits + complexity_hits} reasoning/complexity signal(s)."
        else:
            category = "fast"
            reason = "No strong coding or advanced-reasoning signals detected."

        complexity = min(1.0, 0.15 + 0.12 * complexity_hits + 0.08 * reasoning_hits + 0.05 * coding_hits)
        if len(tokens) > 35:
            complexity = min(1.0, complexity + 0.15)

        return RoutingDecision(
            category=category,
            model=self.models[category],
            complexity=round(complexity, 2),
            reason=reason,
        )

    def route_task(self, task) -> RoutingDecision:
        return self.classify(task.description)
