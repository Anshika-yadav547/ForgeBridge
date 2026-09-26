# machines.py
# Read-only modernization adapter — Member 4, security-migration branch.
#
# This module bridges the fictional AUTOFACTORY-2005 legacy C system to the
# REST API.  It reproduces the safety-interlock evaluation logic from:
#
#   legacy/AUTOFACTORY-2005/src/alarm.c        (four-branch interlock logic)
#   legacy/AUTOFACTORY-2005/include/factory.h  (MachineStatus struct / TEMP_LIMIT_DEFAULT)
#   legacy/AUTOFACTORY-2005/config/limits.cfg  (85 °C, 10 lpm, 7.5 mm/s)
#   legacy/AUTOFACTORY-2005/src/main.c:6       (Machine 7 demo fixture)
#
# The legacy C source is NOT modified.  This adapter is a Python translation
# of the same deterministic logic for use in the read-only status endpoint.
#
# Only Machine 7 is defined by the current demo fixture.  No additional
# machines are invented.  Unknown machine IDs raise KeyError so the API
# layer can convert them to HTTP 404.

from backend.schemas import MachineStatusResponse

# ---------------------------------------------------------------------------
# Demo fixture
# Source: legacy/AUTOFACTORY-2005/src/main.c:6
#   SensorReading machine7 = {7, 86.2f, 3.1f, 22, 0};
# ---------------------------------------------------------------------------
_MACHINE_7_FIXTURE = {
    "machine_id": 7,
    "temperature_c": 86.2,
    "vibration_mm_s": 3.1,
    "coolant_flow_lpm": 22,
    "emergency_stop": False,
}

# ---------------------------------------------------------------------------
# Thresholds
# Source: legacy/AUTOFACTORY-2005/config/limits.cfg and legacy/AUTOFACTORY-2005/include/factory.h
# ---------------------------------------------------------------------------
_TEMP_LIMIT_C = 85.0       # factory.h: TEMP_LIMIT_DEFAULT; limits.cfg: temperature_limit_c=85
_MIN_COOLANT_LPM = 10      # limits.cfg: minimum_coolant_flow_lpm=10
_MAX_VIBRATION_MM_S = 7.5  # limits.cfg: maximum_vibration_mm_s=7.5

_SOURCE = "AUTOFACTORY-2005"


def _evaluate_machine(fixture: dict) -> MachineStatusResponse:
    """
    Reproduce the interlock evaluation from legacy/AUTOFACTORY-2005/src/alarm.c.

    Branch order matches alarm.c exactly (emergency_stop → temperature →
    coolant → vibration).  The logic is not modified; it is translated from C
    to Python for the read-only status adapter.
    """
    machine_id = fixture["machine_id"]

    # Default: all clear (alarm.c:7–12)
    alarm_active = False
    production_enabled = True
    reason = "normal"

    if fixture["emergency_stop"]:
        # alarm.c:14–17
        alarm_active = True
        production_enabled = False
        reason = "emergency stop engaged"
    elif fixture["temperature_c"] >= _TEMP_LIMIT_C:
        # alarm.c:18–26  (temperature_exceeds_limit uses >=)
        alarm_active = True
        production_enabled = False
        reason = "temperature limit exceeded"
    elif fixture["coolant_flow_lpm"] < _MIN_COOLANT_LPM:
        # alarm.c:27–30
        alarm_active = True
        production_enabled = False
        reason = "insufficient coolant flow"
    elif fixture["vibration_mm_s"] > _MAX_VIBRATION_MM_S:
        # alarm.c:31–34
        alarm_active = True
        production_enabled = False
        reason = "excessive vibration"

    return MachineStatusResponse(
        machine_id=machine_id,
        alarm_active=alarm_active,
        production_enabled=production_enabled,
        reason=reason,
        source=_SOURCE,
    )


def get_machine_status(machine_id: int) -> MachineStatusResponse:
    """
    Return the read-only safety status for a machine.

    Only machine_id=7 is defined by the AUTOFACTORY-2005 demo fixture.
    Raises KeyError for any unknown machine_id so the API layer can
    return HTTP 404.

    This function is strictly read-only.  It does not start or stop
    production, disable alarms, reset machines, or modify any configuration.
    """
    if machine_id == 7:
        return _evaluate_machine(_MACHINE_7_FIXTURE)

    raise KeyError(f"Machine {machine_id} not found in AUTOFACTORY-2005")
