#!/usr/bin/env python3
"""Runs data/jobs.tsv through hijri-converter and prints expected.out."""
import sys

sys.path.insert(0, "vendor")
from hijri_converter import Gregorian, Hijri  # noqa: E402


def g2h(s):
    y, m, d = int(s[0:4]), int(s[5:7]), int(s[8:10])
    try:
        h = Gregorian(y, m, d).to_hijri()
    except OverflowError as e:
        return ["error=" + str(e)]
    return [
        "hijri_iso=" + h.isoformat(),
        "hijri_dmy=" + h.dmyformat(),
        "hijri_dmy2=" + h.dmyformat(separator="-", padding=False),
        "month_en=" + h.month_name("en"),
        "month_ar=" + h.month_name("ar"),
        "month_bn=" + h.month_name("bn"),
        "day_en=" + h.day_name("en"),
        "weekday=" + str(h.weekday()),
        "isoweekday=" + str(h.isoweekday()),
        "length=" + str(h.month_length()),
        "notation=" + h.notation("en"),
    ]


def h2g(s):
    y, m, d = int(s[0:4]), int(s[5:7]), int(s[8:10])
    try:
        h = Hijri(y, m, d)
    except (OverflowError, ValueError) as e:
        return ["error=" + str(e)]
    g = h.to_gregorian()
    return [
        "greg_iso=" + g.isoformat(),
        "greg_dmy=" + g.dmyformat(),
        "month_en=" + g.month_name("en"),
        "month_ar=" + g.month_name("ar"),
        "day_en=" + g.day_name("en"),
        "notation=" + g.notation("en"),
    ]


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        rows = g2h(f[1]) if f[0] == "g2h" else h2g(f[1])
        for r in rows:
            out.append("  " + r)
sys.stdout.write("\n".join(out) + "\n")
