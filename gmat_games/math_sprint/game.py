"""Math Sprint — game loop, levels 1–5."""

import sys
import time

from ..shared import close_enough, fmt, parse_last_number
from .engine import LEVELS

QUESTIONS_PER_LEVEL = 10
PASS_THRESHOLD = 0.70


def _prompt(expr, answer):
    """Show expression, read input. Returns (correct, elapsed). Exits on 'q'."""
    try:
        t0 = time.time()
        raw = input(f"  {expr} = ? ").strip()
        elapsed = time.time() - t0
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        sys.exit(0)

    if raw.lower() in ("q", "quit", "exit"):
        print("\nGoodbye!")
        sys.exit(0)

    val = parse_last_number(raw)
    return (close_enough(val, answer) if val is not None else False), elapsed


def play_level(level: int) -> tuple[int, float]:
    gen  = LEVELS[level]["gen"]
    desc = LEVELS[level]["desc"]
    correct, total_time = 0, 0.0

    print(f"\n{'═' * 57}")
    print(f"  LEVEL {level}  —  {desc}")
    print(f"{'═' * 57}")
    print(f"  {QUESTIONS_PER_LEVEL} questions.  Type 'q' to quit.\n")

    for i in range(1, QUESTIONS_PER_LEVEL + 1):
        expr, ans = gen()
        print(f"  [{i:2d}/{QUESTIONS_PER_LEVEL}]  ", end="", flush=True)
        ok, elapsed = _prompt(expr, ans)
        total_time += elapsed
        if ok:
            correct += 1
            print(f"           ✓  ({elapsed:.1f}s)")
        else:
            print(f"           ✗  → {fmt(round(ans, 4))}  ({elapsed:.1f}s)")

    avg = total_time / QUESTIONS_PER_LEVEL
    pct = correct / QUESTIONS_PER_LEVEL * 100
    print(f"\n  {'★' * correct}{'☆' * (QUESTIONS_PER_LEVEL - correct)}")
    print(f"  Score: {correct}/{QUESTIONS_PER_LEVEL} ({pct:.0f}%)  |  Avg: {avg:.1f}s/question")
    return correct, total_time


def main():
    print("""
╔═════════════════════════════════════════════════════╗
║              MATH SPRINT  —  Mental Math            ║
║                   GMAT Practice                     ║
╚═════════════════════════════════════════════════════╝

  Answer each expression as fast as you can.
  Order of operations applies: × and ÷ before + and −.
  Decimals: answer to 2 decimal places is fine.
  Type 'q' at any prompt to quit.
""")

    while True:
        raw = input("  Start at level [1 / 2 / 3 / 4 / 5]: ").strip()
        if raw in ("1", "2", "3", "4", "5"):
            start_level = int(raw)
            break
        if raw.lower() in ("q", "quit", "exit"):
            print("\nGoodbye!")
            sys.exit(0)
        print("  Please enter 1, 2, 3, 4, or 5.")

    grand_correct, grand_total, grand_time = 0, 0, 0.0
    level = start_level
    while level <= 5:
        c, t = play_level(level)
        grand_correct += c
        grand_total   += QUESTIONS_PER_LEVEL
        grand_time    += t
        pct = c / QUESTIONS_PER_LEVEL

        if level < 5:
            if pct >= PASS_THRESHOLD:
                print(f"\n  Passed! Ready for Level {level + 1}.")
                if input(f"  Continue to Level {level + 1}? [Y/n] ").strip().lower() in ("n", "no"):
                    break
                level += 1
            else:
                print(f"\n  Score below {int(PASS_THRESHOLD*100)}% — keep practicing Level {level}.")
                if input(f"  Retry Level {level}? [Y/n] ").strip().lower() in ("n", "no"):
                    break
        else:
            level += 1

    overall_pct = grand_correct / grand_total * 100 if grand_total else 0
    avg_overall = grand_time / grand_total if grand_total else 0
    print(f"""
{'═' * 57}
  GAME OVER
  Total score : {grand_correct}/{grand_total} ({overall_pct:.0f}%)
  Total time  : {grand_time:.1f}s  |  Avg: {avg_overall:.1f}s/question
{'═' * 57}
""")
