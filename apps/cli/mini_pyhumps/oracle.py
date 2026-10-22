#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored pyhumps, prints expected.out.

Output per job:
  == <op> | <identifier>
    <result>

For the conversion ops the result is the converted string; for the is_* ops
it is "true" / "false". mini_pyhumps.kara reimplements each on bytes and must
match this byte-for-byte on every backend.
"""
import sys

sys.path.insert(0, "vendor")
import humps  # noqa: E402

OPS = {
    "camelize": humps.camelize,
    "decamelize": humps.decamelize,
    "pascalize": humps.pascalize,
    "kebabize": humps.kebabize,
    "dekebabize": humps.dekebabize,
    "is_camelcase": humps.is_camelcase,
    "is_snakecase": humps.is_snakecase,
    "is_pascalcase": humps.is_pascalcase,
    "is_kebabcase": humps.is_kebabcase,
}


def run(op, arg):
    fn = OPS[op]
    r = fn(arg)
    if isinstance(r, bool):
        return "true" if r else "false"
    return r


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        f = line.split("\t")
        op = f[0]
        arg = f[1] if len(f) > 1 else ""
        out.append("== " + op + " | " + arg)
        out.append("  " + run(op, arg))

sys.stdout.write("\n".join(out) + "\n")
