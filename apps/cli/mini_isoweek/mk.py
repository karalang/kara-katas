#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_isoweek: one job per line, tab-separated.

The jobs exercise ISO 8601 week-date arithmetic the way reporting, scheduling
and fiscal-week code does: construction with the library's out-of-range week
normalization (Week(2011,0) rolls back to the previous year, Week(2011,53)
rolls forward past a 52-week year), the string forms (`2011W08` and `2011-W08`)
and their error, mapping a calendar date to its week (with the Jan-1/Dec-31
boundary cases where the ISO year differs from the calendar year), the seven
days of a week, week<->ordinal round-trips, week + n and week - week, contains,
replace, and the 52-vs-53-week-year queries (2020, 2015 and 2009 have 53 weeks).
"""
import os

JOBS = [
    ["str", "2011", "8"],
    ["str", "2011", "0"],         # normalize back into 2010
    ["str", "2010", "53"],
    ["str", "2011", "53"],        # 2011 has 52 weeks -> rolls to 2012W01
    ["str", "2020", "53"],        # 2020 genuinely has 53 weeks
    ["repr", "2011", "35"],
    ["year_week", "2011", "8"],
    ["fromstring", "2011W08"],
    ["fromstring", "2011-W08"],
    ["fromstring", "1999W52"],
    ["fromstring", "bogus"],      # ValueError
    ["withdate", "2011", "2", "22"],
    ["withdate", "2021", "1", "1"],   # 2021-01-01 falls in 2020W53
    ["withdate", "2012", "12", "31"], # 2012-12-31 falls in 2013W01
    ["withdate", "2016", "1", "4"],
    ["day", "2011", "8", "0"],
    ["day", "2011", "8", "6"],
    ["monday", "2020", "1"],
    ["sunday", "2020", "1"],
    ["days", "2011", "8"],
    ["toordinal", "2011", "8"],
    ["fromordinal", "104911"],
    ["add", "2011", "52", "1"],       # across the year boundary
    ["add", "2020", "53", "1"],
    ["sub_int", "2011", "1", "1"],
    ["sub_week", "2011", "8", "2011", "1"],
    ["sub_week", "2012", "1", "2010", "52"],
    ["contains", "2011", "8", "2011", "2", "21"],   # Monday of W08
    ["contains", "2011", "8", "2011", "2", "28"],   # next Monday, outside
    ["replace_week", "2011", "8", "20"],
    ["replace_year", "2011", "8", "2015"],
    ["last_week_of_year", "2020"],    # 53
    ["last_week_of_year", "2021"],    # 52
    ["weeks_of_year", "2015"],        # 53-week year
    ["weeks_of_year", "2011"],        # 52-week year
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for job in JOBS:
        fh.write("\t".join(job) + "\n")
