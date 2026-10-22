#!/usr/bin/env python3
"""Runs data/jobs.tsv through price-parser's parse_number and prints expected.out.

Each job is <num>\t<decsep>. The result is parse_number(num, decsep): a Decimal
or None, printed as `result=<str(Decimal)>` or `result=None`.
"""
import sys

sys.path.insert(0, "vendor")
from price_parser.parser import parse_number  # noqa: E402


def run(num, dec):
    sep = None if dec == "-" else dec
    r = parse_number(num, decimal_separator=sep)
    return "result=None" if r is None else "result=" + str(r)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        out.append("  " + run(f[0], f[1]))
sys.stdout.write("\n".join(out) + "\n")
