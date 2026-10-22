#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored toposort library and writes
expected.out. See mk.py for the op table and graphspec format.

  l <spec> -> toposort levels, each level's items sorted and ",".joined,
              levels " | ".joined; "ERR" on CircularDependencyError.
  f <spec> -> toposort_flatten(data, sort=True), space-joined; "ERR" on cycle.

A circular dependency is reported with the bare token "ERR" rather than
CircularDependencyError's message, which embeds a set repr with per-process
iteration order; see README.md."""
import sys
sys.path.insert(0, "vendor")
import toposort as lib  # noqa: E402


def parse_spec(spec):
    d = {}
    if spec == "":
        return d
    for entry in spec.split(";"):
        if entry == "":
            continue
        key, _, depstr = entry.partition(":")
        d[key] = set(x for x in depstr.split(",") if x != "")
    return d


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, spec = line.partition("\t")
    data = parse_spec(spec)
    if op == "l":
        try:
            levels = list(lib.toposort(data))
            out.append(" | ".join(",".join(sorted(s)) for s in levels))
        except lib.CircularDependencyError:
            out.append("ERR")
    elif op == "f":
        try:
            out.append(" ".join(lib.toposort_flatten(data, sort=True)))
        except lib.CircularDependencyError:
            out.append("ERR")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
