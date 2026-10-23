#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored timeago 1.0.16, printing
what mini_timeago.kara must print.

Each op prints "> format(<args>)" or "> parse(<arg>)" with its arguments
as repr() shows them, then "  -> <result>" (a str as itself, anything
else as its repr) or "  error <Class>: <str(e)>". A job prints
"== name".

Two things are pinned so the run is reproducible: the time zone is UTC,
which datetime.fromtimestamp() reads, and date.today(), which the parser
uses for a time with no date, is 2026-10-23. date.today() is pinned by
handing the parser a subclass of date whose today() is fixed; the date
values in the jobs are built from the same subclass, so the parser's
isinstance() checks see them as dates.

Run: python3 -I -B oracle.py > expected.out"""
import datetime as dtm
import os
import sys
import time

os.environ["TZ"] = "UTC"
time.tzset()

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import timeago  # noqa: E402
from timeago import parser  # noqa: E402


class FixedDate(dtm.date):
    @classmethod
    def today(cls):
        return cls(2026, 10, 23)

    def __repr__(self):
        return dtm.date.__repr__(self).replace("FixedDate", "datetime.date")


parser.date = FixedDate

OUT = []


def emit(s):
    OUT.append(s)


def dec(w):
    if w == "n":
        return None
    if w == "l":
        return []
    t, v = w.split(":", 1)
    if t == "b":
        return v == "1"
    if t == "i":
        return int(v)
    if t == "f":
        return float(v)
    if t == "s":
        return bytes.fromhex(v).decode("utf-8")
    n = [int(x) for x in v.split(",")]
    if t == "d":
        return FixedDate(*n)
    if t == "td":
        return dtm.timedelta(days=n[0], seconds=n[1], microseconds=n[2])
    assert t == "dt", w
    tz = None
    if len(n) == 8:
        tz = dtm.timezone(dtm.timedelta(seconds=n[7]))
    return dtm.datetime(*n[:7], tzinfo=tz)


def result(r):
    return r if isinstance(r, str) else repr(r)


def main():
    with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as fh:
        lines = [ln for ln in fh.read().split("\n") if ln]
    for line in lines:
        f = line.split("\t")
        if f[0] == "job":
            emit("== " + f[1])
            continue
        args = [dec(w) for w in f[1:]]
        emit("> %s(%s)" % (f[0], ", ".join(repr(a) for a in args)))
        try:
            if f[0] == "format":
                r = timeago.format(*args)
            else:
                r = parser.parse(*args)
            emit("  -> " + result(r))
        except Exception as e:  # noqa: BLE001
            emit("  error %s: %s" % (type(e).__name__, e))
    sys.stdout.buffer.write(("\n".join(OUT) + "\n").encode("utf-8"))


main()
