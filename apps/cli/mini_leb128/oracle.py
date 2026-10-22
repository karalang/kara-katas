#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored leb128 library and writes
expected.out: for ue/se, the encoded bytes as lowercase hex; for ud/sd, the
decoded decimal integer. See mk.py."""
import sys
sys.path.insert(0, "vendor")
import leb128  # noqa: E402


def hx(bs):
    return "".join("%02x" % b for b in bs)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "ue":
        out.append(hx(leb128.u.encode(int(f[1]))))
    elif op == "ud":
        out.append(str(leb128.u.decode(bytearray.fromhex(f[1]))))
    elif op == "se":
        out.append(hx(leb128.i.encode(int(f[1]))))
    elif op == "sd":
        out.append(str(leb128.i.decode(bytearray.fromhex(f[1]))))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
