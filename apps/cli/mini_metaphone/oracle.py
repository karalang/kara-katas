#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored Metaphone library and writes
expected.out: one `primary|secondary` line per `dm <word>` job. See mk.py."""
import sys
sys.path.insert(0, "vendor")
from metaphone import doublemetaphone  # noqa: E402

out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    if f[0] == "dm":
        p, s = doublemetaphone(f[1])
        out.append(p + "|" + s)
    else:
        raise SystemExit("unknown op %r" % f[0])

sys.stdout.write("\n".join(out) + "\n")
