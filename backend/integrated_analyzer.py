
from pathlib import Path

from legacy_analyzer import diagnose_machine_7
from history_analyzer import analyze_history


BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = (
    BASE_DIR
    / "legacy"
    / "AUTOFACTORY-2005"
    / "docs"
    / "machine_history.csv"
)


def analyze_machine(
    machine_id: int = 7,
    history_file: Path = HISTORY_FILE,
) -> dict:
    if not isinstance(machine_id, int) or isinstance(machine_id, bool):
        raise TypeError("machine_id must be an integer")

    if not isinstance(history_file, Path):
        raise TypeError("history_file must be a Path")

   

    if machine_id != 7:
       return {
           "agent": "ForgeBridge Integrated Analyzer",
           "machine_id": machine_id,
           "status": "error",
           "message": "Machine 7 only is currently supported.",
        } 

    current_diagnosis = diagnose_machine_7()

    if not history_file.exists():
        history = {
            "status": "error",
            "message": f"Machine history file not found: {history_file}",
    }
    else:
        history = analyze_history(str(history_file), machine_id)





    history = analyze_history(str(history_file), machine_id)

    historical_finding = {
        **history,
        "agent": "HistoryAgent",
        "language": None,
        "finding": (
            history.get("summary")
            or history.get("reason")
            or "No historical information found."
        ),
        "sources": [str(history_file)],
        "status": (
            "supported-by-sources"
            if history.get("summary")
            else "error"
        ),
    }

    return {
        "agent": "ForgeBridge Integrated Analyzer",
        "machine_id": machine_id,
        "current_diagnosis": current_diagnosis,
        "historical_analysis": historical_finding,
        "evidence_note": (
            "This is fictional legacy factory data and not real-world evidence. "
            "Current diagnosis is based on legacy code. "
            "Historical analysis is based on the machine history CSV."
        ),
    }

