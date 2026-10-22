#!/usr/bin/env python3
"""Writes data/jobs.tsv for mini_base62 (tab-separated ops):
  e  <n>            encode integer n (default charset)       -> base62 string
  em <n> <minlen>   encode integer n, zero-padded to minlen  -> base62 string
  ei <n>            encode integer n with the inverted charset -> base62 string
  d  <s>            decode a base62 string (default charset)  -> integer, or ERR
  di <s>            decode with the inverted charset          -> integer, or ERR
  eb <hex>          encodebytes: base62 of the big-endian bytes -> base62 string
  db <s>            decodebytes: base62 string -> bytes, as lowercase hex
`db` inputs are produced by mk.py's own pure byte encoder (no library import);
oracle.py replays every job against the vendored base62 library. See README.md."""
import os
os.makedirs("data", exist_ok=True)

DEF = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def da_divmod62(digits):
    out, carry = [], 0
    for d in digits:
        cur = carry * 256 + d
        out.append(cur // 62)
        carry = cur % 62
    i = 0
    while i < len(out) - 1 and out[i] == 0:
        i += 1
    return out[i:], carry


def enc_bytes(bs):
    digits = list(bs) if bs else [0]
    if not any(d != 0 for d in digits):
        return "0"
    chs = []
    cur = digits
    while not (len(cur) == 1 and cur[0] == 0):
        cur, r = da_divmod62(cur)
        chs.append(DEF[r])
    chs.reverse()
    return "".join(chs)


ints = [0, 1, 61, 62, 63, 100, 255, 256, 1000, 123456789,
        9223372036854775807, 34, 3843, 3844, 238327, 238328]
bytestrs = ["01", "ff", "0001", "68656c6c6f", "deadbeef",
            "000102030405060708090a0b0c0d0e0f10111213",
            "000005", "ffffffffffffffffffff",
            "74686520717569636b2062726f776e20666f78206a756d7073"]

lines = []
for n in ints:
    lines.append("e\t%d" % n)
for n in ints:
    lines.append("em\t%d\t5" % n)
for n in [0, 1, 61, 999, 123456789]:
    lines.append("ei\t%d" % n)
# decode round-trips: encode here (pure) is not needed; feed known base62 forms
for n in ints:
    # build the default-charset encoding with the integer path (pure)
    m, chs = n, []
    while m > 0:
        chs.append(DEF[m % 62]); m //= 62
    s = "".join(reversed(chs)) or "0"
    lines.append("d\t%s" % s)
lines.append("d\t0z1A")          # the 0z prefix is stripped
lines.append("d\t!!")            # invalid char -> ERR
lines.append("d\t A")            # space not in charset -> ERR
for n in [0, 1, 61, 999]:
    m, chs = n, []
    INV = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while m > 0:
        chs.append(INV[m % 62]); m //= 62
    lines.append("di\t%s" % ("".join(reversed(chs)) or "0"))
for h in bytestrs:
    lines.append("eb\t%s" % h)
for h in bytestrs:
    lines.append("db\t%s" % enc_bytes(bytes.fromhex(h)))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
