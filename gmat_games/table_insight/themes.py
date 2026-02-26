"""Table Insight — data table generation and display."""

import random

# Sentinel placed into a cell for missing-value questions.
# All modules that test `val is HIDDEN` must import from here.
HIDDEN = object()


# ─── Cell / column helpers ────────────────────────────────────────────────────

def fmt_cell(val, decimals=1):
    """Format a cell value; add commas for large ints (>=10000)."""
    if val is HIDDEN:
        return "?"
    if isinstance(val, int):
        return f"{val:,}" if val >= 10_000 else str(val)
    if isinstance(val, float):
        if val >= 10_000 and val.is_integer():
            return f"{int(val):,}"
        return f"{val:.{decimals}f}"
    return str(val)


def col_values(table, col_idx):
    """Return all values in a column (may include HIDDEN)."""
    return [row[col_idx] for row in table["rows"]]


def numeric_col_values(table, col_idx):
    """Return only the numeric (non-HIDDEN) values in a column."""
    return [v for v in col_values(table, col_idx) if v is not HIDDEN]


# ─── Display ──────────────────────────────────────────────────────────────────

def display_table(table):
    """Print a fixed-width table: label column left-aligned, numbers right-aligned."""
    headers, rows, label_col = table["headers"], table["rows"], table["label_col"]

    grid = []
    for row in rows:
        grid.append([
            (str(val) if val is not HIDDEN else "?") if c == label_col else fmt_cell(val, table["decimals"][c])
            for c, val in enumerate(row)
        ])

    widths = [max(len(h), max(len(r[c]) for r in grid)) for c, h in enumerate(headers)]
    sep = "  " + "─" * (sum(widths) + 3 * (len(widths) - 1) + 4)

    def _row(cells):
        parts = [c.ljust(w) if i == label_col else c.rjust(w) for i, (c, w) in enumerate(zip(cells, widths))]
        return "  | " + "   ".join(parts) + " |"

    print(sep)
    print(_row(headers))
    print(sep)
    for row in grid:
        print(_row(row))
    print(sep)
    print()


# ─── Theme generators ─────────────────────────────────────────────────────────

def _make_city_table(n_rows):
    cities = random.sample([
        "Austin", "Denver", "Nashville", "Portland", "Raleigh",
        "Phoenix", "Atlanta", "Charlotte", "Minneapolis", "Salt Lake City",
        "Columbus", "Indianapolis", "Kansas City", "Louisville", "Richmond",
    ], n_rows)
    return {
        "theme":    "City Economic Data",
        "headers":  ["City", "Population (K)", "GDP ($B)", "Unemp. %", "Med. Income ($K)"],
        "rows":     [[c, random.randint(300, 2500), round(random.uniform(20, 200), 1),
                      round(random.uniform(2.0, 8.5), 1), random.randint(45, 95)] for c in cities],
        "label_col": 0,
        "decimals": [0, 0, 1, 1, 0],
    }


def _make_student_table(n_rows):
    names = random.sample([
        "Alice", "Ben", "Clara", "David", "Elena", "Fiona",
        "George", "Hana", "Ivan", "Julia", "Kevin", "Layla",
    ], n_rows)
    return {
        "theme":    "Student Scores",
        "headers":  ["Student", "Math", "English", "Science", "History"],
        "rows":     [[n, random.randint(55, 99), random.randint(55, 99),
                      random.randint(55, 99), random.randint(55, 99)] for n in names],
        "label_col": 0,
        "decimals": [0, 0, 0, 0, 0],
    }


def _make_sales_table(n_rows):
    regions = random.sample([
        "Northeast", "Southeast", "Midwest", "Southwest", "West",
        "Mid-Atlantic", "Pacific Northwest", "Great Plains",
    ], n_rows)
    return {
        "theme":    "Regional Sales",
        "headers":  ["Region", "Q1 ($K)", "Q2 ($K)", "Q3 ($K)", "Q4 ($K)"],
        "rows":     [[r, random.randint(80, 600), random.randint(80, 600),
                      random.randint(80, 600), random.randint(80, 600)] for r in regions],
        "label_col": 0,
        "decimals": [0, 0, 0, 0, 0],
    }


def _make_product_table(n_rows):
    products = random.sample([
        "Widget A", "Widget B", "Gadget X", "Gadget Y", "Gizmo Pro",
        "Gizmo Lite", "Module 1", "Module 2", "Component Z", "Device Plus",
        "Pack Standard", "Pack Deluxe",
    ], n_rows)
    return {
        "theme":    "Product Inventory",
        "headers":  ["Product", "Units Sold", "Revenue ($K)", "Return Rate %", "Cust. Rating"],
        "rows":     [[p, random.randint(200, 5000), random.randint(50, 800),
                      round(random.uniform(0.5, 12.0), 1), round(random.uniform(3.0, 5.0), 1)] for p in products],
        "label_col": 0,
        "decimals": [0, 0, 0, 1, 1],
    }


THEME_MAKERS = [_make_city_table, _make_student_table, _make_sales_table, _make_product_table]


def generate_table(theme_maker, tier):
    """Generate a table for the given theme and tier (tier 3 → max rows)."""
    if theme_maker is _make_sales_table:
        n_rows = random.randint(4, 6) if tier == 3 else min(random.randint(6, 7), 5)
    else:
        n_rows = 8 if tier == 3 else random.randint(6, 7)
    return theme_maker(n_rows)
