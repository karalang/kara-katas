#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored pathvalidate, prints expected.out.

Target platform is Windows. Output per job:
  == <op> | <displayed-arg>
    validate -> OK  or  <PVxxxx> <REASON_NAME>
    sanitize -> [<sanitized>]

The arg is shown with control bytes escaped as \xNN so the header is printable
and unambiguous; the sanitized result is wrapped in [ ] so trailing spaces and
empty results are visible.
"""
import sys

sys.path.insert(0, "vendor")
from pathvalidate import sanitize_filename, validate_filename, ValidationError  # noqa: E402

PLATFORM = "Windows"


def disp(s):
    out = []
    for ch in s:
        o = ord(ch)
        if o < 32 or o == 127:
            out.append("\\x%02x" % o)
        else:
            out.append(ch)
    return "".join(out)


def run(op, arg):
    if op == "validate":
        try:
            validate_filename(arg, platform=PLATFORM)
            return "OK"
        except ValidationError as e:
            return e.reason.code + " " + e.reason.name
    if op == "sanitize":
        return "[" + sanitize_filename(arg, platform=PLATFORM) + "]"
    return "?"


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        f = line.split("\t")
        op = f[0]
        arg = f[1] if len(f) > 1 else ""
        out.append("== " + op + " | " + disp(arg))
        out.append("  " + run(op, arg))

sys.stdout.write("\n".join(out) + "\n")
