#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_ubjson: one encode or decode job per line.

    <op> \t <payload>

For every value below, two jobs are written: an `enc` whose payload is the
value as JSON, and a `dec` whose payload is the lowercase hex of the UBJSON
the library produces for that value (computed here, so the decode job is fed
real encoder output). Together they cover the integer-width ladder
(uint8 `U`, int8 `i`, int16 `I`, int32 `l`, int64 `L`), the one-byte-string
`C` CHAR vs the `S` STRING form, empty strings, and nested arrays and objects.
"""
import json
import os
import sys

sys.path.insert(0, "vendor")
import ubjson  # noqa: E402

VALUES = [
    None,
    True,
    False,
    0,
    1,
    255,
    256,
    300,
    32767,
    32768,
    70000,
    2147483647,
    2147483648,
    5000000000,
    -1,
    -128,
    -129,
    -300,
    -70000,
    -5000000000,
    "a",
    "",
    "hello",
    "hi there",
    [1, 2, 3],
    [True, None, "x"],
    [[1], [2, 3]],
    {"a": 1, "b": 2},
    {"name": "x", "vals": [1, 2]},
    {"u": {"v": 1}},
    {"id": 256, "tags": ["a", "bb"], "ok": True},
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for v in VALUES:
        fh.write("enc\t" + json.dumps(v, separators=(",", ":")) + "\n")
        fh.write("dec\t" + ubjson.dumpb(v).hex() + "\n")
