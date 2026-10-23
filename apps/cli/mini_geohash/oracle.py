#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored python-geohash modules (geohash,
jpgrid, jpiarea; the optional Rust extension is absent, so geohash runs its
pure-Python path) and writes expected.out. Each job prints one line,
"<op>(<args>) => <result>", where <result> is repr() of the return value (an
int prints as str()), "<ExceptionType>: <message>" when the call raises, and
gets " [UserWarning]" appended when the call emitted a warning (geohash warns
when latitude 90.0 is moved to the adjacent cell).
Run: python3 -I -B oracle.py > expected.out"""
import sys
import warnings

sys.path.insert(0, "vendor")
import geohash  # noqa: E402
import jpgrid  # noqa: E402
import jpiarea  # noqa: E402

assert geohash._geohash is None, "the Rust extension must not be loaded"


def call(f):
    op = f[0]
    if op == "enc":
        return geohash.encode(float(f[1]), float(f[2]), int(f[3]))
    if op == "dec":
        return geohash.decode(f[1])
    if op == "decx":
        return geohash.decode_exactly(f[1])
    if op == "bbox":
        return geohash.bbox(f[1])
    if op == "nb":
        return geohash.neighbors(f[1])
    if op == "exp":
        return geohash.expand(f[1])
    if op == "u64":
        return geohash.encode_uint64(float(f[1]), float(f[2]))
    if op == "du64":
        return geohash.decode_uint64(int(f[1]))
    if op == "eu64":
        return geohash.expand_uint64(int(f[1]), int(f[2]))
    if op == "jpenc":
        return jpgrid.encode(float(f[1]), float(f[2]), int(f[3]))
    if op == "jpdec":
        return jpgrid.decode(f[1])
    if op == "jpsw":
        return jpgrid.decode_sw(f[1])
    if op == "jpswd":
        return jpgrid.decode_sw(f[1], True)
    if op == "jpbbox":
        return jpgrid.bbox(f[1])
    if op == "jpnb":
        return jpgrid.neighbors(f[1])
    if op == "jpexp":
        return jpgrid.expand(f[1])
    if op == "iaenc":
        return jpiarea.encode(float(f[1]), float(f[2]))
    if op == "iadec":
        return jpiarea.decode(f[1])
    if op == "iasw":
        return jpiarea.decode_sw(f[1])
    if op == "iaswd":
        return jpiarea.decode_sw(f[1], True)
    if op == "iabbox":
        return jpiarea.bbox(f[1])
    if op == "ianb":
        return jpiarea.neighbors(f[1])
    if op == "iaexp":
        return jpiarea.expand(f[1])
    raise SystemExit("unknown op " + op)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if line == "":
        continue
    f = line.split("\t")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            r = call(f)
            res = str(r) if isinstance(r, int) else repr(r)
        except Exception as e:
            res = "%s: %s" % (type(e).__name__, e)
    if caught:
        res += " [%s]" % caught[0].category.__name__
    out.append("%s(%s) => %s" % (f[0], ", ".join(f[1:]), res))
print("\n".join(out))
