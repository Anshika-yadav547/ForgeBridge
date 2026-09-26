# Migration Agent

## Purpose

Plan and support read-only modernization of the fictional AUTOFACTORY-2005
legacy system.

This agent helps engineers understand what the legacy C system does, map that
behaviour to a modern REST API shape, and implement the bridge without
modifying or bypassing any legacy safety logic.

The agent does not implement anything autonomously. All changes require human
review and approval before being applied.

## Scope

| Layer | Path | Role |
|---|---|---|
| Legacy C source | `legacy/AUTOFACTORY-2005/src/` | Evaluation logic — read-only reference |
| Legacy header | `legacy/AUTOFACTORY-2005/include/factory.h` | Types and constants |
| Legacy config | `legacy/AUTOFACTORY-2005/config/limits.cfg`, `legacy/AUTOFACTORY-2005/config/machine.cfg` | Thresholds and machine identity |
| Adapter design | `legacy/AUTOFACTORY-2005/adapter/README.md` | Authoritative endpoint specification |
| Change ticket | `legacy/AUTOFACTORY-2005/tickets/CHANGE-241.txt` | Constraint: no interlock bypass |
| Backend | `backend/` | Target for the REST API implementation |

COBOL source (`legacy/AUTOFACTORY-2005/cobol/MACHINE-STATUS.cbl`) is a
parallel fictional representation of the same logic. It is a reference for
understanding business rules, not a runtime dependency of the adapter.

## Required endpoint

```
GET /api/v1/machines/{machine_id}/status
```

Source of this specification: `legacy/AUTOFACTORY-2005/adapter/README.md`

### Expected response — Machine 7

```json
{
  "machine_id": 7,
  "alarm_active": true,
  "production_enabled": false,
  "reason": "temperature limit exceeded",
  "source": "AUTOFACTORY-2005"
}
```

Field definitions derived from `legacy/AUTOFACTORY-2005/include/factory.h`
(`MachineStatus` struct) and `legacy/AUTOFACTORY-2005/src/alarm.c`
(evaluation logic):

| Field | Legacy source | Type | Notes |
|---|---|---|---|
| `machine_id` | `SensorReading.machine_id` | integer | Machine 7 is the only demo fixture |
| `alarm_active` | `MachineStatus.alarm_active` | boolean | `true` when any interlock trips |
| `production_enabled` | `MachineStatus.production_enabled` | boolean | `false` when any interlock trips |
| `reason` | `MachineStatus.reason` | string | Verbatim interlock reason string |
| `source` | Provenance label | string | Always `"AUTOFACTORY-2005"` |

## Machine 7 safety-status behaviour

The following is derived entirely from `legacy/AUTOFACTORY-2005/src/alarm.c`
and `legacy/AUTOFACTORY-2005/config/limits.cfg`. Every statement is traceable to a source file.

| Condition | File | Behaviour |
|---|---|---|
| `emergency_stop != 0` | `alarm.c:14` | `alarm_active=true`, `production_enabled=false`, reason: `"emergency stop engaged"` |
| `temperature_c >= 85.0` | `alarm.c:18`, `temperature.c:3`, `limits.cfg:1` | `alarm_active=true`, `production_enabled=false`, reason: `"temperature limit exceeded"` |
| `coolant_flow_lpm < 10` | `alarm.c:27`, `limits.cfg:2` | `alarm_active=true`, `production_enabled=false`, reason: `"insufficient coolant flow"` |
| `vibration_mm_s > 7.5` | `alarm.c:31`, `limits.cfg:3` | `alarm_active=true`, `production_enabled=false`, reason: `"excessive vibration"` |
| All within limits | `alarm.c:7–12` | `alarm_active=false`, `production_enabled=true`, reason: `"normal"` |

The demo fixture in `main.c:6` is `{7, 86.2f, 3.1f, 22, 0}` — Machine 7 at
86.2 °C, which exceeds the 85.0 °C limit. The expected demo response is
therefore `alarm_active: true`, `reason: "temperature limit exceeded"`.

Raw sensor scaling: `sensor.c:7` divides raw sensor values by 10.0
(`sensor_scale=10` in `legacy/AUTOFACTORY-2005/config/machine.cfg`).

## 404 behaviour

Requests for any `machine_id` other than `7` must return HTTP 404. Only
Machine 7 is defined by the legacy demo fixture. This is consistent with
`CHANGE-241.txt` (expose machine status) and `adapter/README.md` (read-only
bridge for the demo).

