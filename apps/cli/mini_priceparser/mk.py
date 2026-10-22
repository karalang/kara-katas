#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated <num>\t<decsep>.

<num> is a raw number string as price-parser's parse_number receives it after
currency and surrounding text have been stripped; <decsep> is the explicit
decimal separator to force (`-` for None = guess it). The set covers the
thousand/decimal guessing heuristic (the 1/2/>=4-digit rule), all four
separator modes, the euro-as-decimal-separator case, forced separators, and
the invalid inputs that return None.
"""
import os

JOBS = [
    ("1,234", "-"),
    ("12,34", "-"),
    ("12,345", "-"),
    ("1,1", "-"),
    ("1.1", "-"),
    ("1234", "-"),
    ("12.99", "-"),
    ("12.999", "-"),
    ("3,0000", "-"),
    (".75", "-"),
    ("12.50", "-"),
    ("12€34", "-"),
    ("12€ 34", "-"),
    ("1 234.99", "-"),
    ("1,235€99", "-"),
    ("1 235€99", "-"),
    ("1.235€99", "-"),
    ("1,234,567", "-"),
    ("1.234.567,89", "-"),
    ("1 000 000", "-"),
    ("007", "-"),
    ("0", "-"),
    ("1.000", "-"),
    ("140.000", ","),
    ("140.000", "."),
    ("1.000", "."),
    ("1.000", ","),
    ("12,34", "€"),
    ("", "-"),
    ("foo", "-"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for num, dec in JOBS:
        fh.write(num + "\t" + dec + "\n")
print("wrote data/jobs.tsv:", len(JOBS), "jobs")
