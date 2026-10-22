#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored packaging.version and prints
expected.out. mini_packaging.kara must reproduce this byte-for-byte on every
backend.

Each job is `<op>\t<payload>`:

  norm <version>     -> str(Version(version)), the canonical PEP 440 form, or
                        the literal INVALID when packaging raises InvalidVersion;
  cmp  <a>\x1f<b>     -> "<", "=" or ">" for the ordering of the two versions.
"""
import sys

sys.path.insert(0, "vendor")
from version import InvalidVersion, Version  # noqa: E402

US = "\x1f"


def run(op, payload):
    if op == "norm":
        try:
            return str(Version(payload))
        except InvalidVersion:
            return "INVALID"
    if op == "cmp":
        a, b = payload.split(US, 1)
        va, vb = Version(a), Version(b)
        if va < vb:
            return "<"
        if va > vb:
            return ">"
        return "="
    return "unknown op"


def main():
    chunks = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        op, payload = line.split("\t", 1)
        shown = payload.replace(US, " | ")
        chunks.append("== " + op + " " + shown + "\n  " + run(op, payload) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
