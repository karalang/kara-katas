#!/usr/bin/env python3
"""Replays data/jobs.tsv against the vendored holidays 0.62 and prints
what each step returns. A step that raises prints `error <class>: <message>`.

Run: python3 -I -B oracle.py > expected.out"""
import calendar
import os
import sys
from datetime import date, datetime, timedelta

# With no language asked for, gettext reads the locale from these; clear
# them so the names do not depend on the machine.
for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
    os.environ.pop(var, None)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
os.chdir(HERE)

import warnings  # noqa: E402

warnings.simplefilter("ignore")

import holidays  # noqa: E402

env = {}


def key(s):
    if s.startswith("@"):
        v = s[1:]
        return float(v) if "." in v else int(v)
    if s.startswith("date("):
        return date(*map(int, s[5:-1].split(",")))
    if s.startswith("dt("):
        return datetime(*map(int, s[3:-1].split(",")))
    return s


def opts(args):
    kw = {}
    for a in args:
        k, v = a.split("=", 1)
        if k == "years":
            if ".." in v:
                lo, hi = v.split("..")
                kw[k] = range(int(lo), int(hi) + 1)
            elif "," in v:
                kw[k] = [int(x) for x in v.split(",")]
            else:
                kw[k] = int(v)
        elif k in ("observed", "expand"):
            kw[k] = v == "1"
        elif k == "categories":
            kw[k] = tuple(v.split(","))
        elif k == "category":
            kw["categories"] = v
        else:
            kw[k] = v
    return kw


def out(s):
    print("  " + s)


def weekday_name(d):
    return calendar.day_name[d.weekday()]


def payroll(h, year):
    moved = 0
    for m in range(1, 13):
        for day in (15, calendar.monthrange(year, m)[1]):
            d = date(year, m, day)
            if h.is_working_day(d):
                continue
            pay = h.get_nth_working_day(d, -1)
            out(f"{d} {h.get(d) or weekday_name(d)} -> paid {pay} ({weekday_name(pay)})")
            moved += 1
    out(f"{moved} of 24 pay dates moved")


def read_csv(name):
    with open(os.path.join("data", name)) as f:
        rows = [ln.split(",") for ln in f.read().split("\n") if ln]
    return rows[1:]


def sla(name):
    for tid, team, opened, days in read_csv(name):
        try:
            h = env[team]
            due = h.get_nth_working_day(opened, int(days))
            out(f"{tid} {team} opened {opened} +{days} -> due {due} {weekday_name(due)}")
        except Exception as e:
            out(f"{tid} error {type(e).__name__}: {e}")


def pto(name, start, end):
    rows = read_csv(name)
    a = date.fromisoformat(start)
    b = date.fromisoformat(end)
    off = {p: 0 for p, _ in rows}
    d = a
    while d <= b:
        if d.weekday() < 5:
            who = []
            for person, cal in rows:
                h = env[cal]
                if d in h:
                    who.append(f"{person} ({h[d]})")
                    off[person] += 1
            if who:
                out(f"{d} {weekday_name(d)[:3]}: {', '.join(who)}")
        d += timedelta(days=1)
    out("days off: " + ", ".join(f"{p} {n}" for p, n in off.items()))


def trading(h, year):
    total = 0
    for m in range(1, 13):
        first = date(year, m, 1)
        last = date(year, m, calendar.monthrange(year, m)[1])
        n = h.get_working_days_count(first, last)
        total += n
        closed = [f"{d.day} {name}" for d, name in sorted(h.items()) if first <= d <= last]
        out(f"{year}-{m:02d} {n:2d} trading days" + (": " + "; ".join(closed) if closed else ""))
    out(f"{year}: {total} trading days")


