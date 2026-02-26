#!/bin/zsh
set -euo pipefail

BREW_PYTHON="$(brew --prefix)/bin/python3"

if [[ ! -x "${BREW_PYTHON}" ]]; then
  echo "Homebrew python3 not found at ${BREW_PYTHON}."
  echo "Install with: brew install python"
  exit 1
fi

exec "${BREW_PYTHON}" math_sprint.py
