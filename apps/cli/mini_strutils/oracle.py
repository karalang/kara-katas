#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored boltons.strutils and writes
expected.out.

For each job it prints a header line

    == <op> <args...>

then the function's result on its own line. `pil` prints the Python list repr
(`[1, 3, 5]`), `irl` the tuple-of-tuples repr (`((1, 1), (3, 3))`); the others
print the returned string. mini_strutils.kara reproduces this stream exactly.
"""
import sys

sys.path.insert(0, "vendor")
from boltons import strutils as S  # noqa: E402


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    out.append("== " + " ".join([op] + f[1:]))
    if op == "c2u":
        out.append(S.camel2under(f[1]))
    elif op == "u2c":
        out.append(S.under2camel(f[1]))
    elif op == "ord":
        out.append(S.ordinalize(f[1]))
    elif op == "a10":
        out.append(S.a10n(f[1]))
    elif op == "slug":
        out.append(S.slugify(f[1]))
    elif op == "pil":
        out.append(repr(S.parse_int_list(f[1])))
    elif op == "fil":
        ints = [int(t) for t in f[1].split()] if f[1].strip() else []
        out.append(S.format_int_list(ints))
    elif op == "cil":
        rs, st = f[1], int(f[2])
        en = None if f[3] == "*" else int(f[3])
        out.append(S.complement_int_list(rs, st, en))
    elif op == "irl":
        out.append(repr(S.int_ranges_from_int_list(f[1])))
    elif op == "hrl":
        items = f[1].split("|") if f[1] else []
        out.append(S.human_readable_list(items))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