def ics_text(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")


def ics(h, year, path):
    days = h[f"{year}-01-01":f"{year + 1}-01-01"]
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//mini_holidays//holidays 0.62//EN"]
    for n, d in enumerate(days, 1):
        lines += [
            "BEGIN:VEVENT",
            f"UID:{d:%Y%m%d}-{n}@mini-holidays",
            f"DTSTART;VALUE=DATE:{d:%Y%m%d}",
            f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}",
            f"SUMMARY:{ics_text(h[d])}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    full = os.path.join("data", "out", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as f:
        f.write(("\r\n".join(lines) + "\r\n").encode("utf-8"))
    with open(full, "rb") as f:
        back = f.read()
    out(f"wrote {path}: {len(back)} bytes, {len(days)} events")
    for ln in back.decode("utf-8").split("\r\n"):
        if ln.startswith("SUMMARY:") or ln.startswith("DTSTART"):
            out(ln)


def run(p):
    op = p[0]
    if op == "country":
        env[p[1]] = holidays.country_holidays(p[2], **opts(p[3:]))
        return
    if op == "market":
        env[p[1]] = holidays.financial_holidays(p[2], **opts(p[3:]))
        return
    if op == "sla":
        return sla(p[1])
    if op == "pto":
        return pto(p[1], p[2], p[3])
    if op == "add":
        env[p[1]] = env[p[2]] + env[p[3]]
        return
    if op == "copy":
        env[p[1]] = env[p[2]].copy()
        return
    h = env[p[1]]
    a = p[2:]
    if op == "items":
        for d, name in h.items():
            out(f"{d} {name}")
    elif op == "sorted":
        for d, name in sorted(h.items()):
            out(f"{d} {name}")
    elif op == "len":
        out(str(len(h)))
    elif op == "bool":
        out(str(bool(h)))
    elif op == "repr":
        out(repr(h))
    elif op == "str":
        out(str(h))
    elif op == "years":
        out(str(h.years))
    elif op == "attrs":
        for name in ("country", "market", "subdiv", "language", "observed", "expand"):
            out(f"{name} = {getattr(h, name, None)!r}")
        out(f"categories = {sorted(h.categories)!r}")
    elif op == "get":
        if len(a) > 1:
            out(repr(h.get(key(a[0]), a[1][1:])))
        else:
            out(repr(h.get(key(a[0]))))
    elif op == "item":
        out(repr(h[key(a[0])]))
    elif op == "in":
        out(str(key(a[0]) in h))
    elif op == "getlist":
        out(repr(h.get_list(key(a[0]))))
    elif op == "named":
        kw = {}
        if len(a) > 1:
            kw["lookup"] = a[1]
        if len(a) > 2:
            kw["split_multiple_names"] = a[2] == "split=1"
        out(repr(h.get_named(a[0], **kw)))
    elif op == "pop":
        if len(a) > 1:
            out(repr(h.pop(key(a[0]), a[1][1:])))
        else:
            out(repr(h.pop(key(a[0]))))
    elif op == "popnamed":
        out(repr(h.pop_named(a[0])))
    elif op in ("update", "append"):
        d = {}
        for kv in a:
            k, v = kv.split("=", 1)
            d[key(k)] = v
        getattr(h, op)(d)
    elif op == "updatelist":
        h.update([key(x) for x in a])
    elif op == "updateone":
        h.update(key(a[0]))
    elif op == "slice":
        if len(a) > 2:
            step = timedelta(days=int(a[2][3:])) if a[2].startswith("td:") else int(a[2])
            out(repr(h[key(a[0]):key(a[1]):step]))
        else:
            out(repr(h[key(a[0]):key(a[1])]))
    elif op == "working":
        out(str(h.is_working_day(key(a[0]))))
    elif op == "nth":
        out(str(h.get_nth_working_day(key(a[0]), int(a[1]))))
    elif op == "count":
        out(str(h.get_working_days_count(key(a[0]), key(a[1]))))
    elif op == "set":
        if a[0] == "categories":
            setattr(h, a[0], set(a[1].split(",")))
        else:
            setattr(h, a[0], a[1] == "1")
    elif op == "eq":
        other = env[a[0]]
        out(f"{h == other} {h != other}")
    elif op == "payroll":
        payroll(h, int(a[0]))
    elif op == "trading":
        trading(h, int(a[0]))
    elif op == "ics":
        ics(h, int(a[0]), a[1])
    else:
        raise SystemExit("unknown op " + op)


def main():
    n = nerr = 0
    with open(os.path.join("data", "jobs.tsv"), encoding="utf-8") as f:
        lines = f.read().split("\n")
    for line in lines:
        if not line:
            continue
        parts = line.split("\t")
        print("> " + " ".join(parts))
        try:
            run(parts)
        except Exception as e:
            out(f"error {type(e).__name__}: {e}")
            nerr += 1
        n += 1
    print(f"{n} steps, {nerr} ended in an error")


main()
