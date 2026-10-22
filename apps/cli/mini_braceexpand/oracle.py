#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored braceexpand, prints expected.out.

Output per pattern:
  == <pattern>  (<count>)
    <result>            one indented line per expansion
or, on an unbalanced pattern:
  == <pattern>
    !ERROR <message>
"""
import sys

sys.path.insert(0, "vendor")
from braceexpand import braceexpand, UnbalancedBracesError  # noqa: E402

out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        pat = line
        try:
            res = list(braceexpand(pat))
            out.append("== " + pat + "  (" + str(len(res)) + ")")
            for r in res:
                out.append("  " + r)
        except UnbalancedBracesError as e:
            out.append("== " + pat)
            out.append("  !ERROR " + str(e))

sys.stdout.write("\n".join(out) + "\n")
