#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored baseconv, prints expected.out.

Output per line:
  == <op> <base> | <value>
    <result>            (or `ValueError: invalid digit "X"`)
"""
import sys

sys.path.insert(0, "vendor")
from baseconv import (  # noqa: E402
    BaseConverter,
    base2,
    base16,
    base36,
    base56,
    base58,
    base62,
    base64,
)

CONV = {
    "base2": base2,
    "base16": base16,
    "base36": base36,
    "base56": base56,
    "base58": base58,
    "base62": base62,
    "base64": base64,
    "myconv": BaseConverter("MyOwnAlphabet0123456"),
    "altsign": BaseConverter("abcd-", sign="$"),
}

out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        op, base, value = line.split("\t")
        out.append("== " + op + " " + base + " | " + value)
        conv = CONV[base]
        try:
            if op == "encode":
                res = conv.encode(value)
            else:
                res = conv.decode(value)
        except ValueError as e:
            res = "ValueError: " + str(e)
        out.append("  " + res)

sys.stdout.write("\n".join(out) + "\n")
