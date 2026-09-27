
from pathlib import Path
import re


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def detect_language(file_path):
    extension = Path(file_path).suffix.lower()

    if extension in [".c", ".h"]:
        return "C"
    elif extension in [".cpp", ".hpp"]:
        return "C++"
    elif extension in [".cbl", ".cob"]:
        return "COBOL"
    elif extension in [".f", ".for", ".f90", ".f95"]:
        return "FORTRAN"
    return "UNKNOWN"


def extract_program_name(file_path, language):
    content = read_file(file_path)

    if language == "COBOL":
        match = re.search(
            r"PROGRAM-ID\.\s*([A-Z0-9-]+)",
            content,
            re.IGNORECASE
        )
        if match:
            return match.group(1)

    return Path(file_path).stem


def extract_c_functions(file_path):
    content = read_file(file_path)

    pattern = (
        r"\b(?:int|void|float|double|char|MachineStatus)\s+"
        r"(\w+)\s*\([^;{}]*\)\s*\{"
    )
    return re.findall(pattern, content)


def extract_c_conditions(file_path):
    content = read_file(file_path)
    conditions = []

    # Basic extraction of if and else-if conditions.
    # Handles the nested parentheses in function calls.
    for match in re.finditer(r"\b(?:if|else\s+if)\s*\(", content):
        start = match.end()
        depth = 1
        index = start

        while index < len(content) and depth:
            if content[index] == "(":
                depth += 1
            elif content[index] == ")":
                depth -= 1
            index += 1

        if depth == 0:
            condition = content[start:index - 1]
            conditions.append(" ".join(condition.split()))

    return conditions


def extract_c_business_rules(file_path):
    content = read_file(file_path)
    rules = []

    # Extract simple if/else-if blocks from the factory example.
    # This is intended for the supplied demonstration source.
    pattern = (
        r"(?:if|else\s+if)\s*\((.*?)\)\s*\{"
        r"(.*?)(?=\}\s*else|\}\s*return|\})"
    )

    for condition, body in re.findall(pattern, content, re.DOTALL):
        effects = []

        assignments = re.findall(
            r"status\.(\w+)\s*=\s*([^;]+);",
            body
        )

        for variable, value in assignments:
            effects.append({
                "variable": variable,
                "value": value.strip()
            })

        rules.append({
            "condition": " ".join(condition.split()),
            "effects": effects
        })

    return rules


def extract_paragraphs(file_path):
    paragraphs = []

    ignored = {
        "IDENTIFICATION DIVISION",
        "DATA DIVISION",
        "PROCEDURE DIVISION",
        "WORKING-STORAGE SECTION",
        "END-IF",
        "STOP RUN",
    }

    for line in read_file(file_path).splitlines():
        stripped = line.strip()

        if not stripped.endswith("."):
            continue

        name = stripped[:-1].strip()

        if name in ignored or not name or name[0].isdigit():
            continue

        if all(c.isupper() or c == "-" for c in name):
            paragraphs.append(name)

    return paragraphs


def extract_conditions(file_path):
    conditions = []

    for line in read_file(file_path).splitlines():
        stripped = line.strip()

        if stripped.upper().startswith("IF "):
            conditions.append(stripped[3:].strip())

    return conditions


def extract_business_rules(file_path):
    rules = []
    current_condition = None
    current_effects = []

    for line in read_file(file_path).splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.upper().startswith("IF "):
            current_condition = stripped[3:].strip()
            current_effects = []

        elif stripped.upper().startswith("MOVE ") and current_condition:
            move_text = stripped[5:].strip()
            parts = re.split(r"\s+TO\s+", move_text, maxsplit=1,
                             flags=re.IGNORECASE)

            if len(parts) == 2:
                current_effects.append({
                    "variable": parts[1].rstrip(".").strip(),
                    "value": parts[0].strip()
                })

        elif stripped.upper() == "END-IF." and current_condition:
            rules.append({
                "condition": current_condition,
                "effects": current_effects
            })
            current_condition = None
            current_effects = []

    return rules


def extract_machine_reading(file_path):
    content = read_file(file_path)

    match = re.search(
        r"SensorReading\s+machine7\s*=\s*\{([^}]+)\}",
        content,
        re.DOTALL
    )

    if not match:
        return None

    values = [value.strip() for value in match.group(1).split(",")]

    if len(values) != 5:
        return None

    return {
        "machine_id": int(values[0]),
        "temperature_c": float(values[1].rstrip("fF")),
        "vibration_mm_s": float(values[2].rstrip("fF")),
        "coolant_flow_lpm": float(values[3]),
        "emergency_stop": int(values[4])
    }


