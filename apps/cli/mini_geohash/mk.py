#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated, "<op>\t<arg>...".
Inputs are literals here (the library is not imported). Floats are written as
Python reprs, so the Kara side's f64.parse reads back the same double.
Run: python3 -s -P -B mk.py"""
import os

jobs = []


def job(*f):
    jobs.append("\t".join(str(x) for x in f))


# --- geohash.encode(latitude, longitude, precision) ---
for la, lo, p in [
    (42.6, -5.6, 5), (57.64911, 10.40744, 11), (35.6812, 139.7671, 12),
    (0.0, 0.0, 12), (-0.0, -0.0, 7), (-90.0, -180.0, 10), (89.99999999999999, 179.99999999999997, 20),
    (51.5007, -0.1246, 9), (-33.8568, 151.2153, 8), (40.6892, -74.0445, 6), (-54.8, -68.3, 10),
    (35.6812, 139.7671, 0), (35.6812, 139.7671, 1), (35.6812, 139.7671, 24),
    (12.5, 180.0, 6), (12.5, 540.0, 6), (12.5, -900.5, 6), (-12.5, -180.0, 6),
    (1e-300, 1e-300, 10), (-1e-300, -1e-300, 10), (1e-17, -1e-17, 16),
    (90.0, 0.0, 12), (90.0, 139.7671, 6), (90.5, 0.0, 5), (-90.1, 10.0, 5), (-90.0, 359.9, 8),
]:
    job("enc", repr(la), repr(lo), p)

# --- decode / decode_exactly / bbox / neighbors / expand ---
codes = ["ezs42", "u4pruydqqvj", "xn76urx613z2", "r3gx2ux9ggh1", "0", "z", "", "zzzzzzzzzzzz",
         "000000", "gcpuvpk", "s00000000000000000000", "bcdz", "pbpbpbpbpbpbpbpbpbpbpbpb"]
for c in codes:
    for op in ("dec", "decx", "bbox", "nb", "exp"):
        job(op, c)
for c in ["ezs4a", "Ezs42", "il"]:
    job("dec", c)
    job("bbox", c)
    job("exp", c)

# --- uint64 forms ---
for la, lo in [(-90.0, -180.0), (0.0, 0.0), (45.0, 135.0), (35.6812, 139.7671), (-33.8568, 151.2153),
               (89.99999999999999, 179.99999999999997), (90.0, 0.0), (91.0, 0.0), (-91.0, 0.0), (10.0, 900.25)]:
    job("u64", repr(la), repr(lo))
for u in [0, 0x0800000000000000, 0x7800000000000000, 0xC000000000000000, 0xF800000000000000,
          0xFFFFFFFFFFFFFFFF, 0xE3C1D5D3A6F2B7A1, 0x123456789ABCDEF0]:
    job("du64", u)
for u, p in [(0xC000000000000000, 1), (0xC000000000000000, 2), (0xC000000000000000, 3),
             (0xC000000000000000, 4), (0xE3C1D5D3A6F2B7A1, 5), (0xE3C1D5D3A6F2B7A1, 10),
             (0xE3C1D5D3A6F2B7A1, 25), (0xE3C1D5D3A6F2B7A1, 26), (0x123456789ABCDEF0, 50),
             (0x123456789ABCDEF0, 51), (0, 20), (0, 21), (0xFFFFFFFFFFFFFFFF, 20),
             (0xFFFFFFFFFFFFFFFF, 21), (0x5555555555555555, 63), (0xAAAAAAAAAAAAAAAA, 64)]:
    job("eu64", u, p)

# --- jpgrid (JIS X 0410 mesh codes) ---
for la, lo in [(35.6812, 139.7671), (34.7025, 135.4959), (43.0686, 141.3508), (26.2124, 127.6809)]:
    for b in (1, 8, 80, 160, 320, 640, 16, 40):
        job("jpenc", repr(la), repr(lo), b)
for c in ["5339", "533946", "53394611", "533946113", "5339461132", "53394611323", "5339461",
          "533946005", "6441428811", "3927253", "523503485"]:
    for op in ("jpdec", "jpsw", "jpswd", "jpbbox", "jpnb", "jpexp"):
        job(op, c)

# --- jpiarea (DoCoMo Open iArea codes) ---
for la, lo in [(35.6812, 139.7671), (34.7025, 135.4959), (43.0686, 141.3508), (26.2124, 127.6809),
               (6.5, 140.0), (35.0, 99.5), (7.0, 100.0)]:
    job("iaenc", repr(la), repr(lo))
for c in ["5339", "533946", "533946003", "53394600302", "52350313312", "6441"]:
    for op in ("iadec", "iasw", "iaswd", "iabbox", "ianb", "iaexp"):
        job(op, c)

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")
