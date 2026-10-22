#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored datauri library and writes
expected.out. See mk.py for the op table and output format."""
import sys
sys.path.insert(0, "vendor")
from datauri import parse, discover, DataURIError  # noqa: E402


def hx(bs):
    return "".join("%02x" % b for b in bs)


def item(p):
    mt = p.media_type if p.media_type is not None else "-"
    return mt + "|" + hx(p.data)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    if op == "p":
        try:
            p = parse(arg)
            out.append(item(p) + "|" + repr(p))
        except DataURIError as e:
            out.append("ERR " + str(e))
    elif op == "d":
        results = list(discover(arg))
        parts = [str(len(results))] + [item(r) for r in results]
        out.append(" ".join(parts))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
