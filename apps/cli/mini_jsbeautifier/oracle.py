"""Runs the vendored jsbeautifier over data/jobs.txt and prints what each
beautify() call returns; this wrote expected.out.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

# As in mk.py: the unpackers are not vendored and pass the source through.
stub = types.ModuleType("jsbeautifier.unpackers")


class UnpackingError(Exception):
    pass


stub.UnpackingError = UnpackingError
stub.run = lambda source, evalcode=False: source
sys.modules["jsbeautifier.unpackers"] = stub

import jsbeautifier  # noqa: E402
from jsbeautifier.javascript.options import BeautifierOptions  # noqa: E402


def unesc(s):
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        nx = s[i + 1]
        if nx == "n":
            out.append("\n")
            i += 2
        elif nx == "r":
            out.append("\r")
            i += 2
        elif nx == "t":
            out.append("\t")
            i += 2
        elif nx == "\\":
            out.append("\\")
            i += 2
        else:
            end = s.index("}", i)
            out.append(chr(int(s[i + 3:end], 16)))
            i = end + 1
    return "".join(out)


# Code points written as \u{hex}: the ASCII controls and the Unicode
# separators, format characters and non-characters the jobs hold (the same
# rule as shown_escaped() in the port).
def shown_escaped(ch):
    n = ord(ch)
    return (n < 0x20 or n == 0x7F or 0x80 <= n < 0xA0 or n == 0xA0 or n == 0xAD or n == 0x1680 or n == 0x180E
            or 0x2000 <= n <= 0x200F or 0x2028 <= n <= 0x202F or 0x205F <= n <= 0x206F or n == 0x3000
            or n == 0xFEFF or 0xFFF0 <= n <= 0xFFFF or 0xD800 <= n <= 0xF8FF or n >= 0xE0000)


def esc(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif shown_escaped(ch):
            out.append("\\u{%x}" % o)
        else:
            out.append(ch)
    return "".join(out)


def parse_value(kind, text):
    if kind == "b":
        return text == "1"
    if kind == "i":
        return int(text)
    if kind == "s":
        return unesc(text)
    return unesc(text).split(",")


# An options object the way the test suite hands one over: an instance of
# the options class carrying exactly the recorded attributes.
def make_options(lines):
    opts = BeautifierOptions()
    opts.__dict__.clear()
    child = {}
    for line in lines:
        _, key, kind, text = line.split(" ", 3)
        v = parse_value(kind, text)
        if key.startswith("js."):
            child[key[3:]] = v
        else:
            setattr(opts, key, v)
    if child:
        opts.js = child
    return opts


sets = {}
jobs = []
cur = None
with open(os.path.join(HERE, "data", "jobs.txt"), encoding="utf-8", newline="\n") as f:
    for line in f.read().split("\n"):
        if line.startswith("set "):
            cur = []
            sets[int(line[4:])] = cur
        elif line.startswith("o "):
            cur.append(line)
        elif line.startswith("job "):
            _, n, s = line.split(" ")
            jobs.append([int(n), int(s), None])
        elif line.startswith("in "):
            jobs[-1][2] = unesc(line[3:])

for n, s, src in jobs:
    out = jsbeautifier.beautify(src, make_options(sets[s]))
    print("== %d (set %d, %d chars in, %d out)" % (n, s, len(src), len(out)))
    for part in out.split("\n"):
        print("| " + esc(part))
print("%d jobs" % len(jobs))
