#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored `genson` library and writes
expected.out. Each line is a tab-separated list of JSON sample documents; they
are fed to one SchemaBuilder via add_object and the inferred schema is printed
as JSON (the library's own to_json(), default settings). mini_genson.kara
reproduces this byte-for-byte on every backend.

Only the add_object inference path is exercised; the add_schema merge path and
the Enum strategy are out of scope (see README)."""
import sys
import json

sys.path.insert(0, "vendor")
from genson import SchemaBuilder  # noqa: E402


def run_line(fields):
    b = SchemaBuilder()
    for doc in fields:
        b.add_object(json.loads(doc))
    return b.to_json()


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(run_line(line.split("\t")))
    sys.stdout.write("\n".join(out) + "\n")


main()
