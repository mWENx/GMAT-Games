# Math Sprint

Command-line mental math practice game with 5 difficulty levels.

## Requirements

- macOS with Homebrew
- Homebrew Python 3

Install Python via Homebrew:

```bash
brew install python
```

## Run

Recommended (forces Homebrew Python):

```bash
./run_math_sprint.sh
```

Alternative:

```bash
/opt/homebrew/bin/python3 math_sprint.py
```

## Gameplay

- Start from any level `1` to `5`
- `10` questions per level
- Need `70%` to advance
- Type `q` to quit
- Input parser grades based on the **last number** in your input
  - Example: `12 + 12 = 24` will be graded as `24`

## Levels

- Level 1: `+` and `-` chains (integers/decimals)
- Level 2: additive chains with embedded `×` or `÷`
- Level 3: longer mixed arithmetic chains
- Level 4: mean, median, percent-of, percent change
- Level 5: harder mean/median + weighted/reverse/multi-step percent

## Project Structure

- `math_sprint.py`: UI/game loop, prompting, scoring, progression
- `math_engine.py`: arithmetic helpers and all question generation logic
- `run_math_sprint.sh`: launcher that uses Homebrew Python
