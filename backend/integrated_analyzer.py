
from pathlib import Path

from legacy_analyzer import diagnose_machine_7
from history_analyzer import analyze_history


BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "test_history.csv"


def analyze_machine(machine_id=7, history_file=HISTORY_FILE):
    """
    Combine the current legacy diagnosis with historical machine records.

    Current diagnosis and historical events are kept separate.
    """

    if machine_id != 7:
        return {
            "status": "error",
            "message": "The current legacy demo supports Machine 7 only.",
        }

    # Analyze the current machine state using the legacy source code.
    current_diagnosis = diagnose_machine_7()

    # Read historical records from the specified CSV file.
    history = analyze_history(str(history_file), machine_id)

    return {
        "agent": "ForgeBridge Integrated Analyzer",
        "machine_id": machine_id,
        "current_diagnosis": current_diagnosis,
        "historical_analysis": history,
        "evidence_note": (
            "AUTOFACTORY-2005 and test_history.csv contain fictional "
            "demonstration data, not real-world evidence."
        ),
    }


if __name__ == "__main__":
    import json

    result = analyze_machine()
    print(json.dumps(result, indent=4, default=str))

