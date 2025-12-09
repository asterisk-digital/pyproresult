# pyproresult

A simple Python library for interfacing with Proresult.

## Setup
To set up for development, run:
```
./scripts/dev_setup.sh
```


## Installation
To use in a project, add this in dependencies in pyproject.toml:

```
"pyproresult @ git+ssh://git@github.com/asterisk-digital/pyproresult.git@main"
```

## APIClient

This class is used to interface with Proresult's API properly.

### Usage

```(python)
import pyproresult

api_client = pyproresult.APIClient(api_key="YOUR_API_KEY")
```

## WebClient

This class is used to interface with Proresult's web interface, to enable things like document upload.

### Usage

```(python)
import pyproresult

web_client = pyproresult.WebClient(api_key="YOUR_API_KEY")
```
