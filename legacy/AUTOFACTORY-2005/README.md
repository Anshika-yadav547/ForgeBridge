# AUTOFACTORY-2005

A fictional C legacy system for the ForgeBridge AI hackathon.

It models automotive factory machines and safety interlocks. All factory
records are synthetic and must not be treated as real-world evidence.

## Build

```bash
make
./build/autofactory
```

## Test

```bash
make test
```

The sample run evaluates Machine 7 at 86.2 C. It reports an alarm because the
configured inclusive threshold is 85 C.

## Directories

- `src/` contains legacy C source files.
- `include/` contains shared declarations.
- `config/` contains machine thresholds.
- `docs/` contains fictional factory documentation.
- `tickets/` contains fictional bugs and change requests.
- `tests/` contains repeatable tests.
- `adapter/` contains the modernization bridge design.