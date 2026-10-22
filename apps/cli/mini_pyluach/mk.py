#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pyluach (tab-separated: op then ints):
  g2h <y> <m> <d>   Gregorian (proleptic) date -> Hebrew date "HYYYY-MM-DD", or INVALID
  h2g <y> <m> <d>   Hebrew date -> Gregorian date "YYYY-MM-DD", or INVALID
  wd  <y> <m> <d>   weekday of a Gregorian date, 1 (Sunday) .. 7 (Shabbos), or INVALID
  heb <y> <m> <d>   Gregorian date -> the converted Hebrew date as a gematria
                    (Hebrew-numeral) string "<day> <month> <year>", or INVALID
mk.py writes only literal inputs (no library import); oracle.py replays every job
against the vendored pyluach library. The heb strings carry Hebrew characters,
emitted as UTF-8. See README.md."""
import os
os.makedirs("data", exist_ok=True)

greg = [
    (2024, 10, 22), (2000, 1, 1), (1948, 5, 14), (2023, 9, 16), (1700, 1, 1),
    (1800, 12, 31), (1900, 2, 28), (2050, 6, 15), (2017, 3, 12), (1999, 12, 31),
    (2024, 2, 29), (1583, 1, 1), (2239, 12, 31), (5, 7, 4), (1, 1, 1),
    (2026, 3, 14), (2026, 9, 12), (1776, 7, 4), (2033, 4, 1), (1990, 11, 6),
    # invalid
    (2000, 13, 1), (2000, 2, 30), (0, 1, 1), (2023, 0, 5), (2023, 4, 31),
]
heb = [
    (5785, 7, 1), (5784, 1, 15), (5784, 13, 14), (5783, 9, 25), (5700, 6, 29),
    (5343, 7, 1), (5999, 6, 29), (5784, 8, 30), (5786, 7, 10), (5786, 1, 15),
    (5784, 1, 30),
    # invalid
    (5784, 14, 1), (5783, 13, 1), (0, 1, 1), (5784, 9, 30),
]

lines = []
for (y, m, d) in greg:
    lines.append("g2h\t%d %d %d" % (y, m, d))
for (y, m, d) in greg:
    lines.append("wd\t%d %d %d" % (y, m, d))
for (y, m, d) in greg:
    lines.append("heb\t%d %d %d" % (y, m, d))
for (y, m, d) in heb:
    lines.append("h2g\t%d %d %d" % (y, m, d))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
