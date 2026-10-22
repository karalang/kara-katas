#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored macaddress and prints expected.out."""
import sys

sys.path.insert(0, "vendor")
from macaddress import OUI, CDI32, CDI40, EUI48, EUI60, EUI64, parse  # noqa: E402

CLASSES = [OUI, CDI32, CDI40, EUI48, EUI60, EUI64]
BY_NAME = {c.__name__: c for c in CLASSES}


def build(spec):
    name, _, s = spec.partition("=")
    return BY_NAME[name](s)


def run(op, arg):
    try:
        if op == "parse":
            return "addr=" + repr(parse(arg, *CLASSES))
        if op == "int":
            name, _, dec = arg.partition(",")
            return "addr=" + repr(BY_NAME[name](int(dec)))
        if op == "oui":
            name, _, s = arg.partition(",")
            return "oui=" + repr(BY_NAME[name](s).oui)
        if op == "cmp":
            a, b = (build(x) for x in arg.split("|"))
            return "lt=" + str(a < b).lower() + " eq=" + str(a == b).lower()
        if op == "sort":
            items = sorted(build(x) for x in arg.split(","))
            return "sorted=" + ",".join(repr(i) for i in items)
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
