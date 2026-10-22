#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored iso3166, prints expected.out."""
import sys

sys.path.insert(0, "vendor")
from iso3166 import countries  # noqa: E402


def run(op, arg):
    if op == "len":
        return str(len(countries))
    if op == "contains":
        # the contains arg is always a string here (codes / numeric strings)
        return "True" if arg in countries else "False"
    if op == "getint":
        n = int(arg)
        try:
            return repr(countries.get(n))
        except KeyError as e:
            return "error: KeyError " + str(e)
    # op == "get"
    try:
        return repr(countries.get(arg))
    except KeyError as e:
        return "error: KeyError " + str(e)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        op = f[0]
        arg = f[1] if len(f) > 1 else ""
        out.append("== " + " | ".join(f))
        out.append("  " + run(op, arg))
sys.stdout.write("\n".join(out) + "\n")
