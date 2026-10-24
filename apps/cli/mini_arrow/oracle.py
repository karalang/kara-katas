#!/usr/bin/env python3
"""Runs data/jobs.jsonl through the real arrow 1.3.0 on python-dateutil
2.9.0.post0 and prints what mini_arrow.kara must print. Both come from
vendor/ (or ARROW_VENDOR); dateutil also imports six, which is not
vendored. The local zone is pinned to UTC, and dateutil looks zones up
only in data/zones.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os, sys, time
os.environ["TZ"] = "UTC"
time.tzset()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.environ.get("ARROW_VENDOR", os.path.join(HERE, "vendor"))]
import json, datetime
import arrow
import dateutil
from dateutil import tz as dtz
from arrow import locales as alocales
from arrow.parser import TzinfoParser

assert arrow.__version__ == "1.3.0"
assert dateutil.__version__ == "2.9.0.post0"
dtz.tz.TZPATHS[:] = ["data/zones"]
dtz.gettz.cache_clear()


def err(e):
    return "%s: %s" % (type(e).__name__, e)


def tzobj(x):
    return TzinfoParser.parse(x)


def conv(v):
    # a job argument as the Python value it stands for
    if isinstance(v, dict):
        if "tuple" in v:
            return tuple(v["tuple"])
        if "tz" in v and len(v) == 1:
            return tzobj(v["tz"])
        if "dt" in v:
            t = v.get("tz")
            return datetime.datetime(*v["dt"], tzinfo=tzobj(t) if t else None)
        if "date" in v:
            return datetime.date(*v["date"])
    return v


def build(spec):
    if "get" in spec:
        kw = {k: conv(v) for k, v in spec.get("kw", {}).items()}
        return arrow.get(*[conv(a) for a in spec["get"]], **kw)
    if "new" in spec:
        kw = {}
        if "tz" in spec:
            kw["tzinfo"] = spec["tz"]
        if "fold" in spec:
            kw["fold"] = spec["fold"]
        return arrow.Arrow(*spec["new"], **kw)
    if "ts" in spec:
        return arrow.Arrow.fromtimestamp(spec["ts"], spec.get("tz"))
    if "uts" in spec:
        return arrow.Arrow.utcfromtimestamp(spec["uts"])
    if "ord" in spec:
        return arrow.Arrow.fromordinal(spec["ord"])
    if "min" in spec:
        return arrow.Arrow.min
    if "max" in spec:
        return arrow.Arrow.max
    raise SystemExit("bad spec %r" % spec)


def other_of(spec):
    if isinstance(spec, str):
        return spec
    if "naive" in spec:
        return datetime.datetime(*spec["naive"])
    if "aware" in spec:
        return datetime.datetime(*spec["aware"], tzinfo=tzobj(spec["tz"]))
    return build(spec)


def info(a):
    return ("weekday=%d isoweekday=%d %r week=%d quarter=%d ts=%r int_ts=%d utcoffset=%r dst=%r "
            "tzname=%r fold=%d ambiguous=%r imaginary=%r ordinal=%d" % (
                a.weekday(), a.isoweekday(), a.isocalendar(), a.week, a.quarter, a.timestamp(),
                a.int_timestamp, a.utcoffset(), a.dst(), a.tzname(), a.fold, a.ambiguous,
                a.imaginary, a.toordinal()))


def show_pair(p):
    return "(%r, %r)" % p


def run_op(a, op):
    name = op[0]
    if name == "repr":
        print(repr(a))
    elif name == "info":
        print(info(a))
    elif name == "tzrepr":
        print(repr(a.tzinfo))
    elif name == "fmt":
        if op[1] is None:
            print(a.format())
        elif len(op) > 2:
            print(a.format(op[1], op[2]))
        else:
            print(a.format(op[1]))
    elif name == "ords":
        for loc in ["en", "fr", "es", "it", "de", "fi", "ko", "nl", "pl"]:
            l = alocales.get_locale(loc)
            print(loc, " ".join(l.ordinal_number(n) for n in
                                [1, 2, 3, 4, 10, 11, 12, 13, 21, 22, 23, 31, 101, 111, 112, -1, -2, -11]))
    elif name == "to":
        a = a.to(op[1])
        print(repr(a))
    elif name == "shift":
        a = a.shift(**op[1])
        print(repr(a))
    elif name == "replace":
        a = a.replace(**op[1])
        print(repr(a))
    elif name == "add":
        a = a + datetime.timedelta(**op[1])
        print(repr(a))
    elif name == "span":
        print(show_pair(a.span(op[1], **op[2])))
    elif name == "floor":
        print(repr(a.floor(op[1])))
    elif name == "ceil":
        print(repr(a.ceil(op[1])))
    elif name in ("range", "span_range", "interval"):
        end = build(op[2]) if op[2] is not None else None
        kw = dict(op[3])
        if name == "range":
            it = arrow.Arrow.range(op[1], a, end, **kw)
        elif name == "span_range":
            it = arrow.Arrow.span_range(op[1], a, end, **kw)
        else:
            it = arrow.Arrow.interval(op[1], a, end, **kw)
        n = 0
        try:
            for x in it:
                n += 1
                print("  " + (repr(x) if name == "range" else show_pair(x)))
        finally:
            print("  %d items" % n)
    elif name == "humanize":
        print(a.humanize(other_of(op[1]), **op[2]))
    elif name == "humanize_shift":
        print(a.shift(**op[1]).humanize(a, **op[2]))
    elif name == "dehumanize":
        print(repr(a.dehumanize(op[1], op[2])))
    elif name == "cmp":
        b = build(op[1])
        print("== %s != %s < %s <= %s > %s >= %s a-b %r b-a %r" % (
            a == b, a != b, a < b, a <= b, a > b, a >= b, a - b, b - a))
    elif name == "between":
        print(a.is_between(build(op[1]), build(op[2]), op[3]))
    elif name == "iso":
        print(a.isoformat(op[1], op[2]))
    else:
        raise SystemExit("bad op %r" % op)
    return a


def run_ops(j):
    try:
        a = build(j["a"])
    except Exception as e:
        print(err(e))
        return
    for op in j["ops"]:
        try:
            a = run_op(a, op)
        except Exception as e:
            print(err(e))


def fields(line):
    return [x.strip() for x in line.split("|")]


def data_lines(name):
    out = []
    for line in open("data/" + name, encoding="utf-8").read().split("\n"):
        if line and not line.startswith("#"):
            out.append(line)
    return out


def utc_iso(a):
    return a.to("UTC").isoformat()


def run_logs():
    fmts = {}
    for line in data_lines("formats.txt"):
        f = fields(line)
        fmts[f[0]] = (f[1], f[2:])
    hours = {}
    per = {}
    stamps = []
    for line in data_lines("app.log"):
        svc, _, rest = line.partition(" ")
        if svc not in fmts:
            print("%-7s no format for this service" % svc)
            continue
        zone, tried = fmts[svc]
        if svc == "audit":
            text = rest.split()[0]
        elif svc == "api":
            kv = dict(x.split("=", 1) for x in rest.split())
            text = kv["ts"]
        else:
            text = rest
        try:
            a = arrow.get(text, tried, normalize_whitespace=True)
            if zone != "-":
                a = a.replace(tzinfo=zone)
            if a.year == 1:
                a = a.replace(year=2024)
            elif a.year == 1970 and svc != "audit":
                # a weekday and a time: that day in the week the log covers
                week = arrow.get("2024-03-04", tzinfo=zone)
                a = week.shift(weekday=a.weekday()).replace(hour=a.hour, minute=a.minute)
        except Exception as e:
            print("%-7s %s" % (svc, err(e)))
            continue
        flag = ""
        if a.imaginary:
            flag = " (no such local time)"
        elif a.ambiguous:
            flag = " (ambiguous)"
        print("%-7s %s  local %s%s" % (svc, utc_iso(a), a.format("ddd HH:mm:ss ZZ"), flag))
        h = a.to("UTC").floor("hour")
        hours[h] = hours.get(h, 0) + 1
        per.setdefault(svc, []).append(a)
        stamps.append(a)
    print("by hour (UTC):")
    for h in sorted(hours):
        print("  %s  %s %d" % (h.format("YYYY-MM-DD HH:mm"), "#" * hours[h], hours[h]))
    print("by service:")
    for svc in sorted(per):
        xs = sorted(per[svc])
        print("  %-7s %d lines, %s .. %s" % (svc, len(xs), utc_iso(xs[0]), utc_iso(xs[-1])))
    first, last = min(stamps), max(stamps)
    print("window: %s (%s)" % (last.humanize(first, granularity=["hour", "minute", "second"], only_distance=True),
                              first.humanize(last)))


def run_meetings():
    now = arrow.get("2024-03-01T12:00:00+00:00")
    for line in data_lines("meetings.txt"):
        title, zone, when, minutes, repeat, who = fields(line)
        try:
            start = arrow.get(when, "YYYY-MM-DD HH:mm", tzinfo=zone)
        except Exception as e:
            print("%s: %s" % (title, err(e)))
            continue
        notes = []
        if start.imaginary:
            notes.append("does not exist on the organizer's clock")
        if start.ambiguous:
            notes.append("happens twice on the organizer's clock")
        print("%s, %s, %s (%s)%s" % (title, start.format("dddd D MMMM YYYY HH:mm ZZZ"), start.humanize(now),
                                    utc_iso(start), "".join("; " + n for n in notes)))
        starts = [start] if repeat == "once" else list(arrow.Arrow.range("week", start, limit=4))
        zones = [z.strip() for z in who.split(",")]
        for s in starts:
            end = s.shift(minutes=int(minutes))
            parts = []
            for z in zones:
                ls, le = s.to(z), end.to(z)
                mark = ""
                if ls.hour < 8 or le.hour > 18 or (le.hour == 18 and le.minute > 0):
                    mark = "*"
                day = ""
                if ls.date() != s.date():
                    day = " (%s)" % ls.format("ddd")
                parts.append("%s %s-%s%s%s" % (z.split("/")[-1], ls.format("HH:mm"), le.format("HH:mm"), day, mark))
            print("  %s  %s" % (s.format("YYYY-MM-DD HH:mm ZZ"), " | ".join(parts)))


def run_billing():
    for line in data_lines("subscriptions.txt"):
        sid, plan, start, cancel, zone = fields(line)
        plan = int(plan)
        try:
            s = arrow.get(start, tzinfo=zone)
            e = arrow.get(cancel, tzinfo=zone) if cancel != "-" else s.shift(months=4)
        except Exception as ex:
            print("%s: %s" % (sid, err(ex)))
            continue
        print("%s %s, %s to %s%s" % (sid, zone, s.format("MMM D, YYYY HH:mm"), e.format("MMM D, YYYY HH:mm"),
                                     "" if cancel != "-" else " (open, four months shown)"))
        total = 0
        for lo, hi in arrow.Arrow.span_range("month", s, e, tz=zone):
            a = max(lo, s)
            b = min(hi, e)
            used = b - a
            full = hi - lo
            us = used.days * 86400 + used.seconds
            fs = full.days * 86400 + full.seconds
            cents = plan * us // fs
            total += cents
            print("  %s  %8s of %8s s  %6.2f" % (lo.format("YYYY-MM"), us, fs, cents / 100))
        print("  total %.2f" % (total / 100))
        print("  renewals: %s" % ", ".join(r.format("ddd MMM D") for r in arrow.Arrow.range("month", s, limit=5)))


def run_feed():
    now = arrow.get("2024-05-15T12:00:00+00:00")
    groups = {}
    for line in data_lines("feed.txt"):
        user, loc, zone, when, what = fields(line)
        try:
            t = arrow.get(when).to(zone)
            ago = t.humanize(now, locale=loc)
        except Exception as e:
            print("%s: %s" % (user, err(e)))
            continue
        local_now = now.to(zone)
        if t > local_now:
            group = "upcoming"
        elif t.is_between(*local_now.span("day"), "[]"):
            group = "today"
        elif t.is_between(*local_now.shift(days=-1).span("day"), "[]"):
            group = "yesterday"
        elif t.is_between(*local_now.span("week"), "[]"):
            group = "this week"
        else:
            group = "earlier"
        groups[group] = groups.get(group, 0) + 1
        try:
            back = now.dehumanize(ago, locale=loc)
            rt = "back to %s" % back.format("YYYY-MM-DD HH:mm")
        except Exception as e:
            rt = err(e)
        print("%s [%s] %s, %s, %s; %s" % (user, group, what, ago, t.format("ddd D MMM HH:mm", locale=loc), rt))
    print("groups: " + ", ".join("%s %d" % (g, groups[g]) for g in
                                 ["upcoming", "today", "yesterday", "this week", "earlier"] if g in groups))


for n, line in enumerate(open("data/jobs.jsonl", encoding="utf-8"), 1):
    j = json.loads(line)
    print("== %d %s" % (n, j["n"]))
    if j["kind"] == "ops":
        run_ops(j)
    else:
        globals()["run_" + j["kind"]]()
