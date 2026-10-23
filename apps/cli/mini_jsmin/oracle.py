#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored jsmin library and writes
expected.out. Each input line is the lowercase hex of a JavaScript source
snippet; the job minifies the decoded source and prints:

    min <hex of the minified source>

mini_jsmin.kara reproduces this byte-for-byte on every backend."""
import sys

sys.path.insert(0, "vendor")
from jsmin import jsmin  # noqa: E402


def row(src):
    return "min " + jsmin(src).encode("ascii").hex()


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(row(bytes.fromhex(line).decode("ascii")))
    sys.stdout.write("\n".join(out) + "\n")


main()
