#!/usr/bin/env python3
"""Writes data/jobs.tsv: the "3 hours ago" labels of a team's activity
feed (commits, deploys, comments and scheduled jobs) in every language the
product ships, as calls on timeago.format() and timeago.parser.parse().

Each line is one op, tab-separated: "job<TAB>name" starts a job;
"format<TAB>date[<TAB>now[<TAB>locale]]" and "parse<TAB>value" are calls.
A value is "n" (None), "b:0"/"b:1", "i:<int>", "f:<float repr>",
"s:<hex>" (a str, UTF-8 in hex), "l" (an empty list), "d:Y,M,D" (a date),
"dt:Y,M,D,h,m,s,us" (a naive datetime) or "dt:Y,M,D,h,m,s,us,off" (one
with a fixed UTC offset of off seconds), and "td:days,seconds,us" (a
timedelta built from those arguments).

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = []

LOCALES = [
    "ar", "bg", "ca", "da", "de", "el", "en", "en_short", "es", "eu",
    "fa_IR", "fi", "fr", "gl", "guj_IN", "he", "hu", "in_BG", "in_HI",
    "in_ID", "is", "it", "ja", "ko", "lt", "ml", "my", "nb_NO", "nl",
    "nn_NO", "pl", "pt_BR", "pt_PT", "ro", "ru", "sk", "sv_SE", "ta", "th",
    "tr", "uk", "vi", "zh_CN", "zh_TW",
]


def s(text):
    return "s:" + text.encode("utf-8").hex()


def i(n):
    return "i:%d" % n


def f(x):
    return "f:" + repr(x)


def d(y, m, dd):
    return "d:%d,%d,%d" % (y, m, dd)


def dt(y, m, dd, h=0, mi=0, sec=0, us=0, off=None):
    v = "dt:%d,%d,%d,%d,%d,%d,%d" % (y, m, dd, h, mi, sec, us)
    return v if off is None else v + ",%d" % off


def td(days=0, seconds=0, us=0):
    return "td:%d,%d,%d" % (days, seconds, us)


def job(name):
    LINES.append("job\t" + name)


def fmt(*vals):
    LINES.append("\t".join(["format"] + list(vals)))


def parse(v):
    LINES.append("parse\t" + v)


NOW = dt(2026, 10, 23, 14, 30, 0)

# ---------------------------------------------------------------- the feed

job("activity feed")
for when, what in [
    ("2026-10-23 14:29:58", "commit"), ("2026-10-23 14:29:49", "comment"),
    ("2026-10-23 14:29:10", "review"), ("2026-10-23 14:28:30", "deploy"),
    ("2026-10-23 14:01:00", "issue"), ("2026-10-23 12:30:00", "release"),
    ("2026-10-23 0:0:0", "backup"), ("2026-10-22 14:30:01", "merge"),
    ("2026-10-20 9:15:00", "branch"), ("2026-10-09 14:30:00", "tag"),
    ("2026-09-23 14:30:00", "milestone"), ("2026-04-01 8:00:00", "fork"),
    ("2025-10-23 14:30:00", "repo"), ("2016/5/27 21:22:20", "account"),
    ("2026-10-23 14:31:00", "cron"), ("2026-10-24 3:00:00", "maintenance"),
    ("2026-12-25 0:0:0", "holiday"), ("2030-1-1 0:0:0", "certificate"),
]:
    fmt(s(when), s("2026-10-23 14:30:00"))
    fmt(s(when), NOW, s("de"))
    fmt(s(when), NOW, s("zh_CN"))

# ---------------------------------------------------------------- units

job("unit boundaries")
LADDER = [0, 1, 9, 10, 11, 59, 60, 61, 119, 120, 121, 179, 180, 3599, 3600,
          3601, 7199, 7200, 86399, 86400, 86401, 172799, 172800, 604799,
          604800, 604801, 1209599, 1209600, 2627999, 2628000, 2628001,
          5255999, 5256000, 31535999, 31536000, 31536001, 63071999,
          63072000, 315360000, 3153600000, 31536000000]
for n in LADDER:
    fmt(td(seconds=n))
    fmt(td(seconds=-n))
fmt(td(us=999999))
fmt(td(us=-999999))
fmt(td(seconds=10, us=999999))
fmt(td(seconds=-10, us=-1))
fmt(td(days=-1, seconds=86390))
fmt(td(days=3, seconds=-1))
fmt(td(days=29, seconds=36000))
fmt(td(days=30, seconds=36000))
fmt(td(days=31))
fmt(td(days=365 * 4 + 1))
fmt(td(days=999999999))
fmt(td(days=-999999999))

job("every locale")
LADDER2 = [0, 10, 45, 60, 150, 3600, 10800, 86400, 259200, 604800,
           1814400, 2628000, 7884000, 31536000, 94608000]
for loc in LOCALES:
    for n in LADDER2:
        fmt(td(seconds=-n), NOW, s(loc))
        fmt(td(seconds=n), NOW, s(loc))

job("plural rules")
for loc in ["ru", "uk", "pl", "lt", "ar", "sk"]:
    for n in list(range(10, 60)):
        fmt(td(seconds=n), NOW, s(loc))
        fmt(td(seconds=-n), NOW, s(loc))
    for n in range(1, 60):
        fmt(td(seconds=60 * n), NOW, s(loc))
        fmt(td(seconds=-60 * n), NOW, s(loc))
    for n in list(range(1, 26)) + list(range(100, 126)) + [1000, 1001, 1012, 1022]:
        fmt(td(days=365 * n), NOW, s(loc))
        fmt(td(days=-365 * n), NOW, s(loc))

# ---------------------------------------------------------------- locales

job("locale names")
for loc in [None, "en", "EN", "", "xx", "zh-CN", "zh", "en.short", "pt",
            "ru ", 5, "fr"]:
    v = "n" if loc is None else (i(loc) if isinstance(loc, int) else s(loc))
    fmt(td(seconds=-7200), NOW, v)
    fmt(td(seconds=7200), NOW, v)

# ---------------------------------------------------------------- parsing

job("parser")
for text in ["2016-5-27 21:22:20", "2016-05-27 21:22:2", "2016/05/27 21:22:2",
             "2016-05-27", "2016/5/27", "21:22:2", "00:00:00", "23:59:59",
             "2016-5-27-99 1:2:3:4", "2016-02-29", "2015-02-29", "2016-13-01",
             "2016-00-10", "0-1-1", "1-1-1", "9999-12-31 23:59:59",
             "10000-1-1", "2016-4-31", "24:00:00", "12:60:00", "12:00:60",
             "10:20", "2016-5", "2016-05-27T10:00:00", "2016-05-27  10:00:00",
             " 2016-05-27 10:00:00", "2016-05-27 10:00:00 ", "2016-05-27 ",
             "", "today", "-", ":", "2016--27", "+2016-+5-+27",
             "2016-05-27\t", "2_016-5-2_7", "٢٠١٦-٥-٢٧ ١٠:٣٠:٠٠", "１２:３４:５６",
             "2016-5-27 -1:2:3", "2016-5-27 1:2:3.5", "0x10-1-1"]:
    parse(s(text))
for v in [d(2016, 5, 27), d(2000, 2, 29), dt(2016, 5, 27, 21, 22, 20),
          dt(2016, 5, 27, 21, 22, 20, 1500), dt(2016, 5, 27, 21, 22),
          dt(2016, 5, 27), dt(2016, 5, 27, 21, 22, 20, 0, 19800),
          dt(2016, 5, 27, 21, 22, 20, 0, -18000), dt(2016, 5, 27, 0, 0, 0, 7, 0),
          i(0), i(1), i(-1), i(86399), i(1464384140), i(1800000000),
          i(-2208988800), f(0.0), f(1.5), f(-1.5), f(0.0000005), f(0.0000015),
          f(0.0000025), f(-0.0000005), f(1464384140.123456), f(1e9 + 0.9999996),
          f(-0.9999996), "b:1", "b:0", "n", "l"]:
    parse(v)

job("format inputs")
for date, now in [
    (s("2016-5-27 21:22:20"), s("2016-5-27 21:22:30")),
    (s("2016-5-27 21:22:20"), s("2016-5-27 21:22:31")),
    (s("2016-05-27"), s("2016-05-28")),
    (s("2016-05-27"), s("2016-06-28 12:00:00")),
    (d(2016, 5, 27), s("2016/5/27 0:0:15")),
    (s("10:00:00"), s("10:05:00")),
    (s("23:59:59"), s("00:00:00")),
    (i(1464384140), i(1464387740)),
    (i(1464384140), s("2016-5-27 21:22:20")),
    (f(1.5), f(12.4)),
    (f(1.5), f(12.5)),
    (f(0.0), f(10.9999996)),
    ("b:0", "b:1"),
    (dt(2016, 5, 27, 21, 22, 20, 0, 0), dt(2016, 5, 27, 23, 22, 20, 0, 7200)),
    (dt(2016, 5, 27, 21, 22, 20, 0, 19800), dt(2016, 5, 27, 21, 22, 20, 0, 0)),
    (dt(2016, 5, 27, 21, 22, 20, 0, -18000), dt(2016, 5, 27, 21, 22, 20, 0, 3600)),
    (dt(2016, 5, 27, 21, 22, 20), dt(2016, 5, 27, 21, 22, 20, 0, 0)),
    (dt(2016, 5, 27, 21, 22, 20, 0, 0), s("2016-5-27 21:22:20")),
    (dt(2016, 5, 27, 21, 22, 20, 999999), dt(2016, 5, 27, 21, 22, 31)),
    (dt(2016, 5, 27, 21, 22, 20, 1), dt(2016, 5, 27, 21, 22, 31)),
    (dt(1, 1, 1), dt(9999, 12, 31, 23, 59, 59, 999999)),
    (dt(9999, 12, 31, 23, 59, 59, 999999), dt(1, 1, 1)),
    (s("2016-13-01"), s("2016-05-28")),
    (s("2016-05-28"), s("2016-13-01")),
    (s("2016-13-01"), s("2016-13-01")),
    ("n", NOW),
    ("l", NOW),
    (NOW, "l"),
    (s(""), NOW),
    (td(seconds=30), s("not a date")),
    (td(seconds=30), "l"),
]:
    fmt(date, now)
    fmt(date, now, s("fr"))
fmt(td(seconds=-30))
fmt(td(seconds=-30), "n")
fmt(td(seconds=-30), "n", "n")

os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
with open(os.path.join(HERE, "data", "jobs.tsv"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(LINES) + "\n")
