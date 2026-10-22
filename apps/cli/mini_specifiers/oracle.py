#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored packaging.specifiers and prints
expected.out. mini_specifiers.kara must reproduce this byte-for-byte.

Each job echoes a `== op | args` header and, indented, the result:
`contains` prints True/False; `filter` prints the surviving versions in order
(space-joined), or `(none)`.
"""
import sys

sys.path.insert(0, "vendor")
from packaging.specifiers import SpecifierSet  # noqa: E402

PRE = {"none": None, "true": True, "false": False}


def run(fields):
    op = fields[0]
    if op == "contains":
        spec, version, pre = fields[1], fields[2], fields[3]
        ss = SpecifierSet(spec)
        return "True" if ss.contains(version, prereleases=PRE[pre]) else "False"
    if op == "filter":
        spec, pre, verlist = fields[1], fields[2], fields[3]
        versions = verlist.split(",")
        ss = SpecifierSet(spec)
        out = list(ss.filter(versions, prereleases=PRE[pre]))
        return " ".join(out) if out else "(none)"
    return "unknown op"


def main():
    lines = open("data/jobs.tsv", encoding="utf-8").read().splitlines()
    chunks = []
    for line in lines:
        if not line:
            continue
        fields = line.split("\t")
        header = "== " + fields[0] + " | " + " ".join(fields[1:])
        chunks.append(header + "\n  " + run(fields) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
