"""Shared utility functions used across all games."""

import re


def fmt(n):
    """Format a number cleanly (no trailing .0)."""
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    if isinstance(n, float):
        return f"{n:.6f}".rstrip("0").rstrip(".")
    return str(n)


def close_enough(user, correct):
    """Accept answers within 0.5% or 0.01, whichever is larger."""
    threshold = max(0.01, abs(correct) * 0.005)
    return abs(user - correct) <= threshold


def parse_last_number(raw: str):
    """Return the last numeric token in user input, or None if absent."""
    matches = re.findall(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", raw)
    if not matches:
        return None
    try:
        return float(matches[-1])
    except ValueError:
        return None


def median_of(vals):
    """Return the median of a list of numbers."""
    s = sorted(vals)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 == 1 else (s[mid - 1] + s[mid]) / 2


def mean_of(vals):
    """Return the arithmetic mean of a list of numbers."""
    return sum(vals) / len(vals)
