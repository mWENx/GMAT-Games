"""Table Insight — question generators for all 8 question types."""

import random

from ..shared import fmt, mean_of, median_of
from .themes import HIDDEN, col_values, fmt_cell, numeric_col_values

TIER_QTYPES = {
    1: [1, 3, 7],
    2: [1, 2, 3, 4, 5, 7],
    3: [1, 2, 3, 4, 5, 6, 7, 8],
}


def _numeric_cols(table):
    return [c for c in range(len(table["headers"])) if c != table["label_col"]]


# ─── Question generators ──────────────────────────────────────────────────────
# Each returns a Question dict or raises ValueError if the table can't support it.
#
# Question dict:  text, answer, answer_type ("numeric"|"text"), display_ans
#                 optional hidden_cell: (row_idx, col_idx)


def qgen_stat(table):
    """Type 1 — median / mean / range of a numeric column."""
    col_idx  = random.choice(_numeric_cols(table))
    col_name = table["headers"][col_idx]
    vals     = numeric_col_values(table, col_idx)
    stat     = random.choice(["median", "mean", "range"])

    if stat == "median":
        ans  = median_of(vals)
        text = f"What is the median of {col_name}?"
    elif stat == "mean":
        ans  = round(mean_of(vals), 1)
        text = f"What is the mean of {col_name}? (round to 1 decimal)"
    else:
        ans  = float(max(vals) - min(vals))
        text = f"What is the range of {col_name}?"

    return {"text": text, "answer": float(ans), "answer_type": "numeric", "display_ans": fmt(round(ans, 2))}


def qgen_missing_value(table):
    """Type 2 — which value restores the column mean after one cell is hidden."""
    col_idx = random.choice(_numeric_cols(table))
    r       = random.randrange(len(table["rows"]))
    if table["rows"][r][col_idx] is HIDDEN:
        raise ValueError("cell already hidden")

    all_vals  = numeric_col_values(table, col_idx)
    true_mean = mean_of(all_vals)
    ans       = true_mean * len(all_vals) - sum(v for i, v in enumerate(all_vals) if i != r)
    label     = table["rows"][r][table["label_col"]]
    text      = (
        f"The mean of {table['headers'][col_idx]} is {fmt(round(true_mean, 2))}. "
        f"The value for '{label}' is missing (?). What is the missing value?"
    )
    return {
        "text": text, "answer": float(round(ans, 4)), "answer_type": "numeric",
        "display_ans": fmt(round(ans, 2)), "hidden_cell": (r, col_idx),
    }


def qgen_conditional_count(table):
    """Type 3 — count rows where col > 25th / 50th / 75th percentile threshold."""
    col_idx = random.choice(_numeric_cols(table))
    vals    = numeric_col_values(table, col_idx)
    s       = sorted(vals)
    pctile  = random.choice([25, 50, 75])
    thresh  = s[max(0, min(int(len(s) * pctile / 100), len(s) - 1))]
    count   = sum(1 for v in vals if v > thresh)
    if count == 0 or count == len(vals):
        raise ValueError("degenerate count")
    dec = table["decimals"][col_idx]
    return {
        "text": f"How many rows have {table['headers'][col_idx]} > {fmt_cell(thresh, dec)}?",
        "answer": float(count), "answer_type": "numeric", "display_ans": str(count),
    }


def qgen_conditional_mean(table):
    """Type 4 — mean of col_X for rows where col_Y > its median."""
    num_cols = _numeric_cols(table)
    if len(num_cols) < 2:
        raise ValueError("not enough numeric columns")
    col_y, col_x = random.sample(num_cols, 2)
    thresh  = median_of(numeric_col_values(table, col_y))
    subset  = [row[col_x] for row in table["rows"]
               if row[col_y] is not HIDDEN and row[col_y] > thresh and row[col_x] is not HIDDEN]
    if len(subset) < 2:
        raise ValueError("subset too small")
    ans  = round(mean_of(subset), 1)
    dec  = table["decimals"][col_y]
    text = (f"What is the mean of {table['headers'][col_x]} for rows where "
            f"{table['headers'][col_y]} > {fmt_cell(thresh, dec)}? (round to 1 decimal)")
    return {"text": text, "answer": float(ans), "answer_type": "numeric", "display_ans": fmt(ans)}


