#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored netaddr and prints expected.out."""
import sys

sys.path.insert(0, "vendor")
from netaddr import (  # noqa: E402
    IPNetwork, IPAddress, cidr_merge, spanning_cidr, iprange_to_cidrs,
    cidr_exclude, glob_to_cidrs, cidr_to_glob, glob_to_iprange,
    iprange_to_globs, valid_glob,
)
from netaddr.core import AddrFormatError, AddrConversionError  # noqa: E402


def joincidrs(nets):
    return ",".join(str(n) for n in nets)


def run(op, arg):
    try:
        if op == "net":
            n = IPNetwork(arg)
            return "net=" + str(n) + " cidr=" + str(n.cidr)
        if op == "merge":
            return "cidrs=" + joincidrs(cidr_merge(arg.split(",")))
        if op == "span":
            return "cidr=" + str(spanning_cidr(arg.split(",")))
        if op == "range2cidr":
            a, b = arg.split(",")
            return "cidrs=" + joincidrs(iprange_to_cidrs(IPAddress(a), IPAddress(b)))
        if op == "exclude":
            t, e = arg.split("|")
            return "cidrs=" + joincidrs(cidr_exclude(t, e))
        if op == "glob2cidr":
            return "cidrs=" + joincidrs(glob_to_cidrs(arg))
        if op == "cidr2glob":
            return "glob=" + cidr_to_glob(arg)
        if op == "glob2range":
            return "range=" + str(glob_to_iprange(arg))
        if op == "range2glob":
            a, b = arg.split(",")
            return "globs=" + ",".join(iprange_to_globs(IPAddress(a), IPAddress(b)))
        if op == "validglob":
            return "valid=" + str(valid_glob(arg)).lower()
    except (AddrFormatError, AddrConversionError, ValueError, TypeError) as e:
        return "error=" + str(e)
    raise SystemExit("unknown op: " + op)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        out.append("  " + run(f[0], f[1]))
sys.stdout.write("\n".join(out) + "\n")
