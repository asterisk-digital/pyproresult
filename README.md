# pyproresult

A simple Python library for interfacing with Proresult.

## Installation

```bash
uv add pyproresult
```

or, with pip:

```bash
pip install pyproresult
```

## ApiClient

This class is used to interface with Proresult's API properly.

### Usage

```(python)
import pyproresult

api_client = pyproresult.ApiClient(account_id="YOUR_ACCOUNT_ID", api_secret="YOUR_API_SECRET")
```

## WebClient

This class is used to interface with Proresult's web interface, to enable things like document upload.

### Usage

```(python)
import pyproresult

web_client = pyproresult.WebClient(
            base_url=envvars['PRORESULT_URL'],
            username=envvars['PRORESULT_USERNAME'],
            password=envvars['PRORESULT_PASSWORD'],
            dbname=envvars['PRORESULT_DBNAME'])
```

## Development

### Setup

To set up the python environment you need `uv`, then run:
```(bash)
uv sync --group dev
```

### Run linter

```(bash)
uv run ruff check .
```

### Run tests

```(bash)
uv run tox
```

### Run formatter

```(bash)
uv run ruff format .
```
