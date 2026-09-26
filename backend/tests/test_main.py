from fastapi.testclient import TestClient
from main import app

from main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analysis_returns_agent_sources():
    response = client.post(
        "/api/analyze",
        json={"question": "Machine 7 keeps stopping. Why?"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["question"] == "Machine 7 keeps stopping. Why?"
    assert body["answer"]
    assert len(body["agents"]) >= 1

    for finding in body["agents"]:
        assert finding["agent"]
        assert finding["finding"]
        assert finding["sources"]
        assert finding["status"]