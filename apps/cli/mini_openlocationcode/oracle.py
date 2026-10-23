#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored openlocationcode library and
writes expected.out, one line per job:

    encode(<lat>, <lng>[, <len>]) => <code>
    decode(<code>) => [latLo, lngLo, latHi, lngHi, latCenter, lngCenter, len]
    check(<code>) => isValid isShort isFull
    shorten(<code>, <lat>, <lng>) => <code>
    recoverNearest(<code>, <lat>, <lng>) => <code>

A decode prints the library's own CodeArea repr. A raised ValueError prints as
"ValueError: <message>". Run: python3 -I -B oracle.py > expected.out"""
import sys

sys.path.insert(0, "vendor")
from openlocationcode import openlocationcode as olc  # noqa: E402


def run(f):
    op = f[0]
    if op == "enc":
        if len(f) > 3:
            return olc.encode(float(f[1]), float(f[2]), int(f[3]))
        return olc.encode(float(f[1]), float(f[2]))
    if op == "dec":
        return repr(olc.decode(f[1]))
    if op == "chk":
        return "%s %s %s" % (olc.isValid(f[1]), olc.isShort(f[1]), olc.isFull(f[1]))
    if op == "sho":
        return olc.shorten(f[1], float(f[2]), float(f[3]))
    if op == "rec":
        return olc.recoverNearest(f[1], float(f[2]), float(f[3]))
    return "unknown op"


NAMES = {"enc": "encode", "dec": "decode", "chk": "check", "sho": "shorten",
         "rec": "recoverNearest"}
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if line == "":
        continue
    f = line.split("\t")
    try:
        res = run(f)
    except ValueError as e:
        res = "ValueError: %s" % e
    sys.stdout.write("%s(%s) => %s\n" % (NAMES[f[0]], ", ".join(f[1:]), res))
