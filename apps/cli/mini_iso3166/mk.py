#!/usr/bin/env python3
"""Writes data/jobs.tsv: one iso3166 lookup per line, tab-separated.

Columns: op and arg. Ops:
  get <key>        countries.get(str) -> Country repr, or KeyError
  getint <n>       countries.get(int) -> Country repr, or KeyError
  contains <key>   str/int in countries -> True/False
  len              len(countries)

The dispatch quirks are covered: a 2-char key is always alpha-2; a 3-char
all-digit key other than "000" resolves as numeric *before* alpha-3; an int is
zero-padded to three digits; a name miss falls through to apolitical_name.

Keys that reach the name/apolitical index are kept ASCII and apostrophe-free so
the repr uses plain single-quote delimiters with no escaping. The six non-ASCII
countries (AX, CI, CW, RE, BL, TR) and the three apostrophe names (CI, KP, LA)
are exercised through their ASCII codes only, never a cased name lookup.
"""
import os

JOBS = [
    # alpha-2
    ("get", "AF"), ("get", "US"), ("get", "JP"), ("get", "br"), ("get", "DE"),
    # alpha-3
    ("get", "AFG"), ("get", "USA"), ("get", "jpn"), ("get", "IND"),
    # numeric string (3 digits, routed to numeric before alpha-3)
    ("get", "004"), ("get", "840"), ("get", "356"),
    # "000" is excluded from the numeric branch, falls to alpha-3 -> miss
    ("get", "000"),
    # exact name (uppercased match) and apolitical fall-through
    ("get", "Japan"), ("get", "United States of America"), ("get", "ZIMBABWE"),
    ("get", "Palestine"), ("get", "Taiwan"),
    # name miss -> apolitical miss -> KeyError
    ("get", "Atlantis"), ("get", "ZZ"), ("get", "XYZ"),
    # int keys, zero-padded
    ("getint", "4"), ("getint", "840"), ("getint", "51"), ("getint", "392"),
    ("getint", "0"), ("getint", "999"),
    # contains, codes only for non-ASCII / apostrophe countries
    ("contains", "US"), ("contains", "ZZ"), ("contains", "USA"),
    ("contains", "999"), ("contains", "CI"), ("contains", "KP"),
    ("contains", "TR"), ("contains", "004"), ("contains", "000"),
    # len
    ("len", ""),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
