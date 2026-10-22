#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored pyprobables CountMinSketch and
writes expected.out. All ops share ONE CountMinSketch(width=997, depth=5). See
mk.py for the op table.

  bins  -> the depth bin indices (val % width) + i*width, space-joined.
  add   -> CountMinSketch.add(key, n) (post-add query result).
  remove-> CountMinSketch.remove(key, n).
  check -> CountMinSketch.check(key).
  query -> set query_type; echo "query=<mode>"."""
import sys
sys.path.insert(0, "vendor")
from probables import CountMinSketch  # noqa: E402

WIDTH = 997
DEPTH = 5
c = CountMinSketch(width=WIDTH, depth=DEPTH)

out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    if op == "bins":
        hs = c.hashes(arg)
        out.append(" ".join(str((v % WIDTH) + i * WIDTH) for i, v in enumerate(hs)))
    elif op == "add":
        key, _, n = arg.partition(" ")
        out.append(str(c.add(key, int(n))))
    elif op == "remove":
        key, _, n = arg.partition(" ")
        out.append(str(c.remove(key, int(n))))
    elif op == "check":
        out.append(str(c.check(arg)))
    elif op == "query":
        c.query_type = arg
        out.append("query=%s" % arg)
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
