#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored immutables.Map and writes expected.out.

Each op prints one line:
    s <k> <v> -> `len <n>`     (the new length)
    d <k>     -> `len <n>`, or `miss` if the key was absent
    g <k>     -> the value, or `miss`
    h <k>     -> `yes` / `no`
    l         -> `len <n>`
    k         -> the keys in the Map's iteration order, as `[k1, k2, ...]`

The Map is the pure-Python immutables.map.Map (the C extension is not built),
which is exactly the HAMT mini_immutables.kara ports.
"""
import sys

sys.path.insert(0, "vendor")
from immutables.map import Map  # noqa: E402


m = Map()
out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "s":
        k, v = int(f[1]), int(f[2])
        m = m.set(k, v)
        out.append("s %d %d -> len %d" % (k, v, len(m)))
    elif op == "d":
        k = int(f[1])
        try:
            m = m.delete(k)
            out.append("d %d -> len %d" % (k, len(m)))
        except KeyError:
            out.append("d %d -> miss" % k)
    elif op == "g":
        k = int(f[1])
        v = m.get(k, None)
        out.append("g %d -> %s" % (k, "miss" if v is None else str(v)))
    elif op == "h":
        k = int(f[1])
        out.append("h %d -> %s" % (k, "yes" if k in m else "no"))
    elif op == "l":
        out.append("len %d" % len(m))
    elif op == "k":
        out.append("[" + ", ".join(str(x) for x in m) + "]")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
