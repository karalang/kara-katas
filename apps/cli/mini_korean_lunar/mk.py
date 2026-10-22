#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_korean_lunar (tab-separated: op then ints):
  s2l <y> <m> <d>       Gregorian (solar) date -> Korean lunar date
                        ("YYYY-MM-DD" [+ " Intercalation"]), or INVALID
  l2s <y> <m> <d> <i>   Korean lunar date (i = 1 if leap month) -> solar date
                        ("YYYY-MM-DD"), or INVALID
  gap <y> <m> <d>       solar date -> Korean sexagenary (gapja) string, or INVALID
  cgap <y> <m> <d>      solar date -> Chinese sexagenary string, or INVALID
mk.py writes only literal inputs (no library import); oracle.py replays every job
against the vendored korean_lunar_calendar library. The gapja strings contain CJK
characters, emitted as UTF-8. See README.md."""
import os
os.makedirs("data", exist_ok=True)

solar = [
    (1000, 2, 13), (1500, 6, 15), (1582, 10, 4), (1582, 10, 15), (1700, 1, 1),
    (1800, 12, 31), (1900, 2, 28), (1950, 8, 15), (1988, 9, 17), (2000, 1, 1),
    (2017, 6, 24), (2020, 2, 29), (2033, 12, 25), (2050, 1, 1), (2050, 12, 31),
    (1999, 5, 11), (1444, 7, 7), (2024, 10, 22), (2023, 3, 22), (1960, 7, 1),
    # invalid
    (999, 1, 1), (2051, 1, 1), (2000, 13, 1), (2000, 2, 30), (1582, 10, 10),
]
lunar = [
    (1000, 1, 1, 0), (1500, 6, 15, 0), (1700, 1, 1, 0), (1900, 1, 1, 0),
    (2000, 1, 1, 0), (2017, 5, 1, 1), (2020, 4, 1, 1), (2033, 11, 1, 1),
    (2050, 11, 18, 0), (1988, 8, 1, 0), (2024, 1, 1, 0), (2023, 2, 1, 1),
    # invalid
    (999, 1, 1, 0), (2050, 11, 19, 0), (2000, 3, 1, 1),
]

lines = []
for (y, m, d) in solar:
    lines.append("s2l\t%d %d %d" % (y, m, d))
for (y, m, d, i) in lunar:
    lines.append("l2s\t%d %d %d %d" % (y, m, d, i))
for (y, m, d) in solar:
    lines.append("gap\t%d %d %d" % (y, m, d))
for (y, m, d) in solar:
    lines.append("cgap\t%d %d %d" % (y, m, d))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
