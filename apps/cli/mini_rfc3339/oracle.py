#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored rfc3339-validator, prints expected.out.

Output per line:
  == validate | <timestamp>
    true   or   false
"""
import sys

sys.path.insert(0, "vendor")
from rfc3339_validator import validate_rfc3339  # noqa: E402


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        ok = validate_rfc3339(line)
        out.append("== validate | " + line)
        out.append("  " + ("true" if ok else "false"))

sys.stdout.write("\n".join(out) + "\n")
