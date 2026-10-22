#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored semver and prints expected.out."""
import sys

sys.path.insert(0, "vendor")
from semver import Version as V  # noqa: E402


def run(op, arg):
    try:
        if op == "parse":
            d = V.parse(arg).to_dict()
            return ("major=%s minor=%s patch=%s prerelease=%s build=%s"
                    % (d["major"], d["minor"], d["patch"],
                       d["prerelease"], d["build"]))
        if op == "valid":
            return "valid=" + str(V.is_valid(arg)).lower()
        if op == "cmp":
            a, b = arg.split("|")
            return "cmp=" + str(V.parse(a).compare(b))
        if op == "match":
            a, e = arg.split("|")
            return "match=" + str(V.parse(a).match(e)).lower()
        if op == "bump":
            which, v = arg.split("|")
            return "bumped=" + str(getattr(V.parse(v), "bump_" + which)())
        if op == "next":
            part, v = arg.split("|")
            return "next=" + str(V.parse(v).next_version(part))
        if op == "finalize":
            return "final=" + str(V.parse(arg).finalize_version())
    except (ValueError, TypeError) as e:
        return "error=" + str(e)
    raise SystemExit("unknown op: " + op)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        arg = f[1] if len(f) > 1 else ""
        out.append("== " + " | ".join(f))
        out.append("  " + run(f[0], arg))
sys.stdout.write("\n".join(out) + "\n")
