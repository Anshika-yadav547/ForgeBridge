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

## Implementation

The History Agent is implemented in `backend/history_analyzer.py`.

Its main functions are:

* `read_history()`
* `get_machine_history()`
* `summarize_history()`
* `analyze_history()`

## Testing

The History Agent is tested in `backend/tests/test_history_analyzer.py`.
