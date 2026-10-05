# pyproresult

A simple Python library for interfacing with [Proresult](https://proresult.app).

Unofficial: this project is not affiliated with or endorsed by Proresult.

## Installation

```bash
pip install pyproresult
```

## ApiClient

Reads data from Proresult's API.

```python
import pyproresult

api_client = pyproresult.ApiClient(account_id="YOUR_ACCOUNT_ID", api_secret="YOUR_API_SECRET")
projects = api_client.get_projects()
```

## WebClient

Uses Proresult's web interface for things the API doesn't cover, like document upload.

```python
import os

import pyproresult

web_client = pyproresult.WebClient(
    base_url=os.environ["PRORESULT_URL"],
    username=os.environ["PRORESULT_USERNAME"],
    password=os.environ["PRORESULT_PASSWORD"],
    dbname=os.environ["PRORESULT_DBNAME"],
)
```

Both clients raise `pyproresult.ProresultException` on failure.

## Contributing

```bash
uv sync
uv run ruff check . && uv run ruff format --check . && uv run tox
```

- Runtime dependencies use lower bounds (`>=`); dev dependencies are exact-pinned.
- Read required env vars with `os.environ[]`, not `os.getenv()`, so missing values fail loudly.