```json
{"detail": "Machine not found"}
```

## Read-only requirement

The migration agent must never create, recommend, or describe API operations
that perform any of the following:

- Start production
- Stop production
- Disable or reset alarms
- Reset machines
- Change machine configuration at runtime
- Bypass, weaken, or remove safety interlocks

This constraint comes from two independent sources:

1. `legacy/AUTOFACTORY-2005/adapter/README.md` — *"The adapter must not
   provide endpoints that disable alarms, start production, stop production,
   or bypass safety interlocks."*
2. `legacy/AUTOFACTORY-2005/tickets/CHANGE-241.txt` — *"Do not bypass legacy
   safety interlocks."*
3. `AGENTS.md` — *"Preserve all legacy safety interlocks."*

The REST API must expose only `GET` methods. No `POST`, `PUT`, `PATCH`, or
`DELETE` routes are permitted for machine control.

## Data provenance

All machine status data must be derived from the existing legacy system.
Invented or fabricated data must not be returned. Every response must include:

```json
"source": "AUTOFACTORY-2005"
```

This identifies the data as originating from the fictional AUTOFACTORY-2005
codebase and must not be omitted.

## Architecture

```
GET /api/v1/machines/{machine_id}/status
        │
        ▼
backend/main.py          ← FastAPI app; GET route only
        │
        ▼
backend/adapter.py       ← Applies alarm.c evaluation logic in Python
        │                   Reads thresholds from legacy/AUTOFACTORY-2005/config/limits.cfg
        ▼
backend/schemas.py       ← Pydantic MachineStatusResponse model
```

The frontend (when present) must call the backend orchestrator, not this
adapter directly. Source: `AGENTS.md` — *"The frontend calls only the backend
orchestrator."*

## Files to create (not yet implemented)

| File | Purpose |
|---|---|
| `backend/schemas.py` | Pydantic response model (`MachineStatusResponse`) |
| `backend/adapter.py` | Python evaluation of legacy interlock logic |
| `backend/main.py` | FastAPI app with `GET /api/v1/machines/{machine_id}/status` |
| `backend/requirements.txt` | `fastapi`, `uvicorn[standard]` |

No legacy C, COBOL, or configuration files are to be modified.

## Safety rules

- Do not modify `legacy/AUTOFACTORY-2005/src/` as part of the migration.
- Do not modify `legacy/AUTOFACTORY-2005/cobol/` as part of the migration.
- Do not modify `legacy/AUTOFACTORY-2005/config/` as part of the migration.
- Legacy safety interlock logic must be faithfully reproduced in the adapter,
  not relaxed, removed, or altered.
- Require human review before applying any safety-related or deployment change.
- AUTOFACTORY-2005 is fictional demonstration data; never present its
  behaviour as real-world evidence.
- Never commit passwords, API keys, tokens, or private keys.

## Evidence rules

Every modernization explanation must:

1. Identify the relevant source file and line number.
2. Distinguish between:
   - `[repository]` — statements directly traceable to a file in this repo
   - `[interpretation]` — AI reasoning about what the code means or how to
     map it to the API
3. Not invent legacy data, historical facts, or undocumented behaviours.

## Related files

| File | Role |
|---|---|
| `AGENTS.md` | Project-wide rules |
| `legacy/AUTOFACTORY-2005/adapter/README.md` | Endpoint specification and write-operation prohibition |
| `legacy/AUTOFACTORY-2005/tickets/CHANGE-241.txt` | Change constraint: no interlock bypass |
| `legacy/AUTOFACTORY-2005/include/factory.h` | `MachineStatus` and `SensorReading` type definitions |
| `legacy/AUTOFACTORY-2005/src/alarm.c` | Four-branch interlock evaluation logic |
| `legacy/AUTOFACTORY-2005/src/temperature.c` | Temperature threshold comparison |
| `legacy/AUTOFACTORY-2005/src/sensor.c` | Raw sensor scaling (÷ 10) |
| `legacy/AUTOFACTORY-2005/config/limits.cfg` | Threshold values: 85 °C, 10 lpm, 7.5 mm/s |
| `legacy/AUTOFACTORY-2005/config/machine.cfg` | Machine 7 identity and sensor scale |
| `agents/security_agent.md` | Security scan rules for this codebase |
