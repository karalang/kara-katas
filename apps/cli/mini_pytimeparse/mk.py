#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated <sval>\t<granularity>.

Each job is a time expression and the granularity ("seconds" or "minutes")
to parse it under. The curated set covers every one of pytimeparse's five
time formats (unit words, MM:SS, [W D] HH:MM:SS, D:HH:MM:SS, :SS), signed
input, the unit-word spellings and [,/] separators, decimal components, the
int / int-with-float-component / float output branches, the granularity=
minutes reinterpretation, the malformed-number skip, and the no-match (None)
cases.
"""
import os

JOBS = [
    ("32 min", "seconds"),
    ("1w3d2h32m", "seconds"),
    ("1 minute, 24 secs", "seconds"),
    ("1m24s", "seconds"),
    ("4:13", "seconds"),
    (":13", "seconds"),
    ("4:13:02", "seconds"),
    ("4:13:02.266", "seconds"),
    ("2:04:13:02.266", "seconds"),
    ("4:32", "minutes"),
    ("7:02.223", "minutes"),
    ("0:02", "seconds"),
    ("2 days,  4:13:02", "seconds"),
    ("5hr34m56s", "seconds"),
    ("- 1 minute", "seconds"),
    ("+ 1 minute", "seconds"),
    ("1.2 seconds", "seconds"),
    ("1.2 minutes", "seconds"),
    ("1.5h", "seconds"),
    ("4.5m 3s", "seconds"),
    ("1:30", "seconds"),
    ("1:30", "minutes"),
    ("1:24", "seconds"),
    ("1:24", "minutes"),
    ("10 weeks", "seconds"),
    ("1.0 seconds", "seconds"),
    ("2 hours/13 mins", "seconds"),
    ("1.2.3s", "seconds"),
    ("32 m - 1 s", "seconds"),
    ("|5m", "seconds"),
    ("90", "seconds"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for sval, gran in JOBS:
        fh.write(sval + "\t" + gran + "\n")
print("wrote data/jobs.tsv:", len(JOBS), "jobs")
