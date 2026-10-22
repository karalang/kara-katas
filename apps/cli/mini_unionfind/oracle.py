#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored `unionfind` library and writes
expected.out. See mk.py for the op grammar.

`new <n>` starts a fresh unionfind(n); `conn` builds its own grid and calls the
library's `unionfind.isconnected`. mini_unionfind.kara reproduces this
byte-for-byte."""
import sys

sys.path.insert(0, "vendor")
from unionfind import unionfind  # noqa: E402

uf = None
out = []

for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    a = arg.split(" ") if arg else []
    if op == "new":
        uf = unionfind(int(a[0]))
    elif op == "unite":
        uf.unite(int(a[0]), int(a[1]))
    elif op == "find":
        out.append(str(uf.find(int(a[0]))))
    elif op == "same":
        out.append("yes" if uf.issame(int(a[0]), int(a[1])) else "no")
    elif op == "groups":
        out.append("|".join(",".join(str(j) for j in g) for g in uf.groups()))
    elif op == "conn":
        nw, nh, cells = int(a[0]), int(a[1]), a[2]
        ll = [[cells[i * nh + j] == "1" for j in range(nh)] for i in range(nw)]
        out.append("yes" if unionfind.isconnected(ll) else "no")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
