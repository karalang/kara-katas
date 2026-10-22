#!/usr/bin/env python3
"""Writes data/jobs.tsv for mini_hashids.

Each line is: op \t min_length \t payload

  enc  min_length  "v1 v2 ..."   -> encode those ids
  dec  min_length  "<hashid>"    -> decode that hashid

The dec hashids are produced here by the vendored library so the Kara port
need only decode a literal string; one deliberately-invalid dec exercises the
re-encode verification that makes decode return nothing.
"""
import os
import sys

sys.path.insert(0, "vendor")
from hashids import Hashids  # noqa: E402

SALT = "this is my salt"

# (min_length, [values]) encode specs; each also yields a matching dec job.
SPECS = [
    (0, [1, 2, 3]),
    (0, [12345]),
    (0, [683]),
    (0, [1, 2, 3, 4, 5, 6]),
    (0, [2147483647]),
    (0, [0]),
    (8, [1]),
    (16, [1, 23, 456]),
    (12, [1234567]),
    (10, [7, 7, 7]),
]

os.makedirs("data", exist_ok=True)
rows = []
for ml, vals in SPECS:
    payload = " ".join(str(v) for v in vals)
    rows.append("enc\t%d\t%s" % (ml, payload))
    h = Hashids(salt=SALT, min_length=ml).encode(*vals)
    rows.append("dec\t%d\t%s" % (ml, h))

# A string with a character outside the working alphabet -> decode yields nothing.
rows.append("dec\t0\t!bad!")

with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(rows) + "\n")
