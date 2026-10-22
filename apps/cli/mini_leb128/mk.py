#!/usr/bin/env python3
"""Writes data/jobs.tsv for mini_leb128. Four ops, tab-separated:
  ue <dec>   unsigned-encode the decimal value -> hex bytes
  ud <hex>   unsigned-decode the hex bytes     -> decimal value
  se <dec>   signed-encode   the decimal value -> hex bytes
  sd <hex>   signed-decode   the hex bytes      -> decimal value
The decode jobs carry a valid encoding produced by the pure encoders below (no
library import here); oracle.py replays every job against the real leb128
library. See oracle.py / README.md."""
import os
os.makedirs("data", exist_ok=True)


def u_encode(x):
    r = []
    while True:
        b = x & 0x7f
        x = x >> 7
        if x == 0:
            r.append(b)
            return r
        r.append(0x80 | b)


def i_encode(x):
    r = []
    while True:
        b = x & 0x7f
        x = x >> 7
        if (x == 0 and (b & 0x40) == 0) or (x == -1 and (b & 0x40) != 0):
            r.append(b)
            return r
        r.append(0x80 | b)


def hx(bs):
    return "".join("%02x" % b for b in bs)


u_vals = [0, 1, 63, 64, 100, 127, 128, 129, 255, 256, 300, 624485, 16383,
          16384, 2097151, 2097152, 1000000000, 1099511627776, 281474976710655,
          999999999999]
i_vals = [0, 1, -1, 63, 64, -63, -64, -65, 127, -128, -129, 128, 300, -300,
          624485, -624485, -123456, 1000000000, -1000000000, 1099511627775,
          -1099511627776, -2, 2, -2097152]

lines = []
for v in u_vals:
    lines.append("ue\t%d" % v)
for v in u_vals:
    lines.append("ud\t%s" % hx(u_encode(v)))
for v in i_vals:
    lines.append("se\t%d" % v)
for v in i_vals:
    lines.append("sd\t%s" % hx(i_encode(v)))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
