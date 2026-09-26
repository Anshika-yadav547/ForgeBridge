# ForgeBridge Baseline Verification

## Project

ForgeBridge AI

## Legacy system

AUTOFACTORY-2005

## Verification date

2026-09-25

## Repository state

The ForgeBridge repository contains the fictional AUTOFACTORY-2005 legacy
automotive manufacturing system.

The legacy system includes:

- C source files.
- Configuration files.
- Fictional factory documentation.
- Fictional maintenance tickets.
- A changelog.
- Repeatable tests.
- A fictional COBOL module.

## Main demonstration scenario

Machine 7 keeps stopping.

## Test command

Run from the repository root:

```bash
cd legacy/AUTOFACTORY-2005
make test
```

## Expected result

```text
PASS: thermal interlock
```

## Runtime behavior

The sample Machine 7 reading is above the fictional 85C temperature limit.

The expected behavior is:

- The alarm becomes active.
- Production becomes disabled.
- The reason is reported as temperature limit exceeded.

## Baseline conclusion

The AUTOFACTORY-2005 legacy program runs successfully before the ForgeBridge
backend, agents, security scanner, and frontend are added.

All factory data, tickets, maintenance notes, configuration, and source comments
are fictional demonstration data. They must not be treated as real-world factory
evidence.