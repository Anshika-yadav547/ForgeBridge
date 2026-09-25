# COBOL Machine Status Module

This is a fictional COBOL representation of the AUTOFACTORY-2005 Machine 7
safety-status logic.

## Program

`MACHINE-STATUS.cbl`

## Rules

- Temperature at or above 85.0C activates the alarm.
- An active alarm disables production.
- Coolant flow below 10 LPM activates the alarm.
- Vibration above 7.5 mm/s activates the alarm.
- An emergency stop activates the alarm.

## Relationship to the C system

The COBOL sample expresses equivalent business logic to:

- `src/alarm.c`
- `src/temperature.c`
- `config/limits.cfg`

This file is fictional demonstration data. It is not an operational factory
program.