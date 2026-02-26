#!/bin/zsh
set -euo pipefail

if command -v python3 >/dev/null 2>&1; then
  exec python3 -m gmat_games
fi

if command -v python >/dev/null 2>&1; then
  exec python -m gmat_games
fi

echo "Python not found. Please install Python 3."
exit 1
