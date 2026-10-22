#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored base62 library and writes
expected.out. See mk.py for the op table."""
import sys
sys.path.insert(0, "vendor")
import base62  # noqa: E402

INV = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def hx(bs):
    return "".join("%02x" % b for b in bs)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "e":
        out.append(base62.encode(int(f[1])))
    elif op == "em":
        out.append(base62.encode(int(f[1]), minlen=int(f[2])))
    elif op == "ei":
        out.append(base62.encode(int(f[1]), charset=INV))
    elif op == "d":
        try:
            out.append(str(base62.decode(f[1])))
        except ValueError:
            out.append("ERR")
    elif op == "di":
        try:
            out.append(str(base62.decode(f[1], charset=INV)))
        except ValueError:
            out.append("ERR")
    elif op == "eb":
        out.append(base62.encodebytes(bytes.fromhex(f[1])))
    elif op == "db":
        out.append(hx(base62.decodebytes(f[1])))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
