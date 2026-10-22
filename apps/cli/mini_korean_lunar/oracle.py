#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored korean_lunar_calendar library and
writes expected.out. See mk.py for the op table.

  s2l -> setSolarDate then LunarIsoFormat(), or "INVALID".
  l2s -> setLunarDate then SolarIsoFormat(), or "INVALID".
  gap/cgap -> setSolarDate then getGapJaString()/getChineseGapJaString(), or
              "INVALID". The gapja strings carry CJK characters (UTF-8)."""
import sys
sys.path.insert(0, "vendor")
from korean_lunar_calendar import KoreanLunarCalendar  # noqa: E402

out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    p = [int(x) for x in arg.split()]
    k = KoreanLunarCalendar()
    if op == "s2l":
        out.append(k.LunarIsoFormat() if k.setSolarDate(p[0], p[1], p[2]) else "INVALID")
    elif op == "l2s":
        out.append(k.SolarIsoFormat() if k.setLunarDate(p[0], p[1], p[2], bool(p[3])) else "INVALID")
    elif op == "gap":
        out.append(k.getGapJaString() if k.setSolarDate(p[0], p[1], p[2]) else "INVALID")
    elif op == "cgap":
        out.append(k.getChineseGapJaString() if k.setSolarDate(p[0], p[1], p[2]) else "INVALID")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
