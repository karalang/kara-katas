#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_probables (tab-separated: op then arg). All
ops act on ONE shared CountMinSketch(width=997, depth=5), in order:
  bins   <key>          print the depth bin indices for <key> (space-joined)
  add    <key> <n>      add <key> n times; print the post-add query result
  remove <key> <n>      remove <key> n times; print the post-remove query result
  check  <key>          print the current query result for <key>
  query  <mode>         set the estimator (min | mean | mean-min); print "query=<mode>"
mk.py writes only literal inputs (no library import); oracle.py replays every job
against the vendored pyprobables library. Keys are ASCII. See README.md."""
import os
import random
os.makedirs("data", exist_ok=True)

KEYS = ["hello", "world", "foo", "bar", "baz", "alpha", "beta", "the", "quick",
        "brown", "fox", "a", "bb", "ccc", "test123", "zzz"]

lines = []
# a direct check of the hash -> bin indexing for every key
for k in KEYS:
    lines.append("bins\t%s" % k)

# a deterministic stream, replayed under each estimator (state accumulates)
random.seed(1)
script = []
for _ in range(120):
    op = random.choice(["add", "add", "add", "check", "remove"])
    k = random.choice(KEYS)
    n = random.choice([1, 1, 2, 3, 5, 10])
    script.append((op, k, n))

for mode in ["min", "mean", "mean-min"]:
    lines.append("query\t%s" % mode)
    for (op, k, n) in script:
        if op == "check":
            lines.append("check\t%s" % k)
        else:
            lines.append("%s\t%s %d" % (op, k, n))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
