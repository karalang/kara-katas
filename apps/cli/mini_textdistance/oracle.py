#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored textdistance and prints expected.out.

external=False keeps every metric on textdistance's own pure-Python
implementation (never a side C library), so the result is deterministic.
"""
import sys

sys.path.insert(0, "vendor")
import textdistance as td  # noqa: E402

H = td.Hamming(external=False)
L = td.Levenshtein(external=False)
DL = td.DamerauLevenshtein(external=False)   # restricted (OSA) by default
SEQ = td.LCSSeq(external=False)
STR = td.LCSStr(external=False)


def run(op, arg):
    a, b = arg.split("|")
    return (
        "ham=" + str(H(a, b))
        + " lev=" + str(L(a, b))
        + " dam=" + str(DL(a, b))
        + " lcsseq=" + str(SEQ.similarity(a, b))
        + " lcsstr=" + str(STR.similarity(a, b))
    )


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
