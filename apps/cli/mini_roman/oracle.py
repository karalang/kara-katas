#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored roman, prints expected.out."""
import sys

sys.path.insert(0, "vendor")
import roman  # noqa: E402


def run(op, arg):
    try:
        if op == "toroman":
            return roman.toRoman(int(arg))
        if op == "tromanf":
            return roman.toRoman(float(arg))
        if op == "fromroman":
            return str(roman.fromRoman(arg))
        if op == "fromromanns":
            return str(roman.fromRoman(arg, special_case=False))
    except roman.RomanError as e:
        return "error: " + type(e).__name__ + ": " + str(e)
    return "error: unknown op"


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
