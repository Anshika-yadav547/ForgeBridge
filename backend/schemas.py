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