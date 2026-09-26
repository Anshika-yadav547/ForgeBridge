# AGENTS.md — Plan mode

This file provides guidance to agents when working with code in this repository.

## Architectural constraints

- **Frontend → backend only**: `App.jsx` calls `POST /api/analyze` exclusively. The frontend must never call individual agents directly.
- **Agents are not services**: `agents/*.md` are prompt/spec documents. Any new agent capability must be implemented as Python logic inside `backend/orchestrator.py`, not as a separate process or HTTP service.
- **Single orchestrator entry point**: all analysis flows through `orchestrator.analyze_question()`. The route in `main.py` is intentionally a thin pass-through.
- **Schema is the contract**: `backend/schemas.py` defines `AgentFinding` and `AnalysisResponse`. Any new agent type or field must be added here first.
- **Security findings** should come from a deterministic scanner/parser; AI is used only for explanation and reasoning — not as the evidence source.
- **CORS**: only `localhost:5173` and `5174` are allowed. A future deployment layer would need this updated.

## Planned extension points

- New agents → add to `orchestrator.analyze_question()`, return `AgentFinding` objects.
- New agent spec docs → `agents/` (Markdown only).
- New API endpoints → `main.py` with Pydantic schemas in `schemas.py`.
