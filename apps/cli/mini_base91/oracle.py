#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored base91 library and writes
expected.out. See mk.py for the op table."""
import sys
sys.path.insert(0, "vendor")
import base91  # noqa: E402


def hx(bs):
    return "".join("%02x" % b for b in bs)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    if op == "e":
        out.append(base91.encode(bytearray.fromhex(arg)))
    elif op == "d":
        out.append(hx(base91.decode(arg)))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
