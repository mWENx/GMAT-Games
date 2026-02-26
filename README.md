# GMAT Games

Command-line GMAT practice tools — mental math and data insights.

## Requirements

- Python 3 (no external packages)

## Run

```bash
python3 -m gmat_games
```

Or via the shell launcher:

```bash
./run_math_sprint.sh
```

## Games

### Math Sprint — Mental Arithmetic (levels 1–5)

Answer arithmetic expressions as fast as possible.

- 10 questions per level, 70% to advance
- Type `q` to quit at any prompt
- Input parser grades on the **last number** typed (`12 + 12 = 24` → graded as `24`)

| Level | Description |
|---|---|
| 1 | + and − chains (integers or decimals) |
| 2 | additive chains with embedded × or ÷ (PEMDAS applies) |
| 3 | longer mixed arithmetic, larger numbers, optional negatives |
| 4 | mean, median, percent-of, percent change |
| 5 | harder mean/median, weighted mean, reverse/chained percent |

### Table Insight — Data Insights (tiers 1–3)

A data table is displayed; answer GMAT-style questions about it.

- 8 questions per tier, 70% to advance
- 4 rotating themes: City Economic Data, Student Scores, Regional Sales, Product Inventory
- Numeric answers graded within 0.5% tolerance
- Text answers are case- and punctuation-insensitive

| Tier | Question types |
|---|---|
| 1 | stat (median / mean / range), conditional count, percentage |
| 2 | + missing value, conditional mean, ranking |
| 3 | + cross-category median, comparison; two tables per round |

## Project Structure

```
gmat_games/
    __main__.py        Entry point (python3 -m gmat_games)
    shared.py          Shared utilities

    math_sprint/
        engine.py      Term factories, generators, LEVELS dict
        game.py        Game loop

    table_insight/
        themes.py      Table generators and display
        questions.py   Question generators
        game.py        Game loop
```
