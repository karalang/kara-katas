#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one constraint-satisfaction problem per line, as a
space-separated spec the solver enumerates every solution of. The kinds:

    queens N                 the N-queens problem on an NxN board
    rooks N                  N non-attacking rooks on an NxN board
    color V K e e e ...      K-colour a graph of V nodes; each e is "a-b"
    alldiff V d0 d1 ...       V variables all-different; each dI is a
                             comma-separated domain (e.g. 0,1,2,3)

No python-constraint import here (only literal specs); oracle.py replays each
line through the vendored library to produce expected.out. The specs span the
classic examples (queens 4-8, rooks), 2- and 3-colourings of a 5-cycle, K4 and
the Petersen graph (satisfiable and not), and all-different over full and
restricted domains."""

JOBS = [
    "queens 4",
    "queens 5",
    "queens 6",
    "queens 8",
    "rooks 3",
    "rooks 4",
    "color 5 3 0-1 1-2 2-3 3-4 4-0",
    "color 5 2 0-1 1-2 2-3 3-4 4-0",
    "color 4 3 0-1 0-2 0-3 1-2 1-3 2-3",
    "color 4 4 0-1 0-2 0-3 1-2 1-3 2-3",
    "color 10 3 0-1 1-2 2-3 3-4 4-0 0-5 1-6 2-7 3-8 4-9 5-7 7-9 9-6 6-8 8-5",
    "alldiff 4 0,1,2,3 0,1,2,3 0,1,2,3 0,1,2,3",
    "alldiff 4 0,1 0,1,2 1,2,3 2,3",
    "alldiff 5 0,1,2,3,4 0,1,2,3,4 0,1,2,3,4 0,1,2,3,4 0,1,2,3,4",
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for job in JOBS:
            fh.write(job + "\n")


main()
