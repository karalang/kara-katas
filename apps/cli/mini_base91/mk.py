#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_base91 (tab-separated ops):
  e <hex>   encode the bytes given as hex -> a Base91 string
  d <str>   decode a Base91 string        -> the bytes, as lowercase hex
mk.py produces the `d` inputs with its own pure Base91 encoder (no library
import); oracle.py replays every job against the vendored base91 library. The
Base91 alphabet contains no tab or newline, so every value is one TSV field.
See README.md."""
import os
os.makedirs("data", exist_ok=True)

ALPHA = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
         "!#$%&()*+,./:;<=>?@[]^_`{|}~\"")


def encode(data):
    b = 0
    n = 0
    out = []
    for byte in data:
        b |= byte << n
        n += 8
        if n > 13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            out.append(ALPHA[v % 91])
            out.append(ALPHA[v // 91])
    if n:
        out.append(ALPHA[b % 91])
        if n > 7 or b > 90:
            out.append(ALPHA[b // 91])
    return "".join(out)


hexes = [
    "", "00", "01", "ff", "0001", "48656c6c6f", "deadbeef",
    "000102030405060708090a0b0c0d0e0f",
    "54686520717569636b2062726f776e20666f78206a756d7073",
    "ffffffffffffffff", "7f8081", "abcdef0123456789", "0a0d0900",
    "6d616e2069732064697374696e677569736865642c206e6f74206f6e6c79",
]

lines = []
for h in hexes:
    lines.append("e\t%s" % h)
# decode jobs: round-trip the same payloads, plus inputs with skipped junk chars
for h in hexes:
    lines.append("d\t%s" % encode(bytes.fromhex(h)))
lines.append("d\t %s " % encode(b"Hi"))              # surrounding spaces skipped
lines.append("d\t%s    " % encode(b"ok"))             # trailing spaces skipped

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
