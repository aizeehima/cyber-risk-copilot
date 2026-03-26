#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

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
    if [[ "${2:-}" == "--report" ]]; then
      python -m src.main --report
    else
      python -m src.main
    fi
    ;;
  *)
    echo "Usage: ./run.sh {setup|notebook|model [--report]}"
    exit 1
    ;;
esac
