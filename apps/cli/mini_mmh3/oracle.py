#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored pymmh3 and prints expected.out.
mini_mmh3.kara must reproduce this byte-for-byte on every backend.

Each job is `<op>\t<seed>\t<text>`. The output is:

  == <op> <seed> <text>
  <result>

For `h32` the result is MurmurHash3 x86_32 as a signed 32-bit decimal (the
value mmh3.hash returns). For `h128` it is the x86 128-bit hash as 32 lowercase
hex digits (big-endian over the h4,h3,h2,h1 lanes, i.e. `%032x` of the integer
pymmh3.hash128(..., x64arch=False) returns).
"""
import sys

sys.path.insert(0, "vendor")
import pymmh3  # noqa: E402


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        op, seed_s, text = line.split("\t", 2)
        seed = int(seed_s)
        out.append("== " + op + " " + seed_s + " " + text + "\n")
        if op == "h32":
            out.append("%d\n" % pymmh3.hash(text, seed))
        else:
            out.append("%032x\n" % pymmh3.hash128(text, seed, False))
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
