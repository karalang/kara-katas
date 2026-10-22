#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated <dir>\t<date>.

<dir> is `g2h` (Gregorian -> Hijri) or `h2g` (Hijri -> Gregorian); <date> is an
ISO date `YYYY-MM-DD` in the source calendar. The set spans the supported Umm
al-Qura range (Gregorian 1924-08-01 .. 2077-11-16, Hijri 1343-01-01 ..
1500-12-30), its endpoints, and the out-of-range / invalid-field cases that
raise.
"""
import os

JOBS = [
    ("g2h", "1924-08-02"),
    ("g2h", "2023-10-22"),
    ("g2h", "2000-01-01"),
    ("g2h", "1990-05-20"),
    ("g2h", "2077-11-16"),
    ("g2h", "1924-07-31"),
    ("g2h", "2077-11-17"),
    ("h2g", "1445-04-07"),
    ("h2g", "1343-01-01"),
    ("h2g", "1500-12-30"),
    ("h2g", "1446-09-01"),
    ("h2g", "1411-06-05"),
    ("h2g", "1342-12-30"),
    ("h2g", "1501-01-01"),
    ("h2g", "1445-13-01"),
    ("h2g", "1445-01-40"),
    ("h2g", "1445-12-29"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for d, s in JOBS:
        fh.write(d + "\t" + s + "\n")
print("wrote data/jobs.tsv:", len(JOBS), "jobs")