def qgen_ranking(table):
    """Type 5 — which label has the highest / lowest value in a column."""
    col_idx   = random.choice(_numeric_cols(table))
    direction = random.choice(["highest", "lowest"])
    candidates = [(row[col_idx], row[table["label_col"]]) for row in table["rows"] if row[col_idx] is not HIDDEN]
    fn    = max if direction == "highest" else min
    label = fn(candidates, key=lambda x: x[0])[1]
    text  = f"Which {table['headers'][table['label_col']]} has the {direction} {table['headers'][col_idx]}?"
    return {"text": text, "answer": label, "answer_type": "text", "display_ans": label}


def qgen_cross_category_median(table):
    """Type 6 — median of a column for the first-half or second-half row subset."""
    col_idx     = random.choice(_numeric_cols(table))
    rows        = table["rows"]
    mid         = len(rows) // 2
    subset_rows = rows[:mid] if random.choice(["first", "second"]) == "first" else rows[mid:]
    vals        = [r[col_idx] for r in subset_rows if r[col_idx] is not HIDDEN]
    if len(vals) < 2:
        raise ValueError("subset too small")
    ans        = median_of(vals)
    label_list = ", ".join(r[table["label_col"]] for r in subset_rows)
    return {
        "text": f"What is the median of {table['headers'][col_idx]} for: {label_list}?",
        "answer": float(round(ans, 4)), "answer_type": "numeric", "display_ans": fmt(round(ans, 2)),
    }


def qgen_percentage(table):
    """Type 7 — percentage of rows with col above the column mean."""
    col_idx = random.choice(_numeric_cols(table))
    vals    = numeric_col_values(table, col_idx)
    thresh  = mean_of(vals)
    pct     = round(sum(1 for v in vals if v > thresh) / len(vals) * 100, 1)
    if pct == 0 or pct == 100:
        raise ValueError("degenerate percentage")
    dec  = table["decimals"][col_idx]
    text = (f"What percentage of rows have {table['headers'][col_idx]} above the column mean of "
            f"{fmt_cell(thresh, dec)}? (give answer as a number, e.g. 50 for 50%)")
    return {"text": text, "answer": float(pct), "answer_type": "numeric", "display_ans": f"{fmt(pct)}%"}


def qgen_comparison(table):
    """Type 8 — which stat (median or mean) is higher: col_A or col_B?"""
    num_cols = _numeric_cols(table)
    if len(num_cols) < 2:
        raise ValueError("not enough numeric columns")
    col_a, col_b = random.sample(num_cols, 2)
    stat = random.choice(["median", "mean"])
    fn   = median_of if stat == "median" else mean_of
    va, vb = fn(numeric_col_values(table, col_a)), fn(numeric_col_values(table, col_b))
    if abs(va - vb) < 0.001:
        raise ValueError("too close to call")
    label = table["headers"][col_a] if va > vb else table["headers"][col_b]
    text  = f"Which is higher: the {stat} of {table['headers'][col_a]} or the {stat} of {table['headers'][col_b]}?"
    return {"text": text, "answer": label, "answer_type": "text", "display_ans": label}


# ─── Dispatcher ───────────────────────────────────────────────────────────────

QGEN_MAP = {
    1: qgen_stat, 2: qgen_missing_value, 3: qgen_conditional_count,
    4: qgen_conditional_mean, 5: qgen_ranking, 6: qgen_cross_category_median,
    7: qgen_percentage, 8: qgen_comparison,
}


def pick_question(table, allowed_types):
    """Try each allowed type in random order; fall back to stat after 20 attempts."""
    for qtype in random.sample(allowed_types, len(allowed_types)):
        try:
            return QGEN_MAP[qtype](table)
        except (ValueError, IndexError):
            continue
    for _ in range(20):
        try:
            return qgen_stat(table)
        except (ValueError, IndexError):
            continue
    raise RuntimeError("Could not generate any question for this table.")
