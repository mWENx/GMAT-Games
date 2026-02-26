"""Entry point: python3 -m gmat_games"""

import sys

from gmat_games.math_sprint import main as math_sprint_main
from gmat_games.table_insight import main as table_insight_main

BANNER = """
╔══════════════════════════════════════════════════════════╗
║                    GMAT  GAMES                           ║
║              Command-line practice tools                 ║
╚══════════════════════════════════════════════════════════╝

  1 — Math Sprint    Mental arithmetic (levels 1–5)
  2 — Table Insight  Data Insights / table reading (tiers 1–3)
  q — Quit
"""

GAMES = {"1": math_sprint_main, "2": table_insight_main}


def main():
    print(BANNER)
    while True:
        try:
            raw = input("  Choose a game [1 / 2]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)
        if raw in ("q", "quit", "exit"):
            print("\nGoodbye!")
            sys.exit(0)
        if raw in GAMES:
            GAMES[raw]()
            print(BANNER)
        else:
            print("  Please enter 1 or 2.")


if __name__ == "__main__":
    main()
