#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Activate venv
if [ ! -d ".venv" ]; then
  echo "❌ .venv not found. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

source .venv/bin/activate

cmd="${1:-help}"

case "$cmd" in
  setup)
    python --version
    pip install -U pip
    pip install -r requirements.txt
    echo "✅ Setup complete."
    ;;
  notebook)
    python --version
    jupyter notebook
    ;;
  model)
    python --version
    python -m src.main
    ;;
  test)
    python --version
    pytest -q
    ;;
  help|*)
    echo "Usage:"
    echo "  ./run.sh setup     # install dependencies from requirements.txt"
    echo "  ./run.sh notebook  # launch Jupyter"
    echo "  ./run.sh model     # run the risk model (src/main.py)"
    echo "  ./run.sh test      # run tests"
    ;;
esac

