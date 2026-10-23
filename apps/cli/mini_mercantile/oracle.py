#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored mercantile library and writes
expected.out. One line per job:

    op(arg, arg, ...) => result

where a tile prints as x/y/z, a tile list as "<count>: x/y/z x/y/z ...", a
quadkey in brackets, a missing parent as None, a bad quadkey as
"ERR QuadKeyError", and minmax as "lo hi". Every result is an integer tile, a
quadkey string or an integer pair, so the oracle never depends on float repr.
Run: python3 -I oracle.py > expected.out"""
import sys

sys.path.insert(0, "vendor")
import mercantile as M  # noqa: E402


def t(tile):
    return "%d/%d/%d" % (tile.x, tile.y, tile.z)


def tl(tiles):
    tiles = list(tiles)
    return "%d: %s" % (len(tiles), " ".join(t(x) for x in tiles))


def run(f):
    op = f[0]
    a = f[1:]
    if op == "tile":
        return t(M.tile(float(a[0]), float(a[1]), int(a[2])))
    if op == "quadkey":
        return "[" + M.quadkey(int(a[0]), int(a[1]), int(a[2])) + "]"
    if op == "qk2tile":
        try:
            return t(M.quadkey_to_tile(a[0]))
        except M.QuadKeyError:
            return "ERR QuadKeyError"
    if op == "parent":
        x, y, z = int(a[0]), int(a[1]), int(a[2])
        p = M.parent(x, y, z) if a[3] == "-" else M.parent(x, y, z, zoom=int(a[3]))
        return "None" if p is None else t(p)
    if op == "children":
        x, y, z = int(a[0]), int(a[1]), int(a[2])
        c = M.children(x, y, z) if a[3] == "-" else M.children(x, y, z, zoom=int(a[3]))
        return tl(c)
    if op == "neighbors":
        return tl(M.neighbors(int(a[0]), int(a[1]), int(a[2])))
    if op == "tiles":
        zooms = [int(z) for z in a[4].split(",")]
        return tl(M.tiles(float(a[0]), float(a[1]), float(a[2]), float(a[3]), zooms))
    if op == "bounding":
        return t(M.bounding_tile(float(a[0]), float(a[1]), float(a[2]), float(a[3])))
    if op == "minmax":
        lo, hi = M.minmax(int(a[0]))
        return "%d %d" % (lo, hi)
    return "ERR unknown op"


for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if line == "":
        continue
    f = line.split("\t")
    sys.stdout.write("%s(%s) => %s\n" % (f[0], ", ".join(f[1:]), run(f)))
