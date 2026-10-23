#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated, "<op>\t<arg>...".
Inputs are literals here (the library is not imported). Floats are written as
Python reprs; "None" stands for an omitted keyword argument, "True"/"False"
for a bool, and an empty field for the empty string.
Run: python3 -s -P -B mk.py"""
import os

jobs = []


def job(*f):
    jobs.append("\t".join(str(x) for x in f))


N = "None"

# --- from_latlon(latitude, longitude, force_zone_number, force_zone_letter, force_northern) ---
places = [
    (50.77535, 6.08389),        # Aachen
    (40.71435, -74.00597),      # New York
    (-41.28646, 174.77624),     # Wellington
    (-33.92487, 18.42406),      # Cape Town
    (-32.89018, -68.84405),     # Mendoza
    (64.83778, -147.71639),     # Fairbanks
    (35.6812, 139.7671),        # Tokyo
    (-33.8568, 151.2153),       # Sydney
    (51.4778, -0.0015),         # Greenwich
    (60.39299, 5.32415),        # Bergen (Norway's zone 32 exception)
    (78.22317, 15.6267),        # Longyearbyen (Svalbard zone 33)
    (79.0, 5.0),                # Svalbard zone 31
    (80.0, 25.0),               # Svalbard zone 35
    (81.0, 40.0),               # Svalbard zone 37
    (64.1466, -21.9426),        # Reykjavik
    (-0.1807, -78.4678),        # Quito
    (0.0, 0.0),
    (-0.0, 3.0),
    (-77.8463, 166.6683),       # McMurdo
    (-80.0, -180.0), (84.0, 180.0), (84.0, -180.0), (-80.0, 179.99999999999997),
    (12.99210956845755, 13.499569405566604),
]
for la, lo in places:
    job("fl", repr(la), repr(lo), N, N, N)
for la, lo, zn, zl, fn in [
    (12.99210956845755, 13.499569405566604, 50, N, N),   # far from the zone's meridian
    (50.77535, 6.08389, 31, N, N), (50.77535, 6.08389, 32, "u", N),
    (-33.92487, 18.42406, 34, N, True), (-33.92487, 18.42406, N, N, False),
    (40.71435, -74.00597, 18, "S", N), (40.71435, -74.00597, N, "Z", N),
    (40.71435, -74.00597, 0, N, N), (40.71435, -74.00597, 61, N, N),
    (40.71435, -74.00597, 18, "I", N), (40.71435, -74.00597, 18, "O", N),
    (40.71435, -74.00597, 18, "T", True), (40.71435, -74.00597, 18, "", True),
    (-41.28646, 174.77624, 1, N, N),
]:
    job("fl", repr(la), repr(lo), zn, zl, fn)
for la, lo in [(84.1, 0.0), (-80.5, 0.0), (0.0, 180.5), (0.0, -181.0)]:
    job("fl", repr(la), repr(lo), N, N, N)

# --- to_latlon(easting, northing, zone_number, zone_letter, northern, strict) ---
for e, n, zn, zl, north, strict in [
    (294409.0, 5628898.0, 32, "U", N, True), (583960.0, 4507523.0, 18, "T", N, True),
    (313784.0, 5427057.0, 60, "G", N, True), (261878.0, 6243186.0, 34, "H", N, True),
    (514586.0, 6360877.0, 19, "h", N, True), (466013.0, 7190568.0, 6, "W", N, True),
    (294409.0, 5628898.0, 32, N, True, True), (313784.0, 5427057.0, 60, N, False, True),
    (500000.0, 0.0, 31, "N", N, True), (500000.0, 10000000.0, 31, "M", N, True),
    (100000.0, 9000000.0, 1, "X", N, True), (999999.0, 1234.5, 60, "C", N, True),
    (166021.44317933032, 0.0, 31, N, True, True),
    (99999.0, 5000000.0, 32, "U", N, True), (1000000.0, 5000000.0, 32, "U", N, True),
    (500000.0, -1.0, 32, "U", N, True), (500000.0, 10000001.0, 32, "U", N, True),
    (50000.0, 5000000.0, 32, "U", N, False), (1200000.0, -5.0, 32, N, True, False),
    (500000.0, 5000000.0, 32, N, N, True), (500000.0, 5000000.0, 32, "U", True, True),
    (500000.0, 5000000.0, 0, "U", N, True), (500000.0, 5000000.0, 61, "U", N, True),
    (500000.0, 5000000.0, 32, "I", N, True), (500000.0, 5000000.0, 32, "B", N, True),
    (500000.0, 5000000.0, 32, "Y", N, True), (500000.0, 5000000.0, 32, "", N, True),
    (500000.0, 5000000.0, 32, "", False, True),
]:
    job("tl", repr(e), repr(n), zn, zl, north, strict)

# --- zone helpers ---
for la in [-80.0, -79.9, -72.0, -0.1, 0.0, 7.99, 8.0, 71.9, 72.0, 79.99, 80.0, 84.0, 84.5, -80.5]:
    job("zl", repr(la))
for la, lo in [(0.0, -180.0), (0.0, 180.0), (0.0, 179.9), (0.0, 540.0), (0.0, -545.5), (56.0, 3.0),
               (63.99, 11.99), (64.0, 5.0), (55.99, 5.0), (72.0, 0.0), (84.0, 41.99), (71.99, 8.0),
               (85.0, 20.0), (0.0, -0.0)]:
    job("zn", repr(la), repr(lo))
for zn in [1, 30, 31, 60, 0, 61, -3]:
    job("cl", zn)
for zl in ["C", "M", "N", "W", "X", "x", "h", "I", "O", "A", "Y", "CX"]:
    job("cz", zl)
for zn, zl in [(32, "U"), (32, ""), (0, "U"), (32, "Q"), (32, "o")]:
    job("cv", zn, zl)

# --- the utm-converter command ---
for la, lo in [(50.77535, 6.08389), (-33.92487, 18.42406), (60.39299, 5.32415)]:
    job("cli", "latlon", repr(la), repr(lo))
for e, n, zn, zl in [(294409, 5628898, 32, "U"), (313784, 5427057, 60, "G"), (583960, 4507523, 18, "")]:
    job("cli", "utm", e, n, zn, zl)

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")
