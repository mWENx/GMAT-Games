# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the game

```bash
python3 math_sprint.py
```

No dependencies beyond the Python standard library.

## Architecture

Everything lives in `math_sprint.py` — a single-file CLI game with no external dependencies.

### Term factories

Four helpers, each returning `(display_str, py_eval_str)`:

| Factory | Description |
|---|---|
| `t_int(lo, hi)` | Plain integer in `[lo, hi]` |
| `t_decimal()` | 2–3 sig-fig decimal (1 or 2 decimal places) |
| `t_product(max_a, max_b)` | `"a × b"` → `"(a*b)"` |
| `t_quotient(max_div, max_q)` | `"a ÷ b"` → `"(a/b)"`, integer result guaranteed |

`t_quotient` always multiplies `divisor × quotient` to produce the numerator, so the result is always a clean integer.

### Chain builder

`build_chain(terms, ops)` takes a list of term-factory outputs and a list of `"+"` / `"-"` operators, assembles the display string (using Unicode `−`) and a Python eval string, then returns `(expr_str, float_answer)`.

### Level generators

Each generator calls factories and `build_chain`:

- **`gen_l1()`** — 3–4 terms; all `t_int(10, 999)` or all `t_decimal()`; ops: + and − only
- **`gen_l2()`** — 3–4 terms; `t_int` plain terms + one guaranteed `t_product(25,12)` or `t_quotient(20,30)` at a random position; outer ops: + and −
- **`gen_l3()`** — 4–5 terms; `t_int(10,9999)`, `t_product(99,25)`, `t_quotient(25,100)`, occasional `t_decimal()`; optional negative leading term (plain integers only)

**Answer tolerance** (`close_enough`): `max(0.01, abs(correct) * 0.005)` — 0.5% relative or 0.01 absolute, whichever is larger.

**Game loop** (`main` → `play_level`): `while level <= 3` loop with inline retry/advance prompts. `play_level` returns `(correct_count, total_seconds)` which accumulates into grand totals printed at exit.

**Key constants** to tune difficulty: `QUESTIONS_PER_LEVEL` (default 10), `PASS_THRESHOLD` (default 0.70).

## Adding a new level or question style

1. Write a `gen_lN()` function using term factories + `build_chain`, returning `(expr: str, answer: float)`.
2. Add an entry to the `LEVELS` dict with `"gen"` and `"desc"` keys.
3. Extend the `while level <= 3` loop bound in `main()`.
