#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored persiantools library and writes
expected.out. Each line is either

    g YYYY-MM-DD     Gregorian -> Jalali
    j YYYY-MM-DD     Jalali -> Gregorian

and the job prints the converted date in ISO form plus its Persian-digit
rendering:

    <iso> <fa>

mini_persiantools.kara reproduces this byte-for-byte on every backend."""
import sys
from datetime import date

sys.path.insert(0, "vendor")
from persiantools import digits  # noqa: E402
from persiantools.jdatetime import JalaliDate  # noqa: E402


def iso(y, m, d):
    return "%04d-%02d-%02d" % (y, m, d)


def row(line):
    kind, ds = line.split(" ", 1)
    y, m, d = (int(x) for x in ds.split("-"))
    if kind == "g":
        j = JalaliDate.to_jalali(date(y, m, d))
        out = iso(j.year, j.month, j.day)
    else:
        g = JalaliDate(y, m, d).to_gregorian()
        out = iso(g.year, g.month, g.day)
    return out + " " + digits.en_to_fa(out)


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(row(line))
    sys.stdout.write("\n".join(out) + "\n")


main()
