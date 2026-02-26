"""Math Sprint — arithmetic term factories and level generators."""

import random

from ..shared import fmt


# ─── Term factories ───────────────────────────────────────────────────────────
# Each factory returns (display_str, py_eval_str).

def t_int(lo, hi):
    n = random.randint(lo, hi)
    return str(n), str(n)


def t_decimal():
    if random.random() < 0.5:
        n = round(random.uniform(1.0, 99.9), 1)
    else:
        n = round(random.uniform(0.10, 9.99), 2)
    s = fmt(n)
    return s, s


def t_product(max_a, max_b):
    a = random.randint(2, max_a)
    b = random.randint(2, max_b)
    return f"{a} × {b}", f"({a}*{b})"


def t_quotient(max_div, max_q):
    b = random.randint(2, max_div)
    q = random.randint(2, max_q)
    a = b * q
    return f"{a} ÷ {b}", f"({a}/{b})"


# ─── Chain builder ────────────────────────────────────────────────────────────

def build_chain(terms, ops):
    """Assemble an additive chain from term-factory output."""
    display_parts = [terms[0][0]]
    py_parts = [terms[0][1]]
    for op, term in zip(ops, terms[1:]):
        display_parts.append("−" if op == "-" else "+")
        display_parts.append(term[0])
        py_parts.append(op)
        py_parts.append(term[1])
    expr = " ".join(display_parts)
    ans = eval(" ".join(py_parts))
    return expr, round(ans, 8)


# ─── Level generators ─────────────────────────────────────────────────────────

def gen_l1():
    n = random.randint(3, 4)
    ops = [random.choice(["+", "-"]) for _ in range(n - 1)]
    if random.random() < 0.45:
        terms = [t_decimal() for _ in range(n)]
    else:
        terms = [t_int(10, 999) for _ in range(n)]
    return build_chain(terms, ops)


def gen_l2():
    n = random.randint(3, 4)
    ops = [random.choice(["+", "-"]) for _ in range(n - 1)]
    mult_idx = random.randrange(n)
    terms = []
    for i in range(n):
        if i == mult_idx:
            terms.append(t_product(25, 12) if random.random() < 0.5 else t_quotient(20, 30))
        else:
            terms.append(t_int(10, 999))
    return build_chain(terms, ops)


def gen_l3():
    n = random.randint(4, 5)
    ops = [random.choice(["+", "-"]) for _ in range(n - 1)]
    mult_idx = random.randrange(n)
    terms = []
    for i in range(n):
        if i == mult_idx:
            terms.append(t_product(99, 25) if random.random() < 0.5 else t_quotient(25, 100))
        elif random.random() < 0.20:
            terms.append(t_decimal())
        else:
            terms.append(t_int(10, 9999))
    if random.random() < 0.30:
        d, p = terms[0]
        if "×" not in d and "÷" not in d:
            terms[0] = (f"−{d}", f"(-{p})")
    return build_chain(terms, ops)


# ─── Stat / percent helpers ───────────────────────────────────────────────────

def q_mean(lo, hi, n):
    vals = [random.randint(lo, hi) for _ in range(n)]
    return f"mean({', '.join(map(str, vals))})", round(sum(vals) / n, 8)


def q_median(lo, hi, n):
    vals = [random.randint(lo, hi) for _ in range(n)]
    s = sorted(vals)
    mid = n // 2
    ans = s[mid] if n % 2 == 1 else (s[mid - 1] + s[mid]) / 2
    return f"median({', '.join(map(str, vals))})", round(ans, 8)


def q_percent_of(num_lo, num_hi, pct_lo, pct_hi):
    base = random.randint(num_lo, num_hi)
    pct = random.choice([5, 10, 12, 15, 20, 25, 30, 40, 50]) if pct_lo == 0 else random.randint(pct_lo, pct_hi)
    return f"{pct}% of {base}", round(base * pct / 100, 8)


def q_percent_change(lo, hi, max_delta):
    start = random.randint(lo, hi)
    delta = random.randint(5, max_delta)
    if random.random() < 0.5:
        return f"{start} increased by {delta}%", round(start * (1 + delta / 100), 8)
    return f"{start} decreased by {delta}%", round(start * (1 - delta / 100), 8)


def gen_l4():
    kind = random.choice(["mean", "median", "percent_of", "percent_change"])
    if kind == "mean":
        return q_mean(10, 120, random.randint(4, 6))
    if kind == "median":
        return q_median(10, 120, random.choice([5, 7]))
    if kind == "percent_of":
        return q_percent_of(40, 400, 0, 0)
    return q_percent_change(40, 400, 30)


def q_weighted_mean():
    a, b = random.randint(40, 98), random.randint(40, 98)
    wa, wb = random.randint(2, 6), random.randint(2, 6)
    return f"weighted mean: {a} (weight {wa}), {b} (weight {wb})", round((a*wa + b*wb) / (wa+wb), 8)


def q_reverse_percent():
    pct = random.choice([10, 15, 20, 25, 30, 40])
    original = random.randint(80, 900)
    increased = original * (1 + pct / 100)
    return f"if x increased by {pct}% is {fmt(increased)}, find x", round(original, 8)


def q_percent_chain():
    base = random.randint(100, 800)
    up = random.choice([10, 15, 20, 25, 30])
    down = random.choice([5, 10, 15, 20, 25])
    return f"{base} increased by {up}%, then decreased by {down}%", round(base * (1 + up/100) * (1 - down/100), 8)


def gen_l5():
    kind = random.choice(["mean", "median_even", "weighted_mean", "reverse_percent", "percent_chain"])
    if kind == "mean":
        return q_mean(20, 300, random.randint(5, 8))
    if kind == "median_even":
        return q_median(20, 300, random.choice([6, 8]))
    if kind == "weighted_mean":
        return q_weighted_mean()
    if kind == "reverse_percent":
        return q_reverse_percent()
    return q_percent_chain()


# ─── Level registry ───────────────────────────────────────────────────────────

LEVELS = {
    1: {"gen": gen_l1, "desc": "3–4 terms  |  + and −  |  integers or decimals"},
    2: {"gen": gen_l2, "desc": "3–4 terms  |  + − with × ÷ embedded  |  PEMDAS applies"},
    3: {"gen": gen_l3, "desc": "4–5 terms  |  + − × ÷  |  larger numbers, optional negatives"},
    4: {"gen": gen_l4, "desc": "mean, median, and percent-of/change problems"},
    5: {"gen": gen_l5, "desc": "harder mean/median plus multi-step and reverse percent"},
}
