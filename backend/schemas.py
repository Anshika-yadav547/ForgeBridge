from typing import Literal

from pydantic import BaseModel


AgentStatus = Literal[
    "supported-by-source",
    "supported-by-sources",
    "partially-supported",
    "not-supported",
    "manual-review-required",
    "scanner-completed",
    "parsed",
    "error",
]


class AgentFinding(BaseModel):
    agent: str
    language: str | None = None
    finding: str
    sources: list[str]
    status: AgentStatus


class AnalysisRequest(BaseModel):
    question: str


class AnalysisResponse(BaseModel):
    question: str
    answer: str
    agents: list[AgentFinding]


# ---------------------------------------------------------------------------
# MachineStatusResponse
# Read-only modernization adapter — Member 4, security-migration branch.
# Maps to the MachineStatus struct in legacy/AUTOFACTORY-2005/include/factory.h
# and the response shape specified in legacy/AUTOFACTORY-2005/adapter/README.md.
# ---------------------------------------------------------------------------

class MachineStatusResponse(BaseModel):
    machine_id: int
    alarm_active: bool
    production_enabled: bool
    reason: str
    source: str
