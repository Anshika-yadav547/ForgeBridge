# History Agent

## Purpose

The History Agent analyzes historical machine records to help identify previous machine events and summarize their history.

## Input

* Historical records stored in a CSV file.
* Machine ID to analyze.

The CSV file should contain these columns:

* `machine_id`
* `date`
* `event`
* `description`

## Responsibilities

1. Read historical records from the provided CSV file.
2. Filter records by the requested machine ID.
3. Count the matching historical records.
4. Summarize the machine's historical events.
5. Return the source file path and evidence status.
6. Report errors when the history file cannot be read.

## Output

The agent returns:

* Agent name
* Analysis status
* Machine ID
* Summary
* Event count
* Historical events
* Source file
* Evidence status

## Evidence and Safety Rules

* Use only the historical records provided in the CSV file.
* Do not invent historical events or claim that fictional demonstration data is real.
* Clearly distinguish historical records from current machine diagnostics.
* Include the source file path in the result.
* If no matching records exist, report that no matching historical records were found.
* If the CSV file cannot be read, return an error instead of inventing results.

## Historical Evidence Analysis

When investigating the historical temperature-limit change for Machine 7:

1. Check `legacy/AUTOFACTORY-2005/CHANGELOG.txt` for the recorded change from 90°C to 85°C.
2. Check `legacy/AUTOFACTORY-2005/tickets/BUG-187.txt` for the documented symptom and resolution.
3. Check `legacy/AUTOFACTORY-2005/docs/maintenance_notes.txt` for the investigation findings.
4. Check the current temperature limit in `legacy/AUTOFACTORY-2005/include/factory.h`.

### Evidence-Based Findings

* The changelog records that the temperature limit changed from 90°C to 85°C after the Machine 7 thermal-stop investigation.
* The maintenance notes link intermittent stops to heat accumulation near the enclosed spindle housing.
* BUG-187 documents the temperature-limit change.
* The C header defines the current default temperature limit as 85.0°C.
* The available records do not explain why 85°C was selected specifically.

### Historical Evidence Rules

* Cite the exact file path supporting each historical claim.
* Clearly distinguish documented facts from interpretations.
* Do not invent missing historical details, people, dates, or technical explanations.
* If an expected evidence file is missing, report that it could not be found.
* Clearly label all AUTOFACTORY-2005 historical data as fictional.
* Do not confuse historical findings with the current machine diagnosis.





## Implementation

The History Agent is implemented in `backend/history_analyzer.py`.

Its main functions are:

* `read_history()`
* `get_machine_history()`
* `summarize_history()`
* `analyze_history()`

## Testing

The History Agent is tested in `backend/tests/test_history_analyzer.py`.
