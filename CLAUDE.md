# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running

```bash
python3 -m gmat_games
```

No dependencies beyond the Python standard library.

---

## Package layout

```
gmat_games/
    __init__.py
    __main__.py          ← entry point (python3 -m gmat_games)
    shared.py            ← fmt, close_enough, parse_last_number, median_of, mean_of

    math_sprint/
        __init__.py      ← exposes main()
        engine.py        ← term factories, build_chain, level generators, LEVELS dict
        game.py          ← game loop (levels 1–5)

    table_insight/
        __init__.py      ← exposes main()
        themes.py        ← HIDDEN sentinel, 4 theme generators, display helpers
        questions.py     ← 8 question generators, QGEN_MAP, TIER_QTYPES, pick_question
        game.py          ← game loop (tiers 1–3)
```

### Import graph (no cycles)

```
shared              ← (no project imports)
math_sprint/
  engine            ← ..shared
  game              ← ..shared, .engine
table_insight/
  themes            ← (no project imports)
  questions         ← ..shared, .themes
  game              ← ..shared, .themes, .questions
__main__            ← gmat_games.math_sprint, gmat_games.table_insight
```

Intra-package imports use relative syntax (`from ..shared import fmt`,
`from .themes import HIDDEN`). `__main__.py` uses absolute imports.

---

## shared.py

| Function | Description |
|---|---|
| `fmt(n)` | Format number cleanly (strips trailing `.0`) |
| `close_enough(user, correct)` | 0.5% relative or 0.01 absolute tolerance |
| `parse_last_number(raw)` | Extracts last numeric token from user input |
| `median_of(vals)` | Median of a list |
| `mean_of(vals)` | Arithmetic mean of a list |

---

## Math Sprint (`math_sprint/engine.py` + `game.py`)

### Term factories — each returns `(display_str, py_eval_str)`

| Factory | Description |
|---|---|
| `t_int(lo, hi)` | Plain integer in `[lo, hi]` |
| `t_decimal()` | 2–3 sig-fig decimal |
| `t_product(max_a, max_b)` | `"a × b"` → `"(a*b)"` |
| `t_quotient(max_div, max_q)` | `"a ÷ b"` → `"(a/b)"`, integer result |

### Level generators

| Generator | Description |
|---|---|
| `gen_l1()` | 3–4 terms, + and − only, integers or decimals |
| `gen_l2()` | 3–4 terms, one embedded × or ÷ |
| `gen_l3()` | 4–5 terms, larger numbers, optional negative lead |
| `gen_l4()` | mean / median / percent-of / percent-change |
| `gen_l5()` | harder mean/median, weighted mean, reverse/chained percent |

**LEVELS dict** in `engine.py` maps 1–5 to `{gen, desc}`.

**Config** in `game.py`: `QUESTIONS_PER_LEVEL = 10`, `PASS_THRESHOLD = 0.70`.

### Adding a new level

1. Write `gen_lN()` in `engine.py`.
2. Add entry to `LEVELS`.
3. Extend the `while level <= N` bound in `game.main()`.

---

## Table Insight (`table_insight/themes.py` + `questions.py` + `game.py`)

### Table data model

```python
table = {
    "theme":    str,
    "headers":  [str, ...],
    "rows":     [[val, ...], ...],
    "label_col": 0,
    "decimals": [int, ...],   # display decimal places per column
}
HIDDEN = object()   # sentinel for missing-value questions (defined in themes.py)
```

`HIDDEN` is an `object()` singleton defined once in `themes.py`. All modules that
test `val is HIDDEN` must import it from there — never redefine it.

### Themes

| Theme | Numeric columns |
|---|---|
| City Economic Data | Population (K), GDP ($B), Unemp. %, Med. Income ($K) |
| Student Scores | Math, English, Science, History (55–99) |
| Regional Sales | Q1–Q4 ($K, 80–600) |
| Product Inventory | Units Sold, Revenue ($K), Return Rate %, Cust. Rating |

`generate_table(theme_maker, tier)` — tier 3 → max rows, else 6–7.

### Question types

| # | Name | Answer type | Min tier |
|---|---|---|---|
| 1 | Stat (median / mean / range) | numeric | 1 |
| 2 | Missing value (restore column mean) | numeric | 2 |
| 3 | Conditional count (col > percentile) | numeric | 1 |
| 4 | Conditional mean (col_X where col_Y > median) | numeric | 2 |
| 5 | Ranking (highest / lowest label) | text | 2 |
| 6 | Cross-category median (named row subset) | numeric | 3 |
| 7 | Percentage (% rows above column mean) | numeric | 1 |
| 8 | Comparison (which stat of col_A vs col_B?) | text | 3 |

`pick_question(table, allowed_types)` — tries each type in random order;
falls back to `qgen_stat` after 20 attempts.

**Tier question sets:**
```python
TIER_QTYPES = {1: [1, 3, 7], 2: [1, 2, 3, 4, 5, 7], 3: [1, 2, 3, 4, 5, 6, 7, 8]}
```

**Config** in `game.py`: `QUESTIONS_PER_TIER = 8`, `PASS_THRESHOLD = 0.70`.

Tier 3 uses two tables — second table introduced at question 5.

### Adding a new question type

1. Write `qgen_mytype(table)` in `questions.py`; raise `ValueError` if the table
   data can't produce a valid question.
2. Add to `QGEN_MAP`.
3. Add the key to the relevant tiers in `TIER_QTYPES`.

### Adding a new theme

1. Write `_make_mytheme_table(n_rows)` in `themes.py`.
2. Append to `THEME_MAKERS`.
