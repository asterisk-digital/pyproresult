#!/usr/bin/env bash

set -euxo pipefail

# Script to setup local development environment

cd "$( dirname "${BASH_SOURCE[0]}" )/.."

uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"
