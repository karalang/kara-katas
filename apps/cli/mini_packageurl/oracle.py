#!/usr/bin/env python3
"""Runs data/jobs.tsv through packageurl-python and prints expected.out.

A `parse` job prints the six components of PackageURL.from_string (type,
namespace, name, version, qualifiers, subpath; `-` for an absent one,
qualifiers as sorted key=value pairs joined by &) and the canonical
to_string, or `err=<message>` with the library's exact ValueError text. A
`build` job constructs a PackageURL from its fields (`-` becomes None) and
prints `str=<to_string>` or `err=<message>`.
"""
import sys

sys.path.insert(0, "vendor")
from packageurl import PackageURL  # noqa: E402


def none(s):
    return None if s == "-" else s


def q_str(d):
    if not d:
        return "-"
    return "&".join(f"{k}={v}" for k, v in sorted(d.items()))


def run(f):
    k = f[0]
    if k == "parse":
        try:
            o = PackageURL.from_string(f[1])
        except ValueError as e:
            return ["err=" + str(e)]
        return [
            "type=" + (o.type or "-"),
            "namespace=" + (o.namespace or "-"),
            "name=" + (o.name or "-"),
            "version=" + (o.version or "-"),
            "qualifiers=" + q_str(o.qualifiers),
            "subpath=" + (o.subpath or "-"),
            "canonical=" + o.to_string(),
        ]
    if k == "build":
        try:
            o = PackageURL(
                type=none(f[1]),
                namespace=none(f[2]),
                name=none(f[3]),
                version=none(f[4]),
                qualifiers=none(f[5]),
                subpath=none(f[6]),
            )
        except ValueError as e:
            return ["err=" + str(e)]
        return ["str=" + o.to_string()]
    raise SystemExit("unknown job: " + k)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        for r in run(f):
            out.append("  " + r)
sys.stdout.write("\n".join(out) + "\n")
