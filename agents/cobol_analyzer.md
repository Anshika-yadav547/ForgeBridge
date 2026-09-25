# COBOL Analyzer

## Purpose

Understand COBOL source code and extract business rules, programs, sections,
paragraphs, variables, and calls.

## Supported source

- `.cbl`
- `.cob`
- `.cpy` copybooks

## Extract

- PROGRAM-ID
- DIVISION names
- SECTION names
- Paragraph names
- DATA DIVISION variables
- PIC definitions
- PERFORM relationships
- CALL relationships
- COPY relationships
- IF and EVALUATE conditions
- DISPLAY, READ, WRITE, and file operations

## Business-rule example

Input:

IF TEMPERATURE-C >= TEMPERATURE-LIMIT-C
    MOVE "Y" TO ALARM-ACTIVE
    MOVE "N" TO PRODUCTION-ENABLED
    MOVE "TEMPERATURE LIMIT EXCEEDED" TO STOP-REASON

Output:

- Condition: temperature is greater than or equal to the limit.
- Effect: alarm becomes active.
- Effect: production is disabled.
- Reason: temperature limit exceeded.

## Safety

- Treat this repository as fictional.
- Do not invent missing business rules.
- Return exact file paths.
- Distinguish parsed facts from AI interpretation.