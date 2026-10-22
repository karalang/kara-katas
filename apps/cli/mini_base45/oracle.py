#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored base45 library and writes
expected.out: for `enc <hex>`, the Base45 string; for `dec <base45>`, the
decoded bytes as lowercase hex, or ERR when the string is not valid Base45.
See mk.py."""
import sys
sys.path.insert(0, "vendor")
from base45 import b45encode, b45decode  # noqa: E402


def hx(bs):
    return "".join("%02x" % b for b in bs)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    if f[0] == "enc":
        buf = bytes.fromhex(f[1])
        out.append(b45encode(buf).decode())
    elif f[0] == "dec":
        try:
            out.append(hx(b45decode(f[1])))
        except ValueError:
            out.append("ERR")
    else:
        raise SystemExit("unknown op %r" % f[0])

sys.stdout.write("\n".join(out) + "\n")
