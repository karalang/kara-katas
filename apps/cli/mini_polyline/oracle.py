#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored polyline library and writes
expected.out. Each input line is a list of integer coordinates scaled by 1e5,
as space-separated `lat,lng` pairs. The job reconstructs float coordinates
(int / 1e5), encodes them with Google's Encoded Polyline Algorithm, decodes the
result back, and prints:

    enc <the polyline string>
    dec <lat,lng ... of the decoded coordinates, re-scaled to integers>

mini_polyline.kara reproduces this byte-for-byte on every backend. Decoded
coordinates are re-scaled to integers with the library's own _py2_round so the
output is integer and exact; it equals the input (a clean round-trip)."""
import sys

sys.path.insert(0, "vendor")
from polyline import polyline as poly  # noqa: E402

FACTOR = 100000


def row(line):
    pairs = []
    for tok in line.split(" "):
        a, b = tok.split(",")
        pairs.append((int(a), int(b)))
    fcoords = [(a / FACTOR, b / FACTOR) for (a, b) in pairs]
    enc = poly.encode(fcoords, 5)
    dec = poly.decode(enc, 5)
    dec_i = [(poly._py2_round(a * FACTOR), poly._py2_round(b * FACTOR)) for (a, b) in dec]
    decs = " ".join("%d,%d" % (a, b) for (a, b) in dec_i)
    return "enc " + enc + "\ndec " + decs


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(row(line))
    sys.stdout.write("\n".join(out) + "\n")


main()
