#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored word2number, prints expected.out."""
import sys

sys.path.insert(0, "vendor")
from word2number import w2n  # noqa: E402


def run(op, arg):
    try:
        return str(w2n.word_to_num(arg))
    except ValueError as e:
        return "error: " + str(e)


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
