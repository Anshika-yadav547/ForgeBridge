# Contributing to ForgeBridge

## Main branch

The `main` branch must remain stable.

Do not push unfinished work directly to `main`.

## Feature branches

Use a separate branch for each task:

- `member-1-integration`
- `member-2-legacy`
- `member-3-architecture`
- `member-4-security-migration`
- `member-5-frontend-demo`

## Pull requests

Every feature must:

1. Be developed on a separate branch.
2. Include a clear description.
3. Include tests or explain why tests are not applicable.
4. Preserve legacy safety behavior.
5. Avoid secrets and credentials.
6. Be reviewed before merging.

## Required checks

Legacy code:

```bash
cd legacy/AUTOFACTORY-2005
make test
```

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm run build
```

## Commit style

Use clear commit messages:

- `Add Legacy Code Agent`
- `Add architecture graph extraction`
- `Add security scanning`
- `Add read-only status API`
- `Add ForgeBridge dashboard`