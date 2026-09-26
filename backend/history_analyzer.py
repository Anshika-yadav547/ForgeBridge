
from pathlib import Path
import csv


def read_history(file_path):
    """Read historical machine records from a CSV file."""
    path = Path(file_path)

    if not path.exists():
        return {
            "status": "error",
            "reason": f"History file not found: {path}",
            "records": [],
            "source": str(path),
        }

    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            records = list(csv.DictReader(file))

        return {
            "status": "success",
            "records": records,
            "source": str(path),
        }

    except (OSError, UnicodeError, csv.Error) as error:
        return {
            "status": "error",
            "reason": str(error),
            "records": [],
            "source": str(path),
        }


def get_machine_history(records, machine_id):
    """Return only records belonging to the requested machine."""
    matching_records = [
        record for record in records
        if str(record.get("machine_id", "")).strip() == str(machine_id)
    ]

    return matching_records


def summarize_history(records):
    """Summarize recorded events without making unsupported claims."""
    if not records:
        return {
            "event_count": 0,
            "events": [],
            "summary": "No historical records were found.",
        }

    events = []

    for record in records:
        event = {
            "date": record.get("date", ""),
            "event": record.get("event", ""),
            "description": record.get("description", ""),
        }
        events.append(event)

    return {
        "event_count": len(events),
        "events": events,
        "summary": f"{len(events)} historical record(s) found.",
    }


def analyze_history(file_path, machine_id):
    """Load and summarize the history of a specific machine."""
    result = read_history(file_path)

    if result["status"] == "error":
        return result

    records = get_machine_history(result["records"], machine_id)
    summary = summarize_history(records)

    return {
        "agent": "HistoryAgent",
        "status": "success",
        "machine_id": machine_id,
        "summary": summary["summary"],
        "event_count": summary["event_count"],
        "events": summary["events"],
        "source": result["source"],
        "evidence_status": (
            "Historical records found"
            if records
            else "No matching historical records"
        ),
    }


if __name__ == "__main__":
    history_file = input("Enter history CSV path: ").strip()
    machine_id = input("Enter machine ID: ").strip()

    result = analyze_history(history_file, machine_id)

    print("\nHistory Analysis:")
    print(result)

