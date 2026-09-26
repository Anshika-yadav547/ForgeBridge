# ForgeBridge Architecture Map

This folder contains deterministic architecture-map output for the fictional AUTOFACTORY-2005 legacy system.

The architecture analyzer extracts factual relationships from C and COBOL source using lightweight parsing:

- C source files and headers
- `#include` relationships
- Function definitions
- Function-call references
- COBOL `PROGRAM-ID`
- COBOL paragraphs
- COBOL `PERFORM`, `CALL`, and `COPY` statements

This is not compiler-grade analysis. Any relationship created by AI reasoning rather than direct parsing must be labeled `inferred` or `heuristic`.
## Generate graph JSON

From the repository root:

```bash
python -m backend.export_architecture