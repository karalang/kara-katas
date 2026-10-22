#!/usr/bin/env python3
r"""Appends jobs_text() (data/jobs.tsv) to mini_pathvalidate.kara.

Unlike the other apps, the jobs carry real ESC (0x1b) and BEL (0x07) bytes, so
the literal escapes every control byte as \xNN. Kara decodes \x1b back to byte
27 (verified), so jobs_text() reconstructs the exact bytes the oracle read.
"""
import sys


def lit(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif o < 32 or o == 127:
            out.append("\\x%02x" % o)
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


print("")
print("fn jobs_text() -> String {")
print("    let mut s = String.new();")
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    print("    s.push_str(%s);" % lit(line + "\n"))
print("    s")
print("}")
