#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored jsonref and prints expected.out.
mini_jsonref.kara must reproduce this byte-for-byte on every backend.

Each job is `resolve <merge> <doc>`: the JSON document is parsed, every local
`{"$ref": "#/pointer"}` is resolved against it (eagerly, proxies=False), and
the result is serialized with json.dumps' default separators. A reference
that cannot be resolved prints `ERROR: <message>` exactly as JsonRefError
renders it.
"""
import json
import sys

sys.path.insert(0, "vendor")
import jsonref  # noqa: E402


def run(fields):
    merge = fields[1] == "1"
    doc = json.loads(fields[2])
    try:
        r = jsonref.replace_refs(doc, proxies=False, merge_props=merge)
        return json.dumps(r, separators=(", ", ": "))
    except jsonref.JsonRefError as e:
        return "ERROR: " + str(e)


def main():
    chunks = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        header = "== merge=" + f[1] + " | " + f[2]
        chunks.append(header + "\n  " + run(f) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
