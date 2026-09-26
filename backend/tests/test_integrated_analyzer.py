
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.integrated_analyzer import analyze_machine


class TestIntegratedAnalyzer(unittest.TestCase):

    @patch("backend.integrated_analyzer.diagnose_machine_7")
    @patch("backend.integrated_analyzer.analyze_history")
    def test_successful_integration(self, mock_history, mock_diagnosis):
        mock_diagnosis.return_value = {
            "machine_id": 7,
            "diagnosis": {
                "status": "stopped",
                "reason": "temperature limit exceeded"
            }
        }

        mock_history.return_value = {
            "status": "success",
            "machine_id": 7,
            "event_count": 2,
            "events": [
                {"event": "STOP"},
                {"event": "INSPECTION"}
            ]
        }

        result = analyze_machine()

        self.assertEqual(result["machine_id"], 7)
        self.assertIn("current_diagnosis", result)
        self.assertIn("historical_analysis", result)
        self.assertEqual(
            result["current_diagnosis"]["diagnosis"]["status"],
            "stopped"
        )
        self.assertEqual(
            result["historical_analysis"]["event_count"],
            2
        )

    def test_invalid_machine_id(self):
        result = analyze_machine(machine_id=8)

        self.assertEqual(result["status"], "error")
        self.assertIn("Machine 7 only", result["message"])

    @patch("backend.integrated_analyzer.diagnose_machine_7")
    @patch("backend.integrated_analyzer.analyze_history")
    def test_fictional_data_disclaimer(self, mock_history, mock_diagnosis):
        mock_diagnosis.return_value = {"machine_id": 7}
        mock_history.return_value = {
            "status": "success",
            "machine_id": 7
        }

        result = analyze_machine()

        self.assertIn("fictional", result["evidence_note"].lower())
        self.assertIn("not real-world evidence", result["evidence_note"])

    @patch("backend.integrated_analyzer.diagnose_machine_7")
    @patch("backend.integrated_analyzer.analyze_history")
    def test_missing_history_file(self, mock_history, mock_diagnosis):
        mock_diagnosis.return_value = {"machine_id": 7}
        mock_history.return_value = {
            "status": "error",
            "message": "File not found"
        }

        result = analyze_machine(
            history_file=Path("missing_history.csv")
        )

        self.assertEqual(
            result["historical_analysis"]["status"],
            "error"
        )
        self.assertIn("current_diagnosis", result)


if __name__ == "__main__":
    unittest.main()

