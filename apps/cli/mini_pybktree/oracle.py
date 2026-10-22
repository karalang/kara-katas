#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored pybktree and writes expected.out.
The vendored pybktree is a single pure-Python module with no dependencies, so
the oracle runs exactly the BK-tree code mini_pybktree.kara mirrors. See mk.py
for the op table."""
import sys
sys.path.insert(0, "vendor")
from pybktree import BKTree, hamming_distance  # noqa: E402


def fmt_find(pairs):
    return "[" + ", ".join("(%d, %d)" % (d, it) for d, it in pairs) + "]"


def fmt_list(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


tree = BKTree(hamming_distance)
out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "add":
        tree.add(int(f[1]))
        out.append(repr(tree))
    elif op == "find":
        out.append(fmt_find(tree.find(int(f[1]), int(f[2]))))
    elif op == "iter":
        out.append(fmt_list(list(tree)))
    elif op == "len":
        out.append(str(len(list(tree))))
    elif op == "dist":
        out.append(str(hamming_distance(int(f[1]), int(f[2]))))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
