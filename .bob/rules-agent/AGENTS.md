# AGENTS.md — Agent (coding) mode

This file provides guidance to agents when working with code in this repository.

## Critical constraints

- **Backend tests must be run from `backend/`**, not the repo root — `main.py` uses bare module imports (`from orchestrator import …`, `from schemas import …`) that break from any other directory.
- Run a single test: `python -m pytest tests/test_main.py::test_name` (from `backend/`).
- Frontend linter is **oxlint**, not ESLint. Config is `frontend/.oxlintrc.json`.

## Schema contract

Every agent finding returned by the orchestrator must be an `AgentFinding` (see `backend/schemas.py`):
- `status` must be an exact `AgentStatus` literal — typos silently fail Pydantic validation.
- `sources` must be **repo-relative paths**, not absolute paths.
- `language` is the only optional field.

## Orchestrator pattern

`backend/orchestrator.py` is the sole place to add agent logic. The FastAPI route in `main.py` is intentionally thin — do not add business logic there. New agents are wired into `analyze_question()` in the orchestrator.

## Frontend API URL

The backend URL is hardcoded as `http://127.0.0.1:8000/api/analyze` in `frontend/src/App.jsx`. If the port changes, update it there.

## Agents directory

`agents/*.md` are Markdown prompt/spec files for AI agent behaviour — they are **not Python modules** and are not imported anywhere.
