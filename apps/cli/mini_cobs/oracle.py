#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored cobs / cobsr and writes expected.out.

For each `<op>\t<hex>` job it prints a header line

    == <op> <hex>

then the result: for an `enc` job the encoded frame as hex; for a `dec` job
either `ok <hex>` (the decoded payload) or `err <message>` where <message> is
the vendored DecodeError text. mini_cobs.kara reproduces this stream exactly.
"""
import sys

sys.path.insert(0, "vendor")
from cobs import cobs, cobsr  # noqa: E402


def run(op, raw):
    if op == "cobs_enc":
        return cobs.encode(raw).hex()
    if op == "cobsr_enc":
        return cobsr.encode(raw).hex()
    if op == "cobs_dec":
        try:
            return "ok " + cobs.decode(raw).hex()
        except cobs.DecodeError as e:
            return "err " + str(e)
    if op == "cobsr_dec":
        try:
            return "ok " + cobsr.decode(raw).hex()
        except cobsr.DecodeError as e:
            return "err " + str(e)
    raise SystemExit("unknown op %r" % op)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    if not line:
        continue
    op, hexstr = line.split("\t")
    raw = bytes.fromhex(hexstr)
    out.append("== %s %s" % (op, hexstr))
    out.append(run(op, raw))

sys.stdout.write("\n".join(out) + "\n")
