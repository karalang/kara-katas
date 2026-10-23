#!/usr/bin/env python3
"""Writes data/jobs.tsv: one openlocationcode call per line, tab-separated.

    enc  <lat> <lng> [<codeLength>]    encode
    dec  <code>                        decode
    chk  <code>                        isValid / isShort / isFull
    sho  <code> <lat> <lng>            shorten
    rec  <code> <lat> <lng>            recoverNearest

No library import -- the inputs are literal here. Run: python3 -s -P -B mk.py"""
import os

JOBS = [
    # encode at the default length and every other length
    ("enc", "47.365590", "8.524997"),
    ("enc", "47.365590", "8.524997", "11"),
    ("enc", "47.365590", "8.524997", "12"),
    ("enc", "47.365590", "8.524997", "15"),
    ("enc", "47.365590", "8.524997", "16"),
    ("enc", "47.365590", "8.524997", "8"),
    ("enc", "47.365590", "8.524997", "6"),
    ("enc", "47.365590", "8.524997", "4"),
    ("enc", "47.365590", "8.524997", "2"),
    ("enc", "47.365590", "8.524997", "9"),
    ("enc", "47.365590", "8.524997", "1"),
    ("enc", "47.365590", "8.524997", "7"),
    ("enc", "20.375", "2.775"),
    ("enc", "20.3700625", "2.7821875", "11"),
    ("enc", "51.3701125", "-1.217765625", "11"),
    ("enc", "-41.2730625", "174.7859375", "11"),
    ("enc", "37.539669125", "-122.375069724", "15"),
    ("enc", "-37.8136", "144.9631"),
    ("enc", "35.6895", "139.6917", "11"),
    ("enc", "-33.9249", "18.4241", "13"),
    ("enc", "40.7128", "-74.006", "14"),
    ("enc", "1.286785", "103.854503", "10"),
    # the poles, the antimeridian and out-of-range input
    ("enc", "90", "1"),
    ("enc", "90", "1", "4"),
    ("enc", "90", "1", "11"),
    ("enc", "92", "1"),
    ("enc", "-90", "1"),
    ("enc", "-95", "-185"),
    ("enc", "0", "180"),
    ("enc", "0", "-180"),
    ("enc", "1", "540", "11"),
    ("enc", "1", "-540"),
    ("enc", "89.99999", "179.99999", "15"),
    ("enc", "0", "0"),
    # decode
    ("dec", "8FVC9G8F+6X"),
    ("dec", "8FVC9G8F+6XR"),
    ("dec", "8fvc9g8f+6x"),
    ("dec", "8FVC0000+"),
    ("dec", "8F000000+"),
    ("dec", "7FG49QCJ+2VXGJ"),
    ("dec", "7FG49QCJ+2VXGJRQ"),
    ("dec", "CFX30000+"),
    ("dec", "22222222+22"),
    ("dec", "CFX3X2X2+X2"),
    ("dec", "9C3W9QCJ+2VX"),
    ("dec", "4VCPPQGP+Q9"),
    ("dec", "9G8F+6X"),
    ("dec", "8FVC9G8+6X"),
    ("dec", "WF8Q0000+"),
    # validity
    ("chk", "8FWC2345+G6"),
    ("chk", "8FWC2345+G6G"),
    ("chk", "8fwc2345+"),
    ("chk", "8FWCX400+"),
    ("chk", "WC2345+G6g"),
    ("chk", "2345+G6"),
    ("chk", "45+G6"),
    ("chk", "+G6"),
    ("chk", "G+"),
    ("chk", "+"),
    ("chk", "8FWC2345+G"),
    ("chk", "8FWC2_45+G6"),
    ("chk", "8FWC2345+G6+"),
    ("chk", "8FWC2300+G6"),
    ("chk", "WC2300+G6g"),
    ("chk", "WC2345+G"),
    ("chk", "8FWC00+"),
    ("chk", "80WC0000+"),
    ("chk", "8FWC000+"),
    ("chk", "8FWC2345"),
    ("chk", "X2222222+"),
    ("chk", "2X222222+"),
    ("chk", "C2222222+"),
    ("chk", "2W222222+"),
    ("chk", ""),
    # shorten
    ("sho", "9C3W9QCJ+2VX", "51.3701125", "-1.217765625"),
    ("sho", "9C3W9QCJ+2VX", "51.3708675", "-1.217765625"),
    ("sho", "9C3W9QCJ+2VX", "51.3693575", "-1.217765625"),
    ("sho", "9C3W9QCJ+2VX", "51.3701125", "-1.218520625"),
    ("sho", "9C3W9QCJ+2VX", "51.3701125", "-1.217010625"),
    ("sho", "9C3W9QCJ+2VX", "51.3701125", "-1.17"),
    ("sho", "9C3W9QCJ+2VX", "51.0", "-1.2"),
    ("sho", "9C3W9QCJ+2VX", "60.0", "10.0"),
    ("sho", "8FJFW222+", "42.899", "9.012"),
    ("sho", "8FVC9G8F+6X", "47.4", "8.6"),
    ("sho", "8FVC0000+", "47.4", "8.6"),
    ("sho", "9G8F+6X", "47.4", "8.6"),
    # recoverNearest
    ("rec", "9G8F+6X", "47.4", "8.6"),
    ("rec", "8F+6X", "47.4", "8.6"),
    ("rec", "+2VX", "51.3708675", "-1.217765625"),
    ("rec", "CJ+2VX", "51.3701125", "-1.217765625"),
    ("rec", "9QCJ+2VX", "51.3701125", "-1.217765625"),
    ("rec", "XQP5+", "47.0", "8.0"),
    ("rec", "2222+22", "89.6", "0.0"),
    ("rec", "2222+22", "-89.6", "179.9"),
    ("rec", "QXXX+XX", "89.9", "179.9"),
    ("rec", "XXXX+XX", "-89.9", "-179.9"),
    ("rec", "8FVC9G8F+6X", "0", "0"),
    ("rec", "8fvc9g8f+6x", "0", "0"),
    ("rec", "9G8F+6Y", "47.4", "8.6"),
    ("rec", "9G8+6X", "47.4", "8.6"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for job in JOBS:
        fh.write("\t".join(job) + "\n")
print("wrote %d jobs" % len(JOBS))
