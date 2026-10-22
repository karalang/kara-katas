#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored durationpy library and writes
expected.out. See mk.py for the op table.

  p <durstr> -> "days|seconds|microseconds" (timedelta's three integer fields),
                or the canonical token "ERR" if durationpy rejects the string.
  f/fe <us>  -> durationpy.to_str(timedelta(microseconds=us), extended=...).

The port reports a rejection with the bare token "ERR" rather than durationpy's
exact DurationError message (the message embeds the original string and its
classification follows Python regex semantics); see README.md."""
import sys
import datetime
sys.path.insert(0, "vendor")
import durationpy  # noqa: E402

out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    if op == "p":
        try:
            td = durationpy.from_str(arg)
            out.append("%d|%d|%d" % (td.days, td.seconds, td.microseconds))
        except durationpy.DurationError:
            out.append("ERR")
    elif op in ("f", "fe"):
        td = datetime.timedelta(microseconds=int(arg))
        out.append(durationpy.to_str(td, extended=(op == "fe")))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
