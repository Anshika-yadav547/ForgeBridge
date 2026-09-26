from fastapi.testclient import TestClient

from backend.main import app


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


# ---------------------------------------------------------------------------
# Machine-status endpoint tests — Member 4, security-migration branch.
# Verifies GET /api/v1/machines/{machine_id}/status behaviour for:
#   - Machine 7 (the only demo fixture in AUTOFACTORY-2005)
#   - An unknown machine ID (should return HTTP 404)
#
# Expected Machine 7 result is derived from:
#   legacy/AUTOFACTORY-2005/src/main.c:6   — fixture: 86.2 °C, coolant 22 lpm
#   legacy/AUTOFACTORY-2005/src/alarm.c    — temperature branch fires at >= 85 °C
#   legacy/AUTOFACTORY-2005/config/limits.cfg — temperature_limit_c=85
# ---------------------------------------------------------------------------


def test_machine7_status_returns_200():
    response = client.get("/api/v1/machines/7/status")

    assert response.status_code == 200


def test_machine7_status_fields():
    response = client.get("/api/v1/machines/7/status")
    body = response.json()

    # machine_id matches the requested machine
    assert body["machine_id"] == 7

    # Alarm is active: 86.2 °C >= 85.0 °C limit (alarm.c:18–26)
    assert body["alarm_active"] is True

    # Production is disabled when an interlock trips (alarm.c:25)
    assert body["production_enabled"] is False

    # Reason string matches alarm.c:26 verbatim
    assert body["reason"] == "temperature limit exceeded"

    # Provenance label must identify the legacy system
    assert body["source"] == "AUTOFACTORY-2005"


def test_unknown_machine_returns_404():
    response = client.get("/api/v1/machines/99/status")

    assert response.status_code == 404
