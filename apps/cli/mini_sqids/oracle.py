#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored sqids library and writes
expected.out, one line per job:

    new(<alphabet>, <min_length>, <blocklist>) => ok | <Error>: <message>
    encode(<n, n, ...>) => [<id>] | <Error>: <message>
    decode(<id>) => [<n>, <n>, ...]

"-" in a new() line is the library default (DEFAULT_ALPHABET and
DEFAULT_BLOCKLIST themselves, so the library takes its pre-filtered
blocklist path). Run: python3 -I oracle.py > expected.out"""
import sys

sys.path.insert(0, "vendor")
import sqids  # noqa: E402
from sqids.constants import DEFAULT_ALPHABET, DEFAULT_BLOCKLIST  # noqa: E402

cur = None
out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if line == "":
        continue
    f = line.split("\t")
    op = f[0]
    if op == "new":
        alphabet = DEFAULT_ALPHABET if f[1] == "-" else f[1]
        blocklist = DEFAULT_BLOCKLIST if f[3] == "-" else (f[3].split(",") if f[3] else [])
        try:
            cur = sqids.Sqids(alphabet, int(f[2]), blocklist)
            res = "ok"
        except Exception as e:  # noqa: BLE001
            cur = None
            res = "%s: %s" % (type(e).__name__, e)
        out.append("new(%s, %s, %s) => %s" % (f[1], f[2], f[3], res))
    elif op == "enc":
        nums = [int(x) for x in f[1].split(",")] if f[1] else []
        try:
            res = "[" + cur.encode(nums) + "]"
        except Exception as e:  # noqa: BLE001
            res = "%s: %s" % (type(e).__name__, e)
        out.append("encode(%s) => %s" % (", ".join(str(n) for n in nums), res))
    elif op == "dec":
        res = cur.decode(f[1])
        out.append("decode(%s) => [%s]" % (f[1], ", ".join(str(n) for n in res)))
sys.stdout.write("\n".join(out) + "\n")
