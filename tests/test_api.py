from fastapi.testclient import TestClient
from src.routewise.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_route_endpoint():
    response = client.post("/route", json={"prompt": "Explain a variable"})
    assert response.status_code == 200
    assert response.json()["category"] == "fast"


def test_orchestrate_endpoint():
    response = client.post(
        "/orchestrate",
        json={"prompt": "Implement a Python function to reverse a string"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_empty_prompt_rejected():
    response = client.post("/route", json={"prompt": ""})
    assert response.status_code == 422
