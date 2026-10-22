#!/usr/bin/env python3
"""Writes data/jobs.tsv: one roman-numeral conversion per line, tab-separated.

Columns: op and arg. Ops exercise the library's public API directly:
  toroman   <int>      toRoman(int(arg))
  tromanf   <float>    toRoman(float(arg))  -> NotIntegerError
  fromroman <str>      fromRoman(arg)                 (special_case=True)
  fromromanns <str>    fromRoman(arg, special_case=False)

Covered: the full digit range, the special case N=0, the out-of-range and
not-integer errors with their exact texts, case-insensitive input, and
invalid-numeral forms the regex rejects (too many repeats, a bad ordering),
whose error echoes the *uppercased* input.
"""
import os

JOBS = [
    ("toroman", "0"), ("toroman", "1"), ("toroman", "4"), ("toroman", "9"),
    ("toroman", "14"), ("toroman", "40"), ("toroman", "90"), ("toroman", "400"),
    ("toroman", "944"), ("toroman", "1990"), ("toroman", "2024"),
    ("toroman", "3888"), ("toroman", "4999"),
    # out of range
    ("toroman", "-1"), ("toroman", "5000"), ("toroman", "5001"),
    # not an integer
    ("tromanf", "3.5"),
    # fromRoman, special_case default True
    ("fromroman", ""), ("fromroman", "N"), ("fromroman", "n"),
    ("fromroman", "I"), ("fromroman", "iv"), ("fromroman", "MCMXC"),
    ("fromroman", "MMXXIV"), ("fromroman", "MMMM"),
    ("fromroman", "MMMMCMXCIX"), ("fromroman", "DCCC"), ("fromroman", "mcmxciv"),
    # invalid forms (regex rejects); error echoes the uppercased input
    ("fromroman", "IIII"), ("fromroman", "VV"), ("fromroman", "IC"),
    ("fromroman", "MMMMM"), ("fromroman", "DCCCC"), ("fromroman", "abc"),
    # fromRoman with special_case=False
    ("fromromanns", "N"), ("fromromanns", "MMXXIV"), ("fromromanns", "n"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
