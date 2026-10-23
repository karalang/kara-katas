#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one job per line, either

    g YYYY-MM-DD     convert a Gregorian date to the Jalali (Persian) calendar
    j YYYY-MM-DD     convert a Jalali date to the Gregorian calendar

For each line the job prints the converted date in ISO form plus its
Persian-digit rendering (ASCII digits mapped to U+06F0..U+06F9):

    <iso> <fa>

No persiantools import here (only literal inputs); oracle.py replays each line
through the vendored library to produce expected.out. The dates span leap and
common years in both calendars, Nowruz (Farvardin 1) boundaries, and month
lengths that differ between the 31/30/29-day Jalali months."""

GREG = [
    "1850-01-01",  # earliest modern date in scope
    "1900-03-21",  # a Nowruz
    "1979-02-11",
    "2000-02-29",  # Gregorian leap day
    "2001-03-20",
    "2016-03-20",  # Jalali leap year 1394->1395 boundary region
    "2021-03-21",  # Jalali 1400-01-01 (Nowruz)
    "2023-12-31",
    "2024-02-29",  # Gregorian leap day
    "2024-03-20",
    "2025-03-21",  # Nowruz 1404
    "2026-10-23",  # today
    "2099-12-31",  # latest modern date in scope
]

JALALI = [
    "1228-10-11",  # ~1850 Gregorian
    "1300-01-01",
    "1357-11-22",  # revolution day region
    "1395-12-30",  # Jalali leap day (Esfand 30)
    "1399-12-30",  # Jalali leap day
    "1400-01-01",  # Nowruz
    "1402-06-31",  # a 31-day Shahrivar
    "1403-07-01",  # first 30-day month of the year
    "1403-12-30",  # Jalali leap day
    "1404-01-01",  # Nowruz
    "1404-07-30",
    "1478-12-29",  # ~2099 Gregorian
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for d in GREG:
            fh.write("g " + d + "\n")
        for d in JALALI:
            fh.write("j " + d + "\n")


main()
