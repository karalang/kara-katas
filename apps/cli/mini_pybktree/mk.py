#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pybktree: build one BK-tree over hamming
distance by adding integers, then query it. One op per line (tab-separated):

    add  <v>          add integer v to the tree        -> <repr> after the add
    find <item> <n>   items within hamming distance n   -> [(d, item), ...]
    iter              all items, in the tree's BFS order -> [a, b, ...]
    len               number of items                   -> <n>
    dist <x> <y>      hamming_distance(x, y)             -> <d>

The BK-tree branches by distance-to-parent, so the add order fixes the tree
shape (and therefore the BFS `iter` order and the tie order inside `find`).
`oracle.py` replays the sequence against the vendored pybktree. The `find`
queries sweep n from 0 (exact) up, and one huge n (1000) returns everything, so
the triangle-inequality pruning (`[distance-n, distance+n]`) is exercised at
both ends.
"""
import os

ADD = [0, 4, 5, 14, 15, 8, 10, 12, 31, 7, 1, 2, 3, 63, 100, 127, 200, 255]

ops = []
for v in ADD:
    ops.append(("add", v))
ops.append(("iter",))
ops.append(("len",))

for item, n in [(13, 0), (13, 1), (13, 2), (13, 3), (0, 1000), (255, 1),
                (200, 2), (7, 2), (1, 1), (64, 0), (100, 0), (999, 2),
                (15, 4), (0, 0)]:
    ops.append(("find", item, n))

for x, y in [(0, 15), (8, 15), (13, 5), (255, 0), (127, 128), (1023, 0)]:
    ops.append(("dist", x, y))

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op in ops:
        fh.write("\t".join(str(x) for x in op) + "\n")
