#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Activate venv
source .venv/bin/activate

cmd="${1:-notebook}"

case "$cmd" in
  setup)
    pip install -U pip
    pip install -r requirements.txt
    ;;
  notebook)
    python --version
    jupyter notebook
    ;;
  model)
    python --version
    python -m src.main
    ;;
  *)
    echo "Usage: ./run.sh {setup|notebook|model}"
    exit 1
    ;;
esac

