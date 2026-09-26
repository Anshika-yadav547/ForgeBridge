# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project purpose

ForgeBridge helps engineers understand, troubleshoot, secure, and modernize
fictional legacy automotive manufacturing software (AUTOFACTORY-2005).

## Stack

- **Backend**: Python / FastAPI + Uvicorn, in `backend/`. No `pyproject.toml` — plain `requirements.txt`.
- **Frontend**: React 19 + Vite, in `frontend/`. Linter is **oxlint** (not ESLint).
- **Legacy data**: `legacy/AUTOFACTORY-2005/` — fictional C/COBOL/FORTRAN sources, tickets, docs.

## Commands

All backend commands must be run from `backend/` (pytest discovery relies on relative imports):

```bash
# Backend
cd backend
python -m pytest                          # all tests
python -m pytest tests/test_main.py::test_health   # single test
uvicorn main:app --reload                 # dev server on :8000

# Frontend (from frontend/)
npm run dev       # Vite dev server on :5173
npm run lint      # oxlint
npm run build
```

No root-level `Makefile` or monorepo runner — each sub-project is managed independently.

## Architecture

- The frontend calls **only** `http://127.0.0.1:8000/api/analyze` (hardcoded in `App.jsx`).
- `POST /api/analyze` → `orchestrator.analyze_question()` → returns `AnalysisResponse` (schemas defined in `backend/schemas.py`).
- Agents are **not HTTP services** — `agents/` contains only Markdown prompt/spec files.
- The orchestrator currently returns deterministic stub data; real agent calls go here.

## Response schema (AgentFinding)

All agent results must conform to `backend/schemas.py`:
- `status` must be one of the `AgentStatus` literals: `supported-by-source`, `supported-by-sources`, `partially-supported`, `not-supported`, `manual-review-required`, `scanner-completed`, `parsed`, `error`.
- `sources` must be **exact repo-relative paths** (e.g. `legacy/AUTOFACTORY-2005/src/alarm.c`).
- `language` is optional (`str | None`).

## Data rules

- AUTOFACTORY-2005 is **fictional** demonstration data — never present as real-world evidence.
- All findings must cite exact repository paths as sources.
- Do not invent business rules not present in the source files.
- Distinguish parsed facts from AI interpretation.

## Coding rules

- Explain affected files before major changes.
- Run tests after code changes.
- Preserve all legacy safety interlocks.
- Never commit passwords, API keys, tokens, `.env` files, or private keys.
- Require human review for destructive or deployment actions.
- Use feature branches; merge through pull requests; keep `main` runnable.

## CORS

Backend allows `localhost:5173` and `localhost:5174` only. If you add new origins, update `main.py`.
