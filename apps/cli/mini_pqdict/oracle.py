#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored `pqdict` library and writes
expected.out. See mk.py for the op grammar.

`new` starts a fresh pqdict (min = default, max = reverse=True). Every printing
op appends one line; an operation that raises KeyError or Empty prints `ERR`.
mini_pqdict.kara reproduces this byte-for-byte."""
import sys

sys.path.insert(0, "vendor")
from pqdict import pqdict, Empty  # noqa: E402

pq = None
out = []

for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    a = arg.split(" ") if arg else []
    try:
        if op == "new":
            pq = pqdict(reverse=(arg == "max"))
        elif op == "set":
            pq[a[0]] = int(a[1])
        elif op == "add":
            pq.additem(a[0], int(a[1]))
        elif op == "upd":
            pq.updateitem(a[0], int(a[1]))
        elif op == "del":
            del pq[a[0]]
        elif op == "pop":
            k, v = pq.popitem()
            out.append("%s %d" % (k, v))
        elif op == "top":
            k, v = pq.topitem()
            out.append("%s %d" % (k, v))
        elif op == "get":
            out.append("%d" % pq[a[0]])
        elif op == "has":
            out.append("yes" if a[0] in pq else "no")
        elif op == "len":
            out.append("%d" % len(pq))
        elif op == "pushpop":
            k, v = pq.pushpopitem(a[0], int(a[1]))
            out.append("%s %d" % (k, v))
        elif op == "swap":
            pq.swap_priority(a[0], a[1])
        elif op == "rekey":
            pq.replace_key(a[0], a[1])
        elif op == "drain":
            out.append(" ".join("%s:%d" % (k, v) for k, v in pq.popitems()))
        else:
            raise SystemExit("unknown op %r" % op)
    except (KeyError, Empty):
        out.append("ERR")

sys.stdout.write("\n".join(out) + "\n")
