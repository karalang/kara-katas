#!/usr/bin/env python3
"""Writes data/jobs.tsv: one maidenhead call per line, tab-separated.

    maiden <lat> <lon> <precision>        to_maiden
    loc    <locator> <center 0|1>         to_location
    rect   <locator>                      to_location_rect
    geo    <locator> <center 0|1> <square 0|1>   to_geoJSONObject, json.dumps
    url    <locator> <center 0|1>         google_maps
    cli    <locator | lat,lon> <precision> <flags>   python -m maidenhead

cli flags are letters: u (--url), c (--center), g (--geojson), n (--nosquare).
No library import -- the inputs are literal here. Run: python3 -s -P -B mk.py"""
import os

JOBS = [
    ("maiden", "41.714775", "-72.727260", "3"),
    ("maiden", "41.714775", "-72.727260", "4"),
    ("maiden", "41.714775", "-72.727260", "5"),
    ("maiden", "41.714775", "-72.727260", "6"),
    ("maiden", "41.714775", "-72.727260", "2"),
    ("maiden", "41.714775", "-72.727260", "1"),
    ("maiden", "40.0", "-105.0", "3"),
    ("maiden", "51.4778", "-0.0015", "4"),
    ("maiden", "35.6895", "139.6917", "3"),
    ("maiden", "-33.8688", "151.2093", "4"),
    ("maiden", "-77.8463", "166.6683", "3"),
    ("maiden", "64.1466", "-21.9426", "5"),
    ("maiden", "0.0", "0.0", "3"),
    ("maiden", "-90.0", "-180.0", "3"),
    ("maiden", "89.999", "179.999", "4"),
    ("maiden", "90.0", "180.0", "3"),
    ("maiden", "12.5", "540.0", "3"),
    ("maiden", "12.5", "-540.0", "3"),
    ("maiden", "-12.5", "-359.99", "4"),
    ("loc", "FN31pr", "0"),
    ("loc", "FN31pr", "1"),
    ("loc", "fn31PR", "0"),
    ("loc", "  FN31pr ", "1"),
    ("loc", "FN31", "0"),
    ("loc", "FN", "1"),
    ("loc", "FN31pr33", "0"),
    ("loc", "FN31pr33", "1"),
    ("loc", "FN31pr33ab", "1"),
    ("loc", "JJ00aa", "0"),
    ("loc", "AA00aa00", "0"),
    ("loc", "RR99xx99xx", "1"),
    ("loc", "FN31ZZ", "0"),
    ("loc", "FN3", "0"),
    ("loc", "F", "0"),
    ("loc", "", "0"),
    ("loc", "SN31", "0"),
    ("loc", "FS31", "0"),
    ("loc", "FNA1", "0"),
    ("loc", "F31N", "0"),
    ("rect", "FN31pr"),
    ("rect", "IO91wm"),
    ("rect", "QF56od"),
    ("rect", "JJ00"),
    ("rect", "DM79lr44"),
    ("geo", "FN31pr", "1", "1"),
    ("geo", "FN31pr", "0", "1"),
    ("geo", "FN31pr", "1", "0"),
    ("geo", "FN31pr", "0", "0"),
    ("geo", "io91WM", "1", "1"),
    ("url", "FN31pr", "0"),
    ("url", "FN31pr", "1"),
    ("url", "PM95vq", "1"),
    ("cli", "FN31pr", "6", ""),
    ("cli", "FN31pr", "6", "c"),
    ("cli", "FN31pr", "6", "u"),
    ("cli", "FN31pr", "6", "cu"),
    ("cli", "FN31pr", "6", "g"),
    ("cli", "FN31pr", "6", "gc"),
    ("cli", "FN31pr", "6", "gcn"),
    ("cli", "FN31pr", "6", "gu"),
    ("cli", "41.714775,-72.727260", "3", ""),
    ("cli", "41.714775,-72.727260", "4", "u"),
    ("cli", "41.714775,-72.727260", "4", "cu"),
    ("cli", "-33.8688,151.2093", "6", ""),
    ("cli", "QF56od", "3", "c"),
    ("cli", "AA00aa", "3", ""),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for job in JOBS:
        fh.write("\t".join(job) + "\n")
print("wrote %d jobs" % len(JOBS))
