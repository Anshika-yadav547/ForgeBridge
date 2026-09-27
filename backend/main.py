import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.machines import get_machine_status
from backend.orchestrator import analyze_question
from backend.schemas import AnalysisRequest, AnalysisResponse, MachineStatusResponse


app = FastAPI(title="ForgeBridge API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "ForgeBridge",
        "legacy_system": "AUTOFACTORY-2005",
    }

@app.get("/api/architecture")
def get_architecture():
    graph_path = Path(__file__).parent.parent / "architecture" / "graph.json"

    try:
        with open(graph_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Architecture graph not found"
        )

@app.get("/api/security")
def get_security_results():
    security_path = (
        Path(__file__).parent.parent
        / "security"
        / "semgrep-results.json"
    )

    try:
        with open(security_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Security scan results not found"
        )

@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
    return analyze_question(request.question)


# ---------------------------------------------------------------------------
# Read-only machine-status endpoint — Member 4, security-migration branch.
# Source of specification: legacy/AUTOFACTORY-2005/adapter/README.md
#
# This endpoint is strictly read-only.  It does not start or stop production,
# disable alarms, reset machines, or bypass any legacy safety interlock.
# ---------------------------------------------------------------------------

@app.get("/api/v1/machines/{machine_id}/status", response_model=MachineStatusResponse)
def machine_status(machine_id: int):
    """
    Return the read-only safety status for a machine from AUTOFACTORY-2005.

    Only machine_id=7 is defined by the current demo fixture.
    Returns HTTP 404 for any unknown machine_id.
    """
    try:
        return get_machine_status(machine_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Machine not found") from exc