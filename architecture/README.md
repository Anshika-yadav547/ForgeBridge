# ForgeBridge Architecture Map

This folder contains deterministic architecture-map output for the fictional
AUTOFACTORY-2005 legacy system.

The architecture analyzer extracts factual relationships from C and COBOL
source using lightweight parsing.

- C source files and headers
- `#include` relationships
- C function definitions
- C function-call references
- COBOL `PROGRAM-ID`
- COBOL paragraphs
- COBOL `PERFORM`, `CALL`, and `COPY` statements

## C analysis

C function definitions and call relationships are extracted using lightweight
regex-based parsing.

C call relationships are labeled `calls_heuristic` because the analyzer uses
function-name matching rather than a compiler-grade C parser. Regular
expressions provide pattern matching but do not perform full C semantic
analysis.

Therefore, `calls_heuristic` edges should be treated as likely call
relationships rather than guaranteed compiler-level dependencies.

## COBOL analysis

The COBOL graph represents the hierarchy as:

```text
COBOL file
  └── PROGRAM-ID
        └── paragraph
              └── PERFORM relationship