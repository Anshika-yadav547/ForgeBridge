## Language support

The agent must identify the source language before analysis.

- `.c`, `.h` → C
- `.cpp`, `.hpp` → C++
- `.cbl`, `.cob` → COBOL
- `.f`, `.for`, `.f90`, `.f95` → FORTRAN

For COBOL, inspect:

- Divisions.
- Sections.
- Paragraphs.
- PERFORM statements.
- CALL statements.
- IF and EVALUATE conditions.
- Data definitions and PIC clauses.
- COPY statements.

The answer must include:

- Detected language.
- Program or module name.
- Business rules.
- Dependencies.
- Source paths.
- Evidence status.