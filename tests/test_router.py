from src.routewise.router import ModelRouter


@pytest.fixture
def router():
    return ModelRouter({
        "fast": "fast-test",
        "coding": "coding-test",
        "reasoning": "reasoning-test",
    })


import pytest


def test_simple_prompt_routes_fast(router):
    decision = router.classify("Explain what a variable is")
    assert decision.category == "fast"
    assert decision.model == "fast-test"


def test_code_prompt_routes_coding(router):
    decision = router.classify("Implement a Python function to sort a list")
    assert decision.category == "coding"


def test_reasoning_prompt_routes_reasoning(router):
    decision = router.classify("Derive the convergence conditions and analyze the result")
    assert decision.category == "reasoning"


def test_missing_model_mapping_rejected():
    with pytest.raises(ValueError):
        ModelRouter({"fast": "a"})
