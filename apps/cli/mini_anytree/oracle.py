#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored anytree and writes expected.out.
See mk.py for the op table. The vendored anytree is pure Python with no
dependencies, so oracle.py runs exactly the code mini_anytree.kara mirrors."""
import sys

sys.path.insert(0, "vendor")
from anytree import (  # noqa: E402
    Node, RenderTree, AsciiStyle, ContStyle,
    PreOrderIter, PostOrderIter, LevelOrderIter, Walker,
)
from anytree.search import findall  # noqa: E402


def names(nodes):
    return "[" + ", ".join(n.name for n in nodes) + "]"


nodemap = {}
root = None
out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "n":
        name, parent = f[1], f[2]
        if parent:
            nodemap[name] = Node(name, parent=nodemap[parent])
        else:
            nodemap[name] = Node(name)
            root = nodemap[name]
    elif op == "rt":
        out.append(RenderTree(root, style=ContStyle()).by_attr("name"))
    elif op == "rta":
        out.append(RenderTree(root, style=AsciiStyle()).by_attr("name"))
    elif op == "pre":
        out.append(names(list(PreOrderIter(root))))
    elif op == "post":
        out.append(names(list(PostOrderIter(root))))
    elif op == "lvl":
        out.append(names(list(LevelOrderIter(root))))
    elif op == "path":
        out.append(names(nodemap[f[1]].path))
    elif op == "anc":
        out.append(names(nodemap[f[1]].ancestors))
    elif op == "desc":
        out.append(names(nodemap[f[1]].descendants))
    elif op == "dep":
        out.append(str(nodemap[f[1]].depth))
    elif op == "hgt":
        out.append(str(nodemap[f[1]].height))
    elif op == "leaf":
        out.append("yes" if nodemap[f[1]].is_leaf else "no")
    elif op == "root":
        out.append("yes" if nodemap[f[1]].is_root else "no")
    elif op == "sib":
        out.append(names(nodemap[f[1]].siblings))
    elif op == "lvs":
        out.append(names(nodemap[f[1]].leaves))
    elif op == "walk":
        up, top, down = Walker().walk(nodemap[f[1]], nodemap[f[2]])
        out.append("up:%s top:%s down:%s" % (names(up), top.name, names(down)))
    elif op == "find":
        pref = f[1]
        res = findall(root, filter_=lambda n: n.name.startswith(pref))
        out.append(names(res))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
