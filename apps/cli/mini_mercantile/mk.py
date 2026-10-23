#!/usr/bin/env python3
"""Writes data/jobs.tsv: one mercantile call per line, the operation name then
its arguments, tab-separated. A target zoom of "-" means "not given" (the
library's default), and a zoom list is comma-separated. No library import --
the inputs are literal here. Run: python3 -s -P -B mk.py"""
import os

JOBS = [
    # tile(lng, lat, zoom)
    ("tile", "-105.0", "39.75", "10"),
    ("tile", "0.0", "51.5", "12"),
    ("tile", "139.6917", "35.6895", "14"),
    ("tile", "-74.006", "40.7128", "16"),
    ("tile", "151.2093", "-33.8688", "8"),
    ("tile", "2.3522", "48.8566", "1"),
    ("tile", "-122.4194", "37.7749", "18"),
    ("tile", "18.4241", "-33.9249", "5"),
    ("tile", "0.0", "0.0", "0"),
    ("tile", "-179.9", "85.0", "6"),
    ("tile", "179.9", "-85.0", "6"),
    # quadkey(x, y, z)
    ("quadkey", "486", "332", "10"),
    ("quadkey", "0", "0", "1"),
    ("quadkey", "1", "1", "1"),
    ("quadkey", "8191", "8191", "14"),
    ("quadkey", "0", "0", "0"),
    ("quadkey", "35210", "21493", "16"),
    # quadkey_to_tile(qk)
    ("qk2tile", "0313102310"),
    ("qk2tile", ""),
    ("qk2tile", "0"),
    ("qk2tile", "3"),
    ("qk2tile", "123"),
    ("qk2tile", "0313102310300"),
    ("qk2tile", "0312a"),
    # parent(x, y, z[, zoom])
    ("parent", "486", "332", "10", "-"),
    ("parent", "0", "0", "2", "-"),
    ("parent", "0", "0", "2", "0"),
    ("parent", "486", "332", "10", "8"),
    ("parent", "759", "335", "10", "5"),
    ("parent", "1", "1", "1", "-"),
    # children(x, y, z[, zoom])
    ("children", "0", "0", "0", "-"),
    ("children", "0", "0", "0", "2"),
    ("children", "486", "332", "10", "-"),
    ("children", "243", "166", "9", "11"),
    # neighbors(x, y, z)
    ("neighbors", "486", "332", "10"),
    ("neighbors", "0", "0", "1"),
    ("neighbors", "0", "0", "10"),
    ("neighbors", "1023", "1023", "10"),
    ("neighbors", "0", "0", "0"),
    # tiles(west, south, east, north, zooms)
    ("tiles", "-105.0", "39.0", "-104.0", "40.0", "10"),
    ("tiles", "-180.0", "-85.0", "180.0", "85.0", "1"),
    ("tiles", "-105.0", "39.0", "-104.0", "40.0", "9,10"),
    ("tiles", "179.0", "-1.0", "-179.0", "1.0", "4"),
    ("tiles", "2.0", "48.0", "3.0", "49.0", "12"),
    # bounding_tile(west, south, east, north)
    ("bounding", "-105.0", "39.0", "-104.0", "40.0"),
    ("bounding", "-105.0", "39.75", "-105.0", "39.75"),
    ("bounding", "2.0", "48.0", "3.0", "49.0"),
    ("bounding", "-180.0", "-85.0", "180.0", "85.0"),
    # minmax(zoom)
    ("minmax", "0"),
    ("minmax", "1"),
    ("minmax", "10"),
    ("minmax", "14"),
    ("minmax", "20"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for job in JOBS:
        fh.write("\t".join(job) + "\n")
print("wrote %d jobs" % len(JOBS))
