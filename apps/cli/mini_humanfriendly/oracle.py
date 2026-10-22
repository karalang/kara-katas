#!/usr/bin/env python3
"""Runs data/jobs.tsv through humanfriendly and prints expected.out.

Each job prints "== " and its fields joined by " | ", then a two-space
result line: the formatted string, the parsed number, True/False, or
err=<message> with the library's exact exception text.

Numbers returned by parse_length / parse_timespan are presented through
num_str (an integer when integral, else a fixed 6-decimal form stripped of
trailing zeros) so the harness never depends on Python's float repr;
parse_size already returns an int. This presentation is the harness's; the
computation is the library's.
"""
import sys

sys.path.insert(0, "vendor")
import humanfriendly as hf  # noqa: E402


def num_str(x):
    if isinstance(x, int) or (isinstance(x, float) and x.is_integer()):
        return str(int(x))
    return ("%.6f" % x).rstrip("0").rstrip(".")


def run(f):
    k = f[0]
    try:
        if k == "size_fmt":
            return [hf.format_size(int(f[1]), keep_width=f[3] == "1", binary=f[2] == "1")]
        if k == "size_parse":
            return [str(hf.parse_size(f[1], binary=f[2] == "1"))]
        if k == "len_fmt":
            return [hf.format_length(float(f[1]), keep_width=f[2] == "1")]
        if k == "len_parse":
            return [num_str(hf.parse_length(f[1]))]
        if k == "time_fmt":
            return [hf.format_timespan(int(f[1]), detailed=f[2] == "1", max_units=int(f[3]))]
        if k == "time_parse":
            return [num_str(hf.parse_timespan(f[1]))]
        if k == "num":
            return [hf.format_number(int(f[1]), num_decimals=int(f[2]))]
        if k == "round":
            return [hf.round_number(float(f[1]), keep_width=f[2] == "1")]
        if k == "bool":
            return [str(hf.coerce_boolean(f[1]))]
    except (hf.InvalidSize, hf.InvalidLength, hf.InvalidTimespan, ValueError) as e:
        return ["err=" + str(e)]
    raise SystemExit("unknown job: " + k)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        for r in run(f):
            out.append("  " + r)
sys.stdout.write("\n".join(out) + "\n")
