#!/usr/bin/env python3
"""Runs data/jobs.tsv through pytimeparse and prints expected.out.

Each job is <sval>\t<granularity>. The result is pytimeparse.parse(sval,
granularity): an int, a float, or None. It is printed as `result=<r>` where
<r> is str(int), repr(float), or the literal `None`.
"""
import sys

sys.path.insert(0, "vendor")
from pytimeparse.timeparse import timeparse  # noqa: E402


def run(sval, gran):
    r = timeparse(sval, granularity=gran)
    if r is None:
        return "result=None"
    if isinstance(r, int):
        return "result=" + str(r)
    return "result=" + repr(r)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        out.append("  " + run(f[0], f[1]))
sys.stdout.write("\n".join(out) + "\n")
