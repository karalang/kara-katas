#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_rfc3339: one timestamp per line.

The strings cover the whole RFC 3339 date-time shape the validator accepts —
UTC `Z`, numeric offsets, optional fractional seconds — plus the ways it
rejects: out-of-range fields, a day past the month's length (with the leap-year
cases), the uppercase-only `T`/`Z`, and malformed offsets. Each line is one
`validate` target; the op is implicit.
"""
import os

JOBS = [
    "2020-01-01T00:00:00Z",
    "2021-12-31T23:59:59+05:30",
    "1996-12-19T16:39:57-08:00",
    "1990-12-31T23:59:59.999Z",
    "2017-06-01T14:30:00.123456+00:00",
    "2023-10-22T09:15:30.5-03:00",
    "2020-02-29T00:00:00Z",
    "2000-02-29T12:00:00Z",
    "2023-12-31T00:00:00Z",
    "2021-02-29T00:00:00Z",
    "1900-02-29T00:00:00Z",
    "2020-04-31T00:00:00Z",
    "2023-11-31T00:00:00Z",
    "2020-01-00T00:00:00Z",
    "0000-01-01T00:00:00Z",
    "2020-13-01T00:00:00Z",
    "2020-00-01T00:00:00Z",
    "2020-01-01T24:00:00Z",
    "2020-01-01T00:60:00Z",
    "2020-01-01T00:00:60Z",
    "2020-01-01t00:00:00z",
    "2020-01-01T00:00:00",
    "2020-01-01T00:00:00+5:30",
    "2020-01-01T00:00:00+24:00",
    "2020-01-01 00:00:00Z",
    "2020-01-01T00:00:00Zx",
    "20-01-01T00:00:00Z",
    "2020-1-01T00:00:00Z",
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for s in JOBS:
        fh.write(s + "\n")
