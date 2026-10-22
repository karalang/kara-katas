#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored orderedmultidict.omdict and writes
expected.out. See mk.py for the op table. The vendored library (and its one
dependency, six) are pure Python, so oracle.py runs exactly the code
mini_omdict.kara mirrors."""
import sys

sys.path.insert(0, "vendor")
from orderedmultidict import omdict  # noqa: E402


def fmt_items(pairs):
    return "[" + ", ".join("(%s %d)" % (k, v) for k, v in pairs) + "]"


def fmt_keys(ks):
    return "[" + ", ".join(str(k) for k in ks) + "]"


def fmt_vals(vs):
    return "[" + ", ".join(str(v) for v in vs) + "]"


def csv_ints(s):
    return [int(x) for x in s.split(",")] if s else []


o = omdict()
out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "a":
        o.add(f[1], int(f[2]))
        out.append(fmt_items(o.allitems()))
    elif op == "al":
        o.addlist(f[1], csv_ints(f[2]))
        out.append(fmt_items(o.allitems()))
    elif op == "s":
        o.set(f[1], int(f[2]))
        out.append(fmt_items(o.allitems()))
    elif op == "sl":
        o.setlist(f[1], csv_ints(f[2]))
        out.append(fmt_items(o.allitems()))
    elif op == "rv":
        o.reverse()
        out.append(fmt_items(o.allitems()))
    elif op == "g":
        v = o.get(f[1], None)
        out.append("miss" if v is None else str(v))
    elif op == "gl":
        out.append(fmt_vals(o.getlist(f[1])))
    elif op == "p":
        try:
            out.append(str(o.pop(f[1])))
        except KeyError:
            out.append("miss")
    elif op == "pl":
        try:
            out.append(fmt_vals(o.poplist(f[1])))
        except KeyError:
            out.append("miss")
    elif op == "pv":
        try:
            out.append(str(o.popvalue(f[1], last=True)))
        except KeyError:
            out.append("miss")
    elif op == "pf":
        try:
            out.append(str(o.popvalue(f[1], last=False)))
        except KeyError:
            out.append("miss")
    elif op == "h":
        out.append("yes" if o.has_key(f[1]) else "no")
    elif op == "l":
        out.append(str(o.size()))
    elif op == "ks":
        out.append(fmt_keys(o.keys()))
    elif op == "vs":
        out.append(fmt_vals(o.values()))
    elif op == "it":
        out.append(fmt_items(o.items()))
    elif op == "ai":
        out.append(fmt_items(o.allitems()))
    elif op == "ak":
        out.append(fmt_keys(o.allkeys()))
    elif op == "av":
        out.append(fmt_vals(o.allvalues()))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
