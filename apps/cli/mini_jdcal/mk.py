#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_jdcal (tab-separated: op then space-joined ints):
  g <y> <m> <d>   Gregorian calendar date -> Modified Julian Date (integer)
  j <y> <m> <d>   Julian calendar date    -> Modified Julian Date (integer)
  rg <mjd>        MJD -> proleptic Gregorian date, printed "y|m|d"
  rj <mjd>        MJD -> proleptic Julian date,    printed "y|m|d"
  leap <y>        is_leap(y) in the Gregorian calendar -> "1" / "0"
mk.py writes only literal inputs (no library import); oracle.py replays every job
against the vendored jdcal library. All conversions are date-only (midnight), so
the Julian-date fractional part is always 0 and is not printed. See README.md."""
import os
os.makedirs("data", exist_ok=True)

gcal = [
    (2000, 1, 1), (1950, 1, 1), (1999, 10, 12), (2000, 2, 29), (2001, 2, 28),
    (1582, 10, 15), (1582, 10, 4), (-1999, 10, 12), (0, 1, 1), (1, 1, 1),
    (-1, 12, 31), (-4699, 1, 1), (2245, 12, 31), (1678, 9, 9), (2012, 11, 11),
    (1970, 1, 1), (2024, 2, 29), (1900, 3, 1), (2100, 1, 1), (-4712, 1, 1),
    (2000, -2, -4), (2000, 0, 1), (2000, 3, 0), (2000, 2, 30),   # carry-over forms
]
jcal = [
    (2000, 1, 1), (1950, 1, 1), (1999, 10, 12), (1, 1, 1), (0, 1, 1),
    (-4699, 1, 1), (2245, 12, 31), (1678, 10, 9), (2012, 11, 11), (1582, 10, 5),
]
mjds = [0, 51544, -2395215, 40587, 51827, -678774, 141393, -679162, 15020, 59000,
        -100000, 100000, 1, -1, 58849]
leaps = [2000, 1900, 2004, 2001, 1600, 2100, 0, -1, -4, 4, 1996, 2024, 2023]

lines = []
for (y, m, d) in gcal:
    lines.append("g\t%d %d %d" % (y, m, d))
for (y, m, d) in jcal:
    lines.append("j\t%d %d %d" % (y, m, d))
for mjd in mjds:
    lines.append("rg\t%d" % mjd)
for mjd in mjds:
    lines.append("rj\t%d" % mjd)
for y in leaps:
    lines.append("leap\t%d" % y)

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
