#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored hashids, prints expected.out.

Output per job:
  == <op> | <min_length> | <payload>
    <result>

enc result is the hashid string; dec result is the space-joined decoded ids,
or "[]" when decode returns nothing.
"""
import sys

sys.path.insert(0, "vendor")
from hashids import Hashids  # noqa: E402

SALT = "this is my salt"


def run(op, ml, payload):
    h = Hashids(salt=SALT, min_length=ml)
    if op == "enc":
        vals = [int(x) for x in payload.split()] if payload else []
        return h.encode(*vals)
    if op == "dec":
        nums = h.decode(payload)
        if not nums:
            return "[]"
        return " ".join(str(n) for n in nums)
    return "?"


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        op = f[0]
        ml = int(f[1])
        payload = f[2] if len(f) > 2 else ""
        out.append("== " + " | ".join([op, str(ml), payload]))
        out.append("  " + run(op, ml, payload))

sys.stdout.write("\n".join(out) + "\n")
