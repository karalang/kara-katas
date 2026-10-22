#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored jdcal library and writes
expected.out. See mk.py for the op table.

  g/j  -> int(jd2), the Modified Julian Date (jd1 is always MJD_0).
  rg/rj -> "y|m|d" from jd2gcal/jd2jcal; the conversions are date-only, so the
           fractional day the library returns is always 0.0 and is dropped.
  leap -> "1" or "0"."""
import sys
sys.path.insert(0, "vendor")
import jdcal  # noqa: E402

out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    parts = [int(x) for x in arg.split()]
    if op == "g":
        out.append("%d" % int(jdcal.gcal2jd(parts[0], parts[1], parts[2])[1]))
    elif op == "j":
        out.append("%d" % int(jdcal.jcal2jd(parts[0], parts[1], parts[2])[1]))
    elif op == "rg":
        y, m, d, f = jdcal.jd2gcal(jdcal.MJD_0, parts[0])
        out.append("%d|%d|%d" % (y, m, d))
    elif op == "rj":
        y, m, d, f = jdcal.jd2jcal(jdcal.MJD_0, parts[0])
        out.append("%d|%d|%d" % (y, m, d))
    elif op == "leap":
        out.append("1" if jdcal.is_leap(parts[0]) else "0")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
