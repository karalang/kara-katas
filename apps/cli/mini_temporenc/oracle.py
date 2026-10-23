#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored temporenc library and writes
expected.out. Each line is

    TYPE year month day hour minute second subkind subval tz

(see mk.py for the field encoding). For each job the oracle packs the fields
into a temporenc byte string of the named type, then unpacks that byte string
back into a Moment, printing:

    pack <lowercase hex of the packed bytes>
    unpack y=<v> mo=<v> d=<v> h=<v> mi=<v> s=<v> ns=<v> tz=<v>

where each <v> is the Moment attribute, or - when that component is None
(temporenc stores partial values, so any component may be absent). The
sub-second value is reported as the canonical nanosecond count. mini_temporenc.kara
reproduces this byte-for-byte on every backend."""
import sys

sys.path.insert(0, "vendor")
import temporenc as T  # noqa: E402


def f(v):
    return "-" if v is None else str(v)


def row(line):
    toks = line.split(" ")
    typ = toks[0]
    y, mo, d, h, mi, s = (int(x) for x in toks[1:7])
    subkind = toks[7]
    subval = int(toks[8])
    tz = int(toks[9])

    kw = {"type": typ}
    if y >= 0:
        kw["year"] = y
    if mo >= 0:
        kw["month"] = mo
    if d >= 0:
        kw["day"] = d
    if h >= 0:
        kw["hour"] = h
    if mi >= 0:
        kw["minute"] = mi
    if s >= 0:
        kw["second"] = s
    if subkind == "ms":
        kw["millisecond"] = subval
    elif subkind == "us":
        kw["microsecond"] = subval
    elif subkind == "ns":
        kw["nanosecond"] = subval
    if tz != -9999:
        kw["tz_offset"] = tz

    packed = T.packb(**kw)
    m = T.unpackb(packed)
    hexs = "".join("%02x" % b for b in bytearray(packed))
    fields = "y=%s mo=%s d=%s h=%s mi=%s s=%s ns=%s tz=%s" % (
        f(m.year), f(m.month), f(m.day),
        f(m.hour), f(m.minute), f(m.second),
        f(m.nanosecond), f(m.tz_offset))
    return "pack " + hexs + "\nunpack " + fields


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(row(line))
    sys.stdout.write("\n".join(out) + "\n")


main()
