#!/usr/bin/env python3
"""Writes data/ for mini_calendar: the job list, team rules and holidays."""
import os

os.makedirs("data", exist_ok=True)

RULES = """\
# name	kind	args (tab-separated)
standup	weekly	Mon,Wed,Fri
retro	nth	2	Tue
board	nth	-1	Thu
payday	last-weekday
rent	day	1
review	day	31
offsite	nth	5	Fri
"""

HOLIDAYS = """\
2026-01-01	New Year's Day
2026-05-25	Memorial Day
2026-07-03	Independence Day (observed)
2026-09-07	Labor Day
2026-11-26	Thanksgiving
2026-12-25	Christmas Day
"""

JOBS = [
    "isleap\t2024", "isleap\t1900", "isleap\t2000", "isleap\t2026",
    "leapdays\t1900\t2025", "leapdays\t2000\t2000", "leapdays\t1\t10000",
    "weekday\t2026\t10\t18", "weekday\t1970\t1\t1", "weekday\t2000\t2\t29",
    "weekday\t1\t1\t1", "weekday\t10000\t3\t1", "weekday\t0\t6\t15",
    "monthrange\t2024\t2", "monthrange\t2026\t2", "monthrange\t1900\t2",
    "monthrange\t2026\t12", "monthrange\t2026\t13", "monthrange\t2026\t0",
    "month\t2026\t2\t0\t0\t0", "month\t2026\t2\t6\t0\t0", "month\t2026\t10\t0\t3\t2",
    "month\t2015\t2\t6\t2\t1", "month\t2026\t3\t2\t9\t1", "month\t1752\t9\t0\t2\t1",
    "month\t2026\t11\t13\t4\t1", "month\t2026\t13\t0\t0\t0",
    "monthcal\t2026\t10\t0", "monthcal\t2026\t2\t6", "monthcal\t2021\t2\t0",
    "days3\t2026\t1\t0", "days3\t2026\t3\t6", "days3\t2026\t12\t3",
    "year\t2024\t6\t2\t1\t6\t3", "year\t2026\t0\t2\t1\t6\t4", "year\t2025\t0\t3\t1\t2\t2",
    "html\t2026\t10\t0", "html\t2026\t2\t6",
    "htmlyear\t2026\t4",
    "timegm\t2026\t10\t18\t9\t30\t0", "timegm\t1970\t1\t1\t0\t0\t0", "timegm\t1969\t12\t31\t23\t59\t59",
    "timegm\t2038\t1\t19\t3\t14\t8",
    "agenda\t2026\t1\t0", "agenda\t2026\t5\t6", "agenda\t2026\t7\t0", "agenda\t2026\t2\t0",
    "workdays\t2026",
]

with open("data/rules.tsv", "w") as f:
    f.write(RULES)
with open("data/holidays.tsv", "w") as f:
    f.write(HOLIDAYS)
with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(JOBS) + "\n")
