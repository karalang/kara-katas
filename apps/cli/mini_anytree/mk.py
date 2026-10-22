#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_anytree. The first block builds one tree with
`n` lines (name, then parent name — empty parent means the root), in the order
the nodes are attached; the rest are queries against it, one op per line
(tab-separated):

    n  \t <name> \t <parent>   attach node <name> under <parent> (empty = root)
    rt                         RenderTree, ContStyle  (box-drawing)   -> tree lines
    rta                        RenderTree, AsciiStyle (|-- +-- )      -> tree lines
    pre / post / lvl           PreOrder / PostOrder / LevelOrder names of the whole tree
    path \t <n>                path root..node        -> [a, b, c]
    anc  \t <n>                ancestors (root..parent)
    desc \t <n>                descendants (pre-order, excluding the node)
    dep  \t <n>                depth (edges to root)
    hgt  \t <n>                height (edges to the deepest leaf)
    leaf \t <n>                is_leaf -> yes | no    root \t <n> is_root -> yes | no
    sib  \t <n>                siblings
    lvs  \t <n>                leaves under the node (pre-order)
    walk \t <a> \t <b>         Walker().walk(a, b) -> up:[...] top:x down:[...]
    find \t <prefix>           findall(name startswith prefix), pre-order

Node names are unique ASCII tokens. `oracle.py` replays the sequence against the
vendored anytree.
"""
import os

# (name, parent) in attach order — the Walker doc tree plus extra breadth.
NODES = [
    ("f", ""),
    ("b", "f"), ("a", "b"), ("d", "b"), ("c", "d"), ("e", "d"),
    ("g", "f"), ("i", "g"), ("h", "i"),
    ("g2", "f"), ("k", "g2"),       # a third top branch, and depth under g2
    ("a2", "b"),                     # a second child-list entry for b (order after d)
]

ops = [("n", name, parent) for name, parent in NODES]

ops.append(("rt",))
ops.append(("rta",))
ops.append(("pre",))
ops.append(("post",))
ops.append(("lvl",))

for n in ["h", "d", "f", "e", "k"]:
    ops.append(("path", n))
    ops.append(("anc", n))
    ops.append(("dep", n))
    ops.append(("hgt", n))

for n in ["f", "b", "d", "a", "h", "g2"]:
    ops.append(("desc", n))

for n in ["f", "a", "d", "h"]:
    ops.append(("leaf", n))
    ops.append(("root", n))
    ops.append(("sib", n))
    ops.append(("lvs", n))

for a, b in [("f", "f"), ("f", "b"), ("b", "f"), ("h", "e"), ("d", "e"),
             ("a", "k"), ("c", "h")]:
    ops.append(("walk", a, b))

for p in ["a", "g", "x", "f"]:
    ops.append(("find", p))

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op in ops:
        fh.write("\t".join(str(x) for x in op) + "\n")
