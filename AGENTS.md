# ForgeBridge AI project rules

## Project purpose

ForgeBridge helps engineers understand, troubleshoot, secure, and modernize
fictional legacy automotive manufacturing software.

## Main demo

Machine 7 keeps stopping. Why?

## Data rules

- AUTOFACTORY-2005 is fictional demonstration data.
- Never present fictional tickets or documents as real-world evidence.
- Use exact repository paths as sources.
- Do not invent unsupported historical facts.

## Coding rules

- Explain affected files before major changes.
- Run tests after code changes.
- Preserve all legacy safety interlocks.
- Never commit passwords, API keys, tokens, or private keys.
- Do not commit `.env` files.
- Require human review for destructive or deployment actions.

## Architecture rules

- The frontend calls only the backend orchestrator.
- The frontend must not call individual agents directly.
- Agents must use the common response format.
- Security findings should come from a scanner where possible.
- Use deterministic tools for parsing and dependency extraction.
- Use AI for explanation and reasoning.

## Integration rules

- Use feature branches.
- Merge through pull requests.
- Keep main runnable.
- Resolve conflicts carefully.