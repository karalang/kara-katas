#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored quine-mccluskey library and
writes expected.out. Each line is a boolean-minimisation spec (see mk.py):

    qm <num_bits> <ones-csv> <dc-csv>

For each the oracle builds a QuineMcCluskey(use_xor=False), calls
simplify(ones, dc=dc, num_bits=nbits) to get the minimal sum-of-products cover
as a set of implicant strings ('0'/'1'/'-', MSB first), and prints:

    <job line> => <count>
    <t0 t1 ...>        the cover terms, sorted, space-joined (one line)

mini_quinemccluskey.kara reproduces this byte-for-byte on every backend. The
library returns a set, so the oracle sorts it; every spec in mk.py has a unique
cover (all prime implicants essential), so the sorted result does not depend on
the library's per-process set-iteration order."""
import sys

sys.path.insert(0, "vendor")
from quine_mccluskey.qm import QuineMcCluskey  # noqa: E402


def row(line):
    toks = line.split(" ")
    nbits = int(toks[1])
    ones = [int(x) for x in toks[2].split(",")]
    dc = [] if toks[3] == "-" else [int(x) for x in toks[3].split(",")]
    q = QuineMcCluskey(use_xor=False)
    res = q.simplify(ones, dc=dc, num_bits=nbits)
    terms = sorted(res) if res else []
    out = [line + " => " + str(len(terms))]
    out.append(" ".join(terms))
    return "\n".join(out)


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(row(line))
    sys.stdout.write("\n".join(out) + "\n")


main()
