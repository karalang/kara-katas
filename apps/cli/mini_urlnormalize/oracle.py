#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored url_normalize, prints expected.out."""
import sys

sys.path.insert(0, "vendor")
from url_normalize import url_normalize  # noqa: E402


def run(op, arg):
    return url_normalize(arg)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        arg = f[1] if len(f) > 1 else ""
        out.append("== " + " | ".join(f))
        out.append("  " + run(f[0], arg))
sys.stdout.write("\n".join(out) + "\n")