def extract_temperature_limit(header_path):
    content = read_file(header_path)

    match = re.search(
        r"#define\s+TEMP_LIMIT_DEFAULT\s+([0-9]+(?:\.[0-9]+)?)[fF]?",
        content
    )

    if match:
        return float(match.group(1))

    return None


def diagnose_machine(reading, temperature_limit):
    if reading is None:
        return {
            "status": "unknown",
            "reason": "Machine reading not found."
        }

    if temperature_limit is None:
        return {
            "status": "unknown",
            "reason": "Temperature limit not found."
        }

    if reading["emergency_stop"]:
        return {
            "status": "stopped",
            "reason": "emergency stop engaged"
        }

    if reading["temperature_c"] >= temperature_limit:
        return {
            "status": "stopped",
            "reason": "temperature limit exceeded"
        }

    if reading["coolant_flow_lpm"] < 10:
        return {
            "status": "stopped",
            "reason": "insufficient coolant flow"
        }

    if reading["vibration_mm_s"] > 7.5:
        return {
            "status": "stopped",
            "reason": "excessive vibration"
        }

    return {
        "status": "running",
        "reason": "no stopping condition detected"
    }


def build_analysis_result(
    file_path,
    language,
    program_name,
    paragraphs,
    conditions,
    rules,
    functions=None
):
    return {
        "agent": "LegacyCodeAgent",
        "language": language,
        "program": program_name,
        "source": str(file_path),
        "functions": functions or [],
        "paragraphs": paragraphs,
        "conditions": conditions,
        "business_rules": rules,
        "status": "parsed"
    }


def analyze_file(file_path):
    language = detect_language(file_path)
    program_name = extract_program_name(file_path, language)

    if language in ["C", "C++"]:
        functions = extract_c_functions(file_path)
        conditions = extract_c_conditions(file_path)
        rules = extract_c_business_rules(file_path)
        paragraphs = []

    elif language == "COBOL":
        functions = []
        paragraphs = extract_paragraphs(file_path)
        conditions = extract_conditions(file_path)
        rules = extract_business_rules(file_path)

    else:
        return {
            "status": "unsupported",
            "source": str(file_path),
            "language": language
        }

    return build_analysis_result(
        file_path,
        language,
        program_name,
        paragraphs,
        conditions,
        rules,
        functions
    )


def diagnose_machine_7():
    base = Path(__file__).resolve().parent.parent
    legacy = base / "legacy" / "AUTOFACTORY-2005"

    main_path = legacy / "src" / "main.c"
    alarm_path = legacy / "src" / "alarm.c"
    temperature_path = legacy / "src" / "temperature.c"
    header_path = legacy / "include" / "factory.h"

    for path in [main_path, alarm_path, temperature_path, header_path]:
        if not path.exists():
            return {
                "status": "error",
                "reason": f"Required source file not found: {path}"
            }

    reading = extract_machine_reading(main_path)
    limit = extract_temperature_limit(header_path)

    diagnosis = diagnose_machine(reading, limit)

    return {
        "machine_id": reading["machine_id"] if reading else None,
        "reading": reading,
        "temperature_limit_c": limit,
        "diagnosis": diagnosis,
        "sources": [
            str(main_path.relative_to(base)),
            str(alarm_path.relative_to(base)),
            str(temperature_path.relative_to(base)),
            str(header_path.relative_to(base))
        ]
    }


if __name__ == "__main__":
    file_path = input("Enter file path (C or COBOL): ").strip()

    if not Path(file_path).exists():
        print("File not found:", file_path)
    else:
        result = analyze_file(file_path)
        print("\nAnalysis Result:")
        print(result)

    print("\nMachine 7 Diagnosis:")
    diagnosis = diagnose_machine_7()
    print(diagnosis)

    if diagnosis.get("diagnosis", {}).get("status") == "stopped":
        reading = diagnosis["reading"]
        reason = diagnosis["diagnosis"]["reason"]

        if reason == "temperature limit exceeded":
            print(
                f"Machine {reading['machine_id']} is at "
                f"{reading['temperature_c']}°C, which meets or exceeds "
                f"the {diagnosis['temperature_limit_c']}°C threshold. "
                "The alarm activates and production is disabled."
            )
        else:
            print(
                f"Machine {reading['machine_id']} is stopped because "
                f"{reason}. The alarm activates and production is disabled."
            )
    elif diagnosis.get("diagnosis", {}).get("status") == "running":
        print("No stopping condition was detected.")
    else:
        print("Diagnosis could not be completed:", diagnosis)


            