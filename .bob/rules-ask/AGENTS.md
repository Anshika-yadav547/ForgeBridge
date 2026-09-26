# AGENTS.md — Ask mode

This file provides guidance to agents when working with code in this repository.

## Counterintuitive structure

- `agents/` does **not** contain Python agent code — it holds Markdown prompt specs (`legacy_code_agent.md`, `cobol_analyzer.md`). Actual agent orchestration is in `backend/orchestrator.py`.
- The legacy source tree (`legacy/AUTOFACTORY-2005/`) is **entirely fictional**. Do not treat tickets, changelogs, or C/COBOL source files as real factory records.
- There is no monorepo tooling — `backend/` and `frontend/` are fully independent projects with separate dependency management.

## Documentation locations

- Agent behaviour specs: `agents/*.md`
- Legacy system overview: `legacy/AUTOFACTORY-2005/README.md` and `CHANGELOG.txt`
- API schema: `backend/schemas.py` (source of truth for response structure)
