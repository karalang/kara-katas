#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored pyluach library and writes
expected.out. See mk.py for the op table.

  g2h -> GregorianDate(y,m,d).to_heb() as "HY-MM-DD", or "INVALID".
  h2g -> HebrewDate(y,m,d).to_greg()   as "Y-MM-DD",  or "INVALID".
  wd  -> GregorianDate(y,m,d).weekday() (1..7),       or "INVALID".
  heb -> format(GregorianDate(y,m,d).to_heb(), '%*d %*B %*Y'), the library's own
         gematria rendering (day numeral, Hebrew month, Hebrew year with the
         thousands place); carries Hebrew characters (UTF-8), or "INVALID"."""
import sys
sys.path.insert(0, "vendor")
from pyluach.dates import GregorianDate, HebrewDate  # noqa: E402


def _greg_leap(y):
    return (y % 4 == 0) and not (y % 100 == 0 and y % 400 != 0)


def _greg_month_length(y, m):
    if m in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if m == 2:
        return 29 if _greg_leap(y) else 28
    return 30


def _greg_valid(y, m, d):
    # GregorianDate itself does no input validation, so the app defines its own
    # proleptic-Gregorian domain (year >= 1) and both sides reject outside it.
    return 1 <= y <= 9999 and 1 <= m <= 12 and 1 <= d <= _greg_month_length(y, m)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    p = [int(x) for x in arg.split()]
    if op == "g2h":
        if _greg_valid(p[0], p[1], p[2]):
            h = GregorianDate(p[0], p[1], p[2]).to_heb()
            out.append("%d-%02d-%02d" % (h.year, h.month, h.day))
        else:
            out.append("INVALID")
    elif op == "h2g":
        try:
            g = HebrewDate(p[0], p[1], p[2]).to_greg()
            out.append("%d-%02d-%02d" % (g.year, g.month, g.day))
        except Exception:
            out.append("INVALID")
    elif op == "wd":
        if _greg_valid(p[0], p[1], p[2]):
            out.append(str(GregorianDate(p[0], p[1], p[2]).weekday()))
        else:
            out.append("INVALID")
    elif op == "heb":
        if _greg_valid(p[0], p[1], p[2]):
            h = GregorianDate(p[0], p[1], p[2]).to_heb()
            out.append(format(h, "%*d %*B %*Y"))
        else:
            out.append("INVALID")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
