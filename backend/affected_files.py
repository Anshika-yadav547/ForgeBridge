from __future__ import annotations

from pathlib import Path


TEMPERATURE_RULE_FILES = [
    {
        "path": "legacy/AUTOFACTORY-2005/src/alarm.c",
        "reason": (
            "Evaluates machine safety conditions and disables production "
            "when the temperature limit is exceeded."
        ),
        "evidence_type": "direct-code",
    },
    {
        "path": "legacy/AUTOFACTORY-2005/src/temperature.c",
        "reason": (
            "Contains temperature_exceeds_limit(), which performs the "
            "inclusive temperature comparison."
        ),
        "evidence_type": "direct-code",
    },
    {
        "path": "legacy/AUTOFACTORY-2005/include/factory.h",
        "reason": (
            "Defines TEMP_LIMIT_DEFAULT and shared machine data structures "
            "used by the temperature safety logic."
        ),
        "evidence_type": "direct-code",
    },
    {
        "path": "legacy/AUTOFACTORY-2005/config/limits.cfg",
        "reason": (
            "Documents the configured temperature_limit_c value of 85."
        ),
        "evidence_type": "configuration",
    },
    {
        "path": "legacy/AUTOFACTORY-2005/tests/run_tests.sh",
        "reason": (
            "Verifies that the thermal interlock reports the expected alarm "
            "behavior."
        ),
        "evidence_type": "test",
    },
    {
        "path": "legacy/AUTOFACTORY-2005/cobol/MACHINE-STATUS.cbl",
        "reason": (
            "Contains the equivalent COBOL temperature rule in the "
            "CHECK-TEMPERATURE paragraph."
        ),
        "evidence_type": "equivalent-legacy-rule",
    },
    {
        "path": "legacy/AUTOFACTORY-2005/tickets/BUG-187.txt",
        "reason": (
            "Records the fictional decision to lower the Machine 7 trip "
            "point from 90C to 85C."
        ),
        "evidence_type": "history",
    },
]


def get_temperature_affected_files(
    repository_root: Path,
) -> list[dict[str, str]]:
    affected_files = []

    for item in TEMPERATURE_RULE_FILES:
        file_path = repository_root / item["path"]

        if file_path.exists():
            affected_files.append(item)

    return affected_files