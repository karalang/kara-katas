#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored titlecase, prints expected.out.

Output per line:
  == titlecase | <phrase>
    <title-cased phrase>
"""
import sys

sys.path.insert(0, "vendor")
from titlecase_lib import titlecase  # noqa: E402


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        out.append("== titlecase | " + line)
        out.append("  " + titlecase(line))

sys.stdout.write("\n".join(out) + "\n")
