#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one boolean-function minimisation problem per line, as

    qm <num_bits> <ones-csv> <dc-csv>

where <ones-csv> is the comma-separated list of minterms for which the function
is 1, and <dc-csv> is the comma-separated list of don't-care minterms (or "-"
when there are none). oracle.py replays each line through the vendored
quine-mccluskey library.

No quine-mccluskey import here (only literal specs). Every spec below was chosen
so that its minimal sum-of-products cover is UNIQUE: every prime implicant is
essential, so the cover is the full set of prime implicants, which is
independent of the library's internal set-iteration order (verified to be
byte-identical across many PYTHONHASHSEED values during development). That is
the one precondition for the run==build A/B rule here, since the library walks
Python sets whose order is per-process random."""

# (num_bits, ones, dc)
JOBS = [
    (4, [2, 6, 10, 14], []),
    (2, [0], []),
    (2, [3], []),
    (2, [0, 1, 2, 3], []),
    (2, [1, 3], []),
    (3, [4, 5, 6, 7], []),
    (3, [0, 2, 4, 6], []),
    (3, [1, 5], []),
    (3, [0, 1, 2, 3, 4, 5, 6, 7], []),
    (4, [8, 9, 10, 11, 12, 13, 14, 15], []),
    (4, [0, 8], []),
    (4, [5, 7, 13, 15], []),
    (3, [0, 1, 4, 5], []),
    (3, [2, 3, 6, 7], []),
    (4, [0, 4, 8, 12], []),
    (4, [1, 3, 5, 7, 9, 11, 13, 15], []),
    (4, [0, 1, 2, 3, 8, 9, 10, 11], []),
    (4, [6, 7, 14, 15], []),
    (4, [0, 2, 8, 10], []),
    (4, [4, 6, 12, 14], []),
    (3, [0, 1], []),
    (3, [0, 1, 2, 3, 4, 5], []),
    (4, [0, 5, 10, 15], []),
    (4, [3, 7, 11, 15], []),
    (4, [0, 3, 12, 15], []),
    (4, [2, 6, 14], [10]),
    (3, [1, 5, 7], [3]),
    (3, [0, 2, 6], [4]),
    (4, [8, 9, 11], [10]),
    (3, [4, 5, 6], [7]),
    (3, [1, 3, 7], [5]),
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for (nbits, ones, dc) in JOBS:
            ones_s = ",".join(str(x) for x in ones)
            dc_s = ",".join(str(x) for x in dc) if dc else "-"
            fh.write("qm %d %s %s\n" % (nbits, ones_s, dc_s))


main()
