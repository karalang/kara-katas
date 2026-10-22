#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_unionfind (tab-separated: op then arg).

A stream of disjoint-set sessions. `new <n>` starts a fresh union-find over the
elements 0..n-1; the ops that follow act on it:

  new <n>            start a fresh union-find of n singletons
  unite <i> <j>      merge the sets containing i and j
  find <i>           print the representative (root) of i's set
  same <i> <j>       print yes/no: are i and j in the same set?
  groups             print the current partition, one group per root in index
                     order, members comma-joined, groups joined with '|'

A standalone grid-connectivity op (its own fresh union-find, the library's
`isconnected`):

  conn <nw> <nh> <cells>   cells is an nw*nh row-major string of '0'/'1'
                           (cell (i,j) = cells[i*nh + j]); print yes if every
                           '1' cell forms a single 4-connected region, else no

mk.py writes only literal inputs (no library import); oracle.py replays every
job against the vendored `unionfind` library. All inputs are ASCII. See
README.md."""
import os

os.makedirs("data", exist_ok=True)

SESSIONS = [
    # Kruskal-style merges with connectivity and partition snapshots
    ("uf", 8,
     [("same", 0, 7), ("unite", 0, 1), ("unite", 2, 3), ("unite", 1, 3),
      ("find", 0), ("find", 2), ("same", 0, 3), ("same", 0, 4), ("groups",),
      ("unite", 4, 5), ("unite", 6, 7), ("unite", 5, 7), ("groups",),
      ("unite", 0, 4), ("same", 1, 6), ("find", 6), ("groups",)]),
    # a chain, then a star, exercising path compression through find
    ("uf", 6,
     [("unite", 0, 1), ("unite", 1, 2), ("unite", 2, 3), ("unite", 3, 4),
      ("find", 0), ("same", 0, 4), ("unite", 5, 0), ("groups",),
      ("find", 5), ("find", 4)]),
    # idempotent unites and self-unite
    ("uf", 4,
     [("unite", 0, 0), ("unite", 1, 1), ("unite", 0, 1), ("unite", 1, 0),
      ("same", 0, 1), ("groups",), ("find", 0), ("find", 1)]),
    # singletons: every element its own group
    ("uf", 5,
     [("groups",), ("find", 3), ("same", 2, 2), ("same", 1, 4)]),
    # grid connectivity: connected shapes and broken ones
    ("grid", None,
     [("conn", 3, 3, "111101111"),   # ring of 1s with a 0 centre: connected
      ("conn", 3, 3, "100010001"),   # diagonal: NOT 4-connected
      ("conn", 3, 3, "110000011"),   # two separate blobs
      ("conn", 1, 1, "1"),            # single cell
      ("conn", 2, 2, "0000"),         # no 1s at all: not connected
      ("conn", 4, 3, "111100100100"),  # an L/T shape
      ("conn", 3, 4, "101111101111"),  # a plus-ish region with gaps
      ("conn", 2, 3, "111111")]),     # full grid: connected
]

lines = []
for kind, n, ops in SESSIONS:
    if kind == "uf":
        lines.append("new\t%d" % n)
    for op in ops:
        if op[0] == "groups":
            lines.append("groups")
        elif op[0] == "find":
            lines.append("find\t%d" % op[1])
        elif op[0] in ("unite", "same"):
            lines.append("%s\t%d %d" % (op[0], op[1], op[2]))
        elif op[0] == "conn":
            lines.append("conn\t%d %d %s" % (op[1], op[2], op[3]))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
