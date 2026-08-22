# AGENTS.md — Universal Guidelines

See [`AGENT.md`](AGENT.md) for master architecture rules, non-negotiable hardware/firmware constraints, and module ownership.

### Quick Command Reference
```bash
# Python tests and linting
uv run pytest
uv run ruff check --fix
uv run ruff format

# Repository synchronization
.\sync.ps1 -m "feat(scope): message"
.\sync.ps1 -Build           # compile thesis PDF first, then sync
```
