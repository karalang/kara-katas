#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_duration (tab-separated ops):
  p <durstr>    parse a Go-style duration string -> timedelta days|seconds|us,
                or ERR if the library rejects it
  f <micro>     format timedelta(microseconds=<int>)            (default units)
  fe <micro>    format timedelta(microseconds=<int>), extended  (y/mm/d broken out)
mk.py writes only literal inputs (no library import); oracle.py replays every
job against the vendored durationpy library. Inputs are kept to the exact-integer
subset the port covers (whole-microsecond parse results, whole-component format
outputs); see README.md for the documented boundaries."""
import os
os.makedirs("data", exist_ok=True)

parse_inputs = [
    "0", "+0", "-0",
    "1s", "90m", "1h30m", "2h45m", "1.5h", "0.25h", "100ms", "250us",
    "1d", "2w", "1y", "3mm", "500ms", "1h", "+2h", "-3d", "1w2d3h4m5s",
    "12h", "36h", "2d5h30m", "750ms", "10s", "59m59s",
    "24h", "48h", "1000ms", "1500ms", "5m", "-1h30m", "+90m",
    # rejections -> ERR
    "", "abc", "1x", "1h2", "h", "1.2.3s", "10 s", "1h ", " 1h",
    "1z", "100", "ns",
]

# (microseconds, extended)
fmt_inputs = [
    (0, False), (1000000, False), (90000000, False), (5400000000, False),
    (3600000000, False), (500000, False), (250, False), (1000, False),
    (86400000000, False), (86400000000, True), (172800000000, True),
    (31536000000000, True), (2592000000000, True), (45000000000, False),
    (3900000000, False), (1000000000, False), (60000000, False),
    (750000, False), (999000, False), (999000000, False),
    (213000000000, True), (213000000000, False),
]

lines = []
for s in parse_inputs:
    lines.append("p\t%s" % s)
for (mi, ext) in fmt_inputs:
    lines.append("%s\t%d" % ("fe" if ext else "f", mi))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
