import json
from pathlib import Path
from src.routewise.config import settings
from src.routewise.router import ModelRouter

models = {
    "fast": settings.fast_model,
    "coding": settings.coding_model,
    "reasoning": settings.reasoning_model,
}
router = ModelRouter(models)
cases = json.loads(Path("evaluation/routing_cases.json").read_text())
correct = 0

for case in cases:
    predicted = router.classify(case["prompt"]).category
    expected = case["expected_category"]
    passed = predicted == expected
    correct += int(passed)
    print(f"{'PASS' if passed else 'FAIL'} expected={expected} predicted={predicted} | {case['prompt']}")

print(f"\nRouting accuracy: {correct}/{len(cases)} = {correct / len(cases):.1%}")
