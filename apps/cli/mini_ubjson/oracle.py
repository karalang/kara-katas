#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored py-ubjson and prints expected.out.
mini_ubjson.kara must reproduce this byte-for-byte on every backend.

Each job is `<op>\t<payload>`:

  enc <json>  → ubjson.dumpb(value).hex(): the UBJSON wire bytes, as lowercase
                hex, for the JSON value;
  dec <hex>   → json.dumps(ubjson.loadb(bytes.fromhex(hex))): the JSON value a
                UBJSON byte string decodes to.

The two ops are inverses, so each value appears as both an `enc` (from JSON)
and a `dec` (from the hex the library produced) — exercising the encoder's
integer-width choice and the decoder's marker dispatch over the same data.
"""
import json
import sys

sys.path.insert(0, "vendor")
import ubjson  # noqa: E402


def run(op, payload):
    if op == "enc":
        return ubjson.dumpb(json.loads(payload)).hex()
    if op == "dec":
        return json.dumps(ubjson.loadb(bytes.fromhex(payload)), separators=(", ", ": "))
    return "unknown op"


def main():
    chunks = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        op, payload = line.split("\t", 1)
        chunks.append("== " + op + " " + payload + "\n  " + run(op, payload) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
