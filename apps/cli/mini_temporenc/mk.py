#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one temporenc pack/unpack job per line, as the
space-separated fields

    TYPE year month day hour minute second subkind subval tz

where TYPE is one of D T DT DTZ DTS DTSZ; a missing year/month/day/hour/
minute/second is -1; subkind is n (none), ms, us or ns with its value in
subval (0 when n); and tz is -9999 for "no time zone" or an offset in minutes
from UTC (a multiple of 15, with -960 <= tz <= 930 so the encoded 7-bit field
stays in range).

No temporenc import here (only literal inputs); oracle.py replays each line
through the vendored library to produce expected.out. The jobs cover every
temporenc type and every sub-second precision, partial/empty date and time
components, leap seconds, and the time-zone range boundaries."""

JOBS = [
    # D: date only (full, partial, all-empty)
    "D 2026 10 23 -1 -1 -1 n 0 -9999",
    "D 1 1 1 -1 -1 -1 n 0 -9999",
    "D 2000 2 29 -1 -1 -1 n 0 -9999",
    "D 4094 12 31 -1 -1 -1 n 0 -9999",
    "D 2026 -1 -1 -1 -1 -1 n 0 -9999",       # year only
    "D 2026 10 -1 -1 -1 -1 n 0 -9999",       # year + month
    "D -1 -1 -1 -1 -1 -1 n 0 -9999",         # all empty
    # T: time only (full, leap second, partial)
    "T -1 -1 -1 0 0 0 n 0 -9999",
    "T -1 -1 -1 23 59 59 n 0 -9999",
    "T -1 -1 -1 13 0 60 n 0 -9999",          # leap second
    "T -1 -1 -1 -1 30 -1 n 0 -9999",         # minute only
    # DT: date + time
    "DT 2026 10 23 13 5 7 n 0 -9999",
    "DT 1970 1 1 0 0 0 n 0 -9999",
    "DT 2014 10 30 23 59 60 n 0 -9999",
    # DTZ: date + time + time zone (offset range boundaries)
    "DTZ 2026 10 23 13 5 7 n 0 0",
    "DTZ 2026 10 23 13 5 7 n 0 60",
    "DTZ 2026 10 23 13 5 7 n 0 -60",
    "DTZ 2026 10 23 13 5 7 n 0 345",
    "DTZ 2026 10 23 13 5 7 n 0 930",
    "DTZ 2026 10 23 13 5 7 n 0 -960",
    # DTS: date + time + sub-second, all four precisions
    "DTS 2026 10 23 13 5 7 n 0 -9999",        # precision 11 (none)
    "DTS 2026 10 23 13 5 7 ms 250 -9999",     # precision 00
    "DTS 2026 10 23 13 5 7 ms 999 -9999",
    "DTS 2026 10 23 13 5 7 us 123456 -9999",  # precision 01
    "DTS 2026 10 23 13 5 7 us 999999 -9999",
    "DTS 2026 10 23 13 5 7 ns 123456789 -9999",  # precision 10
    "DTS 2026 10 23 13 5 7 ns 999999999 -9999",
    # DTSZ: date + time + sub-second + time zone, all four precisions
    "DTSZ 2026 10 23 13 5 7 n 0 60",
    "DTSZ 2026 10 23 13 5 7 ms 250 -300",
    "DTSZ 2026 10 23 13 5 7 us 123456 345",
    "DTSZ 2026 10 23 13 5 7 ns 123456789 -960",
    "DTSZ 1970 1 1 0 0 0 ns 0 0",
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for job in JOBS:
            fh.write(job + "\n")


main()
