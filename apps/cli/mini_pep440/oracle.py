#!/usr/bin/env python3
"""Runs data/jobs.tsv through packaging's PEP 440 Version and prints
expected.out. Each job prints "== " and its fields joined by " | ", then two
spaces and the result (a round-tripped string, an attribute line, the six
comparisons, a sorted list, or a canonical form).
"""
import sys

sys.path.insert(0, "vendor")
from packaging.version import Version, InvalidVersion
from packaging.utils import canonicalize_name, canonicalize_version


def props(v):
    return (
        f"epoch={v.epoch!r} release={v.release!r} pre={v.pre!r} "
        f"post={v.post!r} dev={v.dev!r} local={v.local!r} "
        f"public={v.public!r} base={v.base_version!r} "
        f"major={v.major!r} minor={v.minor!r} micro={v.micro!r} "
        f"is_pre={v.is_prerelease!r} is_post={v.is_postrelease!r} "
        f"is_dev={v.is_devrelease!r}"
    )


def run(f):
    k = f[0]
    if k == "parse":
        try:
            return str(Version(f[1] if len(f) > 1 else ""))
        except InvalidVersion as e:
            return str(e)
    if k == "props":
        return props(Version(f[1]))
    if k == "cmp":
        a, b = Version(f[1]), Version(f[2])
        return (
            f"lt={a < b} le={a <= b} eq={a == b} "
            f"ne={a != b} gt={a > b} ge={a >= b}"
        )
    if k == "sort":
        vs = [Version(x) for x in f[1].split(",")]
        return repr([str(v) for v in sorted(vs)])
    if k == "cname":
        return canonicalize_name(f[1])
    if k == "cver":
        return canonicalize_version(f[1], strip_trailing_zero=f[2] == "1")
    raise SystemExit("unknown job: " + k)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        out.append("  " + run(f))
sys.stdout.write("\n".join(out) + "\n")
