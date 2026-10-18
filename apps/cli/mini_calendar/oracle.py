#!/usr/bin/env python3
"""Runs data/jobs.tsv with Python's calendar module and prints expected.out."""
import calendar
import datetime

ABBR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def load_rules():
    rules = []
    for line in open("data/rules.tsv"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        rules.append(line.split("\t"))
    return rules


def load_holidays():
    out = {}
    for line in open("data/holidays.tsv"):
        line = line.rstrip("\n")
        if line:
            d, name = line.split("\t")
            out[d] = name
    return out


def is_workday(y, m, d, hol):
    return calendar.weekday(y, m, d) < 5 and f"{y:04d}-{m:02d}-{d:02d}" not in hol


def rule_days(rule, y, m, hol):
    _, n = calendar.monthrange(y, m)
    kind = rule[1]
    if kind == "weekly":
        want = [ABBR.index(a) for a in rule[2].split(",")]
        return [d for d in range(1, n + 1) if calendar.weekday(y, m, d) in want]
    if kind == "nth":
        k = int(rule[2])
        wd = ABBR.index(rule[3])
        days = [d for d in range(1, n + 1) if calendar.weekday(y, m, d) == wd]
        idx = k - 1 if k > 0 else len(days) + k
        return [days[idx]] if 0 <= idx < len(days) else []
    if kind == "last-weekday":
        d = n
        while not is_workday(y, m, d, hol):
            d -= 1
        return [d]
    if kind == "day":
        return [min(int(rule[2]), n)]
    return []


def agenda(y, m, first):
    print(calendar.TextCalendar(first).formatmonth(y, m), end="")
    hol = load_holidays()
    rules = load_rules()
    _, n = calendar.monthrange(y, m)
    events = {d: [] for d in range(1, n + 1)}
    for r in rules:
        for d in rule_days(r, y, m, hol):
            events[d].append(r[0])
    for d in range(1, n + 1):
        key = f"{y:04d}-{m:02d}-{d:02d}"
        names = list(events[d])
        if key in hol:
            names.insert(0, "holiday: " + hol[key])
        if names:
            print(f"  {key} {ABBR[calendar.weekday(y, m, d)]}  {', '.join(names)}")


def workdays(y):
    hol = load_holidays()
    total = 0
    for m in range(1, 13):
        _, n = calendar.monthrange(y, m)
        work = 0
        off = 0
        for d in range(1, n + 1):
            if calendar.weekday(y, m, d) < 5:
                if f"{y:04d}-{m:02d}-{d:02d}" in hol:
                    off += 1
                else:
                    work += 1
        total += work
        note = f" ({off} holiday{'s' if off != 1 else ''})" if off else ""
        print(f"  {calendar.month_abbr[m]} {work} workdays{note}")
    print(f"  total {total}")


def run(f):
    k = f[0]
    a = [int(x) for x in f[1:]]
    if k == "isleap":
        print(f"  {calendar.isleap(a[0])}")
    elif k == "leapdays":
        print(f"  {calendar.leapdays(a[0], a[1])}")
    elif k == "weekday":
        d = calendar.weekday(a[0], a[1], a[2])
        print(f"  {int(d)} {calendar.day_name[d]}")
    elif k == "monthrange":
        try:
            d, n = calendar.monthrange(a[0], a[1])
            print(f"  {int(d)} {n}")
        except calendar.IllegalMonthError as e:
            print(f"  IllegalMonthError: {e}")
    elif k == "month":
        try:
            print(calendar.TextCalendar(a[2]).formatmonth(a[0], a[1], a[3], a[4]), end="")
        except calendar.IllegalMonthError as e:
            print(f"  IllegalMonthError: {e}")
    elif k == "monthcal":
        print(f"  {calendar.Calendar(a[2]).monthdayscalendar(a[0], a[1])}")
    elif k == "days3":
        days = list(calendar.Calendar(a[2]).itermonthdays3(a[0], a[1]))
        print(f"  {len(days)} days, {days[0]} .. {days[-1]}")
    elif k == "year":
        print(calendar.TextCalendar(a[1]).formatyear(a[0], a[2], a[3], a[4], a[5]), end="")
    elif k == "html":
        print(calendar.HTMLCalendar(a[2]).formatmonth(a[0], a[1]), end="")
    elif k == "htmlyear":
        print(calendar.HTMLCalendar().formatyear(a[0], a[1]))
    elif k == "timegm":
        print(f"  {calendar.timegm(tuple(a))}")
    elif k == "agenda":
        agenda(a[0], a[1], a[2])
    elif k == "workdays":
        workdays(a[0])


for raw in open("data/jobs.tsv"):
    fields = raw.rstrip("\n").split("\t")
    print("== " + " | ".join(fields))
    run(fields)
