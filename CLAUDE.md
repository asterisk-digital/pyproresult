# CLAUDE.md

## Project

Python library for interfacing with Proresult. Uses setuptools for builds, uv for package management.

## Setup

```bash
uv sync --group dev
```

## Commands

- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Test: `uv run tox`

## Structure

- `src/pyproresult/` - library source (ApiClient, WebClient)
- `tasks/` - standalone scripts (e.g. get_hms.py)
- `tests/` - pytest tests
- `__init__.py` - re-exports from src, uses `__all__`

## Conventions

- All dependencies are version-pinned in pyproject.toml
- Use `os.environ[]` (not `os.getenv()`) for required env vars so missing values fail loudly
- Tox runs tests against Python 3.11
