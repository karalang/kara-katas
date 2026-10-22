#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored pymorton and writes expected.out.

For each job it prints a header line

    == <op> <args...>

then the result: `il2` / `il3` print the Morton code in decimal; `dl2` prints
`<x> <y>` and `dl3` prints `<x> <y> <z>`, the decoded coordinates. mini_morton.kara
reproduces this stream exactly.

The import target is vendor/pymorton3 — the vendored pymorton/__init__.py with
its four Python-2 `print` statements (all in unreachable type-guard branches)
rewritten as `print(...)` so it parses on Python 3; every bit operation is
byte-identical to vendor/pymorton/__init__.py (see README).
"""
import sys

sys.path.insert(0, "vendor/pymorton3/..")
import pymorton3 as m  # noqa: E402


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "il2":
        x, y = int(f[1]), int(f[2])
        out.append("== il2 %d %d" % (x, y))
        out.append("%d" % m.interleave2(x, y))
    elif op == "il3":
        x, y, z = int(f[1]), int(f[2]), int(f[3])
        out.append("== il3 %d %d %d" % (x, y, z))
        out.append("%d" % m.interleave3(x, y, z))
    elif op == "dl2":
        n = int(f[1])
        out.append("== dl2 %d" % n)
        a, b = m.deinterleave2(n)
        out.append("%d %d" % (a, b))
    elif op == "dl3":
        n = int(f[1])
        out.append("== dl3 %d" % n)
        a, b, c = m.deinterleave3(n)
        out.append("%d %d %d" % (a, b, c))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
