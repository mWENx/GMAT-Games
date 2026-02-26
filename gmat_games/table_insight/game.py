"""Table Insight — game loop, tiers 1–3."""

import random
import re
import sys
import time

from ..shared import close_enough, parse_last_number
from .themes import HIDDEN, THEME_MAKERS, display_table, generate_table
from .questions import TIER_QTYPES, pick_question

QUESTIONS_PER_TIER = 8
PASS_THRESHOLD = 0.70


def _normalize(s):
    """Normalize text for case/punctuation-insensitive comparison."""
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def _prompt(question_text):
    """Display question, read input. Returns (raw, elapsed). Exits on 'q'."""
    try:
        print(f"         {question_text}")
        t0 = time.time()
        raw = input("           > ").strip()
        elapsed = time.time() - t0
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        sys.exit(0)
    if raw.lower() in ("q", "quit", "exit"):
        print("\nGoodbye!")
        sys.exit(0)
    return raw, elapsed


def _grade(raw, question):
    """Return True if the user's answer is correct."""
    if question["answer_type"] == "numeric":
        val = parse_last_number(raw)
        return val is not None and close_enough(val, question["answer"])
    return _normalize(raw) == _normalize(str(question["answer"]))


def play_tier(tier: int) -> tuple[int, float]:
    table = generate_table(random.choice(THEME_MAKERS), tier)
    second_table = generate_table(random.choice(THEME_MAKERS), tier) if tier == 3 else None

    print(f"\n{'═' * 60}")
    print(f"  TIER {tier}  —  {table['theme']}")
    print(f"{'═' * 60}")
    print(f"  {QUESTIONS_PER_TIER} questions.  Type 'q' to quit.\n")
    display_table(table)

    correct, total_time = 0, 0.0
    current = table

    for i in range(1, QUESTIONS_PER_TIER + 1):
        if tier == 3 and i == 5 and second_table:
            current = second_table
            print(f"\n  — New table: {current['theme']} —\n")
            display_table(current)

        q           = pick_question(current, TIER_QTYPES[tier])
        hidden_cell = q.get("hidden_cell")

        if hidden_cell:
            r, c = hidden_cell
            saved = current["rows"][r][c]
            current["rows"][r][c] = HIDDEN
            print(f"  [{i:2d}/{QUESTIONS_PER_TIER}]  (Table updated — missing value shown as ?)")
            display_table(current)
        else:
            print(f"  [{i:2d}/{QUESTIONS_PER_TIER}]  ", end="")

        try:
            raw, elapsed = _prompt(q["text"])
        finally:
            if hidden_cell:
                current["rows"][r][c] = saved

        ok = _grade(raw, q)
        total_time += elapsed
        if ok:
            correct += 1
            print(f"           ✓  ({elapsed:.1f}s)")
        else:
            print(f"           ✗  → {q['display_ans']}  ({elapsed:.1f}s)")

    avg = total_time / QUESTIONS_PER_TIER
    pct = correct / QUESTIONS_PER_TIER * 100
    print(f"\n  {'★' * correct}{'☆' * (QUESTIONS_PER_TIER - correct)}")
    print(f"  Score: {correct}/{QUESTIONS_PER_TIER} ({pct:.0f}%)  |  Avg: {avg:.1f}s/question")
    return correct, total_time


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║           TABLE INSIGHT  —  Data Insights Practice       ║
║                      GMAT Practice                       ║
╚══════════════════════════════════════════════════════════╝

  A data table is displayed before each set of questions.
  Answer based on the table — no outside knowledge needed.
  Type 'q' at any prompt to quit.
""")

    while True:
        raw = input("  Start at tier [1 / 2 / 3]: ").strip()
        if raw in ("1", "2", "3"):
            start_tier = int(raw)
            break
        if raw.lower() in ("q", "quit", "exit"):
            print("\nGoodbye!")
            sys.exit(0)
        print("  Please enter 1, 2, or 3.")

    grand_correct, grand_total, grand_time = 0, 0, 0.0
    tier = start_tier
    while tier <= 3:
        c, t = play_tier(tier)
        grand_correct += c
        grand_total   += QUESTIONS_PER_TIER
        grand_time    += t
        pct = c / QUESTIONS_PER_TIER

        if tier < 3:
            if pct >= PASS_THRESHOLD:
                print(f"\n  Passed! Ready for Tier {tier + 1}.")
                if input(f"  Continue to Tier {tier + 1}? [Y/n] ").strip().lower() in ("n", "no"):
                    break
                tier += 1
            else:
                print(f"\n  Score below {int(PASS_THRESHOLD * 100)}% — keep practicing Tier {tier}.")
                if input(f"  Retry Tier {tier}? [Y/n] ").strip().lower() in ("n", "no"):
                    break
        else:
            tier += 1

    overall_pct = grand_correct / grand_total * 100 if grand_total else 0
    avg_overall = grand_time / grand_total if grand_total else 0
    print(f"""
{'═' * 60}
  GAME OVER
  Total score : {grand_correct}/{grand_total} ({overall_pct:.0f}%)
  Total time  : {grand_time:.1f}s  |  Avg: {avg_overall:.1f}s/question
{'═' * 60}
""")
