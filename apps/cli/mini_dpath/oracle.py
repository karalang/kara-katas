#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored dpath and prints expected.out.
mini_dpath.kara must reproduce this byte-for-byte on every backend.

Each job is `<op> <glob> <doc>`. `search` prints the matching (path, value)
pairs, `values` the matching values, and `get` the single addressed value or
its error name. Values are serialized with json.dumps' default separators.
"""
import json
import sys

sys.path.insert(0, "vendor")
import dpath  # noqa: E402


def J(v):
    return json.dumps(v, separators=(", ", ": "))


def run(fields):
    op, glob, doc = fields[0], fields[1], json.loads(fields[2])
    if op == "search":
        rs = list(dpath.search(doc, glob, yielded=True))
        return " | ".join(p + "=" + J(v) for p, v in rs) or "(none)"
    if op == "values":
        vs = dpath.values(doc, glob)
        return " | ".join(J(v) for v in vs) or "(none)"
    if op == "get":
        try:
            return J(dpath.get(doc, glob))
        except KeyError:
            return "KeyError"
        except ValueError:
            return "ValueError"
    return "unknown op"


def main():
    chunks = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        header = "== " + f[0] + " " + f[1] + " | " + f[2]
        chunks.append(header + "\n  " + run(f) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
