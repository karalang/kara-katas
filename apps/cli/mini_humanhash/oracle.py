#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored humanhash library and writes
expected.out: one hyphen-joined human-readable rendering per `h <words>
<hexdigest>` job. See mk.py."""
import sys
sys.path.insert(0, "vendor")
from humanhash import humanize  # noqa: E402

out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    if f[0] == "h":
        out.append(humanize(f[2], words=int(f[1])))
    else:
        raise SystemExit("unknown op %r" % f[0])

sys.stdout.write("\n".join(out) + "\n")
