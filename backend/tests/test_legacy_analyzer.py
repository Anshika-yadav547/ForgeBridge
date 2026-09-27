
import unittest
from pathlib import Path
import tempfile

from backend.legacy_analyzer import (
    detect_language,
    extract_program_name,
    extract_c_functions,
    extract_c_conditions,
    extract_paragraphs,
    extract_conditions,
    extract_business_rules,
    extract_machine_reading,
    extract_temperature_limit,
    diagnose_machine,
    analyze_file,
)


class TestLegacyAnalyzer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.folder = Path(self.temp_dir.name)

    def create_file(self, name, content):
        path = self.folder / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_detect_c_language(self):
        self.assertEqual(detect_language("main.c"), "C")

    def test_detect_cpp_language(self):
        self.assertEqual(detect_language("main.cpp"), "C++")

    def test_detect_cobol_language(self):
        self.assertEqual(detect_language("main.cbl"), "COBOL")

    def test_detect_unknown_language(self):
        self.assertEqual(detect_language("main.py"), "UNKNOWN")

    def test_extract_c_function(self):
        path = self.create_file(
            "main.c",
            "int main(void) { return 0; }"
        )
        self.assertEqual(extract_c_functions(path), ["main"])

    def test_extract_c_condition(self):
        path = self.create_file(
            "main.c",
            "int main(void) { if (temperature >= limit) { return 1; } }"
        )
        self.assertEqual(
            extract_c_conditions(path),
            ["temperature >= limit"]
        )

    def test_extract_c_nested_condition(self):
        path = self.create_file(
            "main.c",
            "int main(void) { if (check(a, b)) { return 1; } }"
        )
        self.assertEqual(
            extract_c_conditions(path),
            ["check(a, b)"]
        )

    def test_extract_cobol_program_name(self):
        path = self.create_file(
            "machine.cbl",
            "PROGRAM-ID. MACHINE-STATUS."
        )
        self.assertEqual(
            extract_program_name(path, "COBOL"),
            "MACHINE-STATUS"
        )

    def test_extract_cobol_paragraphs(self):
        path = self.create_file(
            "machine.cbl",
            "MAIN-LOGIC.\nCHECK-TEMPERATURE.\n"
        )
        self.assertEqual(
            extract_paragraphs(path),
            ["MAIN-LOGIC", "CHECK-TEMPERATURE"]
        )

    def test_extract_cobol_conditions(self):
        path = self.create_file(
            "machine.cbl",
            "IF TEMPERATURE >= LIMIT\n"
        )
        self.assertEqual(
            extract_conditions(path),
            ["TEMPERATURE >= LIMIT"]
        )

    def test_extract_cobol_business_rules(self):
        path = self.create_file(
            "machine.cbl",
            "IF TEMPERATURE >= LIMIT\n"
            "    MOVE 'Y' TO ALARM-ACTIVE\n"
            "END-IF.\n"
        )
        rules = extract_business_rules(path)
        self.assertEqual(len(rules), 1)
        self.assertEqual(
            rules[0]["condition"],
            "TEMPERATURE >= LIMIT"
        )
        self.assertEqual(
            rules[0]["effects"],
            [{"variable": "ALARM-ACTIVE", "value": "'Y'"}]
        )

    def test_extract_machine_reading(self):
        path = self.create_file(
            "main.c",
            "SensorReading machine7 = {7, 86.2f, 3.1f, 22, 0};"
        )
        self.assertEqual(
            extract_machine_reading(path),
            {
                "machine_id": 7,
                "temperature_c": 86.2,
                "vibration_mm_s": 3.1,
                "coolant_flow_lpm": 22.0,
                "emergency_stop": 0,
            }
        )

    def test_extract_temperature_limit(self):
        path = self.create_file(
            "factory.h",
            "#define TEMP_LIMIT_DEFAULT 85.0f"
        )
        self.assertEqual(extract_temperature_limit(path), 85.0)

    def test_temperature_at_limit_stops_machine(self):
        reading = {
            "machine_id": 7,
            "temperature_c": 85.0,
            "vibration_mm_s": 3.1,
            "coolant_flow_lpm": 22.0,
            "emergency_stop": 0,
        }
        result = diagnose_machine(reading, 85.0)
        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["reason"], "temperature limit exceeded")

    def test_normal_reading_keeps_machine_running(self):
        reading = {
            "machine_id": 7,
            "temperature_c": 80.0,
            "vibration_mm_s": 3.1,
            "coolant_flow_lpm": 22.0,
            "emergency_stop": 0,
        }
        result = diagnose_machine(reading, 85.0)
        self.assertEqual(result["status"], "running")

    def test_emergency_stop_has_priority(self):
        reading = {
            "machine_id": 7,
            "temperature_c": 80.0,
            "vibration_mm_s": 3.1,
            "coolant_flow_lpm": 22.0,
            "emergency_stop": 1,
        }
        result = diagnose_machine(reading, 85.0)
        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["reason"], "emergency stop engaged")

    def test_missing_reading_returns_unknown(self):
        result = diagnose_machine(None, 85.0)
        self.assertEqual(result["status"], "unknown")

    def test_missing_temperature_limit_returns_unknown(self):
        reading = {
            "machine_id": 7,
            "temperature_c": 80.0,
            "vibration_mm_s": 3.1,
            "coolant_flow_lpm": 22.0,
            "emergency_stop": 0,
        }
        result = diagnose_machine(reading, None)
        self.assertEqual(result["status"], "unknown")

    def test_analyze_c_file(self):
        path = self.create_file(
            "main.c",
            "int main(void) { if (x > 0) { return 1; } return 0; }"
        )
        result = analyze_file(path)
        self.assertEqual(result["language"], "C")
        self.assertEqual(result["functions"], ["main"])
        self.assertEqual(result["status"], "parsed")

    def test_analyze_cobol_file(self):
        path = self.create_file(
            "machine.cbl",
            "PROGRAM-ID. MACHINE-STATUS.\n"
            "PROCEDURE DIVISION.\n"
            "MAIN-LOGIC.\n"
            "    IF TEMP >= LIMIT\n"
            "        MOVE 'Y' TO ALARM\n"
            "    END-IF.\n"
        )
        result = analyze_file(path)
        self.assertEqual(result["language"], "COBOL")
        self.assertEqual(result["program"], "MACHINE-STATUS")
        self.assertIn("MAIN-LOGIC", result["paragraphs"])
        self.assertEqual(result["status"], "parsed")
        

    def test_cobol_temperature_disables_production(self):
        path = self.create_file(
            "machine.cbl",
            "IF TEMPERATURE >= LIMIT\n"
            "    MOVE 'Y' TO ALARM-ACTIVE\n"
            "    MOVE 'N' TO PRODUCTION-ENABLED\n"
            "END-IF.\n"
        )

        rules = extract_business_rules(path)

        self.assertEqual(len(rules), 1)
        self.assertEqual(
            rules[0]["condition"],
            "TEMPERATURE >= LIMIT"
        )
        self.assertEqual(
            rules[0]["effects"],
            [
                {"variable": "ALARM-ACTIVE", "value": "'Y'"},
                {"variable": "PRODUCTION-ENABLED", "value": "'N'"},
            ],
        )


if __name__ == "__main__":
    unittest.main()






    