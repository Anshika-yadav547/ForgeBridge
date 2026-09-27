
import unittest
import tempfile
from pathlib import Path

from backend.history_analyzer import  (
    read_history,
    get_machine_history,
    summarize_history,
    analyze_history,
)


class TestHistoryAnalyzer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.csv_path = Path(self.temp_dir.name) / "history.csv"

        self.csv_path.write_text(
            "machine_id,date,event,description\n"
            "7,2026-09-20,STOP,Temperature limit exceeded\n"
            "7,2026-09-21,INSPECTION,Machine inspected\n"
            "8,2026-09-22,STOP,Coolant flow issue\n",
            encoding="utf-8",
        )

    def test_read_history(self):
        result = read_history(self.csv_path)
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["records"]), 3)

    def test_missing_file(self):
        result = read_history(
            Path(self.temp_dir.name) / "missing.csv"
        )
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["records"], [])

    def test_get_machine_history(self):
        result = read_history(self.csv_path)
        records = get_machine_history(result["records"], 7)
        self.assertEqual(len(records), 2)

    def test_no_matching_machine(self):
        result = read_history(self.csv_path)
        records = get_machine_history(result["records"], 99)
        self.assertEqual(records, [])

    def test_summarize_history(self):
        result = read_history(self.csv_path)
        records = get_machine_history(result["records"], 7)
        summary = summarize_history(records)

        self.assertEqual(summary["event_count"], 2)
        self.assertEqual(
            summary["summary"],
            "2 historical record(s) found."
        )

    def test_empty_history_summary(self):
        summary = summarize_history([])
        self.assertEqual(summary["event_count"], 0)
        self.assertEqual(
            summary["summary"],
            "No historical records were found."
        )

    def test_analyze_history(self):
        result = analyze_history(self.csv_path, 7)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["machine_id"], 7)
        self.assertEqual(result["event_count"], 2)
        self.assertEqual(
            result["evidence_status"],
            "Historical records found"
        )

    def test_analyze_history_no_matching_records(self):
        result = analyze_history(self.csv_path, 99)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["event_count"], 0)
        self.assertEqual(
            result["evidence_status"],
            "No matching historical records"
        )

    def test_analyze_history_missing_file(self):
        missing_path = Path(self.temp_dir.name) / "missing.csv"
        result = analyze_history(missing_path, 7)

        self.assertEqual(result["status"], "error")
        self.assertIn("reason", result)


if __name__ == "__main__":
    unittest.main()

