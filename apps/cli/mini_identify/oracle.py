#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored identify, prints expected.out.

Each job is tab-separated: an op name and one argument. Output per job:
  == <op> | <arg>
    <result>

tags_from_filename / tags_from_interpreter return sets, so their tags are
printed sorted (space-joined, or `(none)` when empty). parse_shebang returns a
tuple, printed in order (or `(none)` when empty).
"""
import io
import sys

sys.path.insert(0, "vendor")
from identify.identify import (  # noqa: E402
    parse_shebang,
    tags_from_filename,
    tags_from_interpreter,
)


def fmt_set(s):
    return " ".join(sorted(s)) if s else "(none)"


def fmt_tuple(t):
    return " ".join(t) if t else "(none)"


def run(op, arg):
    if op == "filename":
        return fmt_set(tags_from_filename(arg))
    if op == "interpreter":
        return fmt_set(tags_from_interpreter(arg))
    if op == "shebang":
        return fmt_tuple(parse_shebang(io.BytesIO(arg.encode("UTF-8"))))
    if op == "shebang_tags":
        cmd = parse_shebang(io.BytesIO(arg.encode("UTF-8")))
        return fmt_set(tags_from_interpreter(cmd[0])) if cmd else "(none)"
    raise SystemExit("unknown op: " + op)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        op, arg = line.split("\t")
        out.append("== " + op + " | " + arg)
        out.append("  " + run(op, arg))

sys.stdout.write("\n".join(out) + "\n")
