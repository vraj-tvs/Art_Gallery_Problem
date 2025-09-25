#!/usr/bin/env bash
set -euo pipefail

# Setup script: creates a virtualenv, installs requirements, and runs main.py

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
VENV_PATH="$REPO_ROOT/.venv"

python3 -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

pip install --upgrade pip >/dev/null
pip install -r "$REPO_ROOT/requirements.txt"

cd "$REPO_ROOT"

exec python3 "$REPO_ROOT/main.py"


