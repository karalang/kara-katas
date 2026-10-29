"""The oracle: runs data/jobs.txt on pandas' offsets, holiday calendars,
periods and timedeltas, and prints what mini_pandas_calendar.kara must
print.

  off <ts> <Offset(...)>      the offset's repr and freqstr, ts + offset,
                              ts - offset, rollforward, rollback and
                              is_on_offset
  freq <alias>                to_offset(alias): repr and freqstr
  range k=v ...               pd.date_range (start, end, periods, freq,
                              inclusive, normalize, tz)
  brange k=v ...              pd.bdate_range (also holidays, weekmask, cal)
  hol <cal> <start> <end>     a holiday calendar's holidays, with names
  per <value> <freq>          a Period: repr, bounds and fields
  pasfreq <value> <freq> <to> <how>
  padd <value> <freq> <n>     Period + n
  pfmt <value> <freq> <fmt>   Period.strftime
  pdiff <a> <b> <freq>        Period(b) - Period(a)
  prange k=v ...              pd.period_range (start, end, periods, freq)
  td <string>                 pd.Timedelta: repr, str, isoformat,
                              total_seconds and components
  tdround <td> <freq> <how>   Timedelta.floor / ceil / round
  tsadd <ts> <td>             Timestamp + Timedelta
  busday count|offset|is ...  numpy's busday_count / busday_offset /
                              is_busday
  due <file> <col> <op> <Offset(...)>
                              a column of dates op the offset (add, sub,
                              rollforward, rollback, on), to_csv
  bucket <file> <col> <freq> <val>
                              groupby(col.dt.to_period(freq))[val]
                              .agg(["count", "sum"]), to_csv

An offset is written Name(args) with no spaces: a bare integer is n,
k=v the keywords. A value is an integer, True or False, a list
[a;b;c], MO(-1)-style weekday for DateOffset, cal=us|nyse|uk for a
holiday calendar, or else a string. Each distinct warning
prints once, after the job's output, as `warn: <Category>: <message>`;
`td:<string>` is a Timedelta. Errors print as `! <exception>: <message>`.

Needs pandas 3.0.5 and numpy.
Run: python3 -I -B oracle.py > expected.out"""
import os
import re
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE
from pandas.tseries import offsets as O
from pandas.tseries.frequencies import to_offset
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    EasterMonday,
    GoodFriday,
    Holiday,
    USFederalHolidayCalendar,
    USLaborDay,
    USMartinLutherKingJr,
    USMemorialDay,
    USPresidentsDay,
    USThanksgivingDay,
    nearest_workday,
    next_monday,
    next_monday_or_tuesday,
)

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


class NYSECalendar(AbstractHolidayCalendar):
    rules = [
        Holiday("New Year's Day", month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday("Juneteenth", month=6, day=19, start_date="2022-01-01",
                observance=nearest_workday),
        Holiday("Independence Day", month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday("Christmas", month=12, day=25, observance=nearest_workday),
    ]


class UKCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday("New Year's Day", month=1, day=1, observance=next_monday),
        GoodFriday,
        EasterMonday,
        Holiday("Early May bank holiday", month=5, day=1,
                offset=O.DateOffset(weekday=MO(1))),
        Holiday("Spring bank holiday", month=5, day=31,
                offset=O.DateOffset(weekday=MO(-1))),
        Holiday("Summer bank holiday", month=8, day=31,
                offset=O.DateOffset(weekday=MO(-1))),
        Holiday("Christmas Day", month=12, day=25, observance=next_monday),
        Holiday("Boxing Day", month=12, day=26, observance=next_monday_or_tuesday),
    ]


CALS = {"us": USFederalHolidayCalendar, "nyse": NYSECalendar, "uk": UKCalendar}
WEEKDAYS = {"MO": MO, "TU": TU, "WE": WE, "TH": TH, "FR": FR, "SA": SA, "SU": SU}


def value(v, key=""):
    if key in ("weekmask", "start", "end") and not v.startswith("["):
        return v
    if v.startswith("td:"):
        return pd.Timedelta(v[3:])
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if v in ("True", "False"):
        return v == "True"
    if v.startswith("[") and v.endswith("]"):
        return [x for x in v[1:-1].split(";") if x]
    m = re.fullmatch(r"(MO|TU|WE|TH|FR|SA|SU)\((-?\d+)\)", v)
    if m:
        return WEEKDAYS[m.group(1)](int(m.group(2)))
    return v


def offset(spec):
    m = re.fullmatch(r"(\w+)\((.*)\)", spec)
    cls = getattr(O, m.group(1))
    args, kw = [], {}
    for a in m.group(2).split(",") if m.group(2) else []:
        if "=" in a:
            k, v = a.split("=", 1)
            if k == "cal":
                kw["calendar"] = CALS[v]()
            else:
                kw[k] = value(v, k)
        else:
            args.append(value(a))
    return cls(*args, **kw)


def stamp(s):
    if "@" in s:
        s, tz = s.split("@")
        return pd.Timestamp(s.replace("T", " "), tz=tz)
    return pd.Timestamp(s.replace("T", " "))


def kwargs(opts):
    kw = {}
    for o in opts:
        k, v = o.split("=", 1)
        if k == "cal":
            kw["holidays"] = CALS[v]().holidays().tolist()
        else:
            kw[k] = value(v, k)
    return kw


def dates(idx):
    return " ".join(str(x).replace(" 00:00:00", "") if " 00:00:00" in str(x) and
                    str(x).endswith(" 00:00:00") else str(x) for x in idx)


def show_index(idx):
    print(f"n={len(idx)} freq={idx.freqstr} dtype={idx.dtype}")
    if len(idx):
        print("  " + "\n  ".join(str(x) for x in idx))


def run(job):
    w = job.split()
    cmd = w[0]
    if cmd == "off":
        ts = stamp(w[1])
        off = offset(w[2])
        print(f"repr: {off!r}")
        print(f"freqstr: {off.freqstr}")
        for name, f in (("+", lambda: ts + off), ("-", lambda: ts - off),
                        ("rollforward", lambda: off.rollforward(ts)),
                        ("rollback", lambda: off.rollback(ts)),
                        ("is_on_offset", lambda: off.is_on_offset(ts))):
            try:
                print(f"{name}: {f()}")
            except Exception as e:
                print(f"{name}: ! {type(e).__name__}: {e}")
    elif cmd == "freq":
        off = to_offset(w[1])
        print(f"repr: {off!r}")
        print(f"freqstr: {off.freqstr}")
    elif cmd == "range":
        show_index(pd.date_range(**kwargs(w[1:])))
    elif cmd == "brange":
        show_index(pd.bdate_range(**kwargs(w[1:])))
    elif cmd == "hol":
        h = CALS[w[1]]().holidays(w[2], w[3], return_name=True)
        for d, name in h.items():
            print(f"{d.date()} {d.day_name()[:3]} {name}")
    elif cmd == "per":
        p = pd.Period(w[1], freq=w[2])
        print(f"repr: {p!r}")
        print(f"start_time: {p.start_time}")
        print(f"end_time: {p.end_time}")
        print(f"year={p.year} quarter={p.quarter} qyear={p.qyear} month={p.month} "
              f"day={p.day} dayofweek={p.dayofweek} dayofyear={p.dayofyear} "
              f"week={p.week} days_in_month={p.days_in_month} "
              f"is_leap_year={p.is_leap_year} ordinal={p.ordinal}")
    elif cmd == "pasfreq":
        p = pd.Period(w[1], freq=w[2])
        print(repr(p.asfreq(w[3], how=w[4])))
    elif cmd == "padd":
        p = pd.Period(w[1], freq=w[2])
        print(repr(p + int(w[3])))
    elif cmd == "pfmt":
        p = pd.Period(w[1], freq=w[2])
        print(p.strftime(" ".join(w[3:]).replace("_", " ")))
    elif cmd == "pdiff":
        print(repr(pd.Period(w[2], freq=w[3]) - pd.Period(w[1], freq=w[3])))
    elif cmd == "prange":
        idx = pd.period_range(**kwargs(w[1:]))
        print(f"n={len(idx)} freq={idx.freqstr} dtype={idx.dtype}")
        if len(idx):
            print("  " + " ".join(str(x) for x in idx))
    elif cmd == "td":
        t = pd.Timedelta(w[1].replace("_", " "))
        print(f"repr: {t!r}")
        print(f"str: {t}")
        print(f"isoformat: {t.isoformat()}")
        print(f"total_seconds: {t.total_seconds()!r}")
        print(f"components: {t.components}")
    elif cmd == "tdround":
        t = pd.Timedelta(w[1].replace("_", " "))
        print(repr(getattr(t, w[3])(w[2])))
    elif cmd == "tsadd":
        print(stamp(w[1]) + pd.Timedelta(w[2].replace("_", " ")))
    elif cmd == "busday":
        kw = kwargs([o for o in w[2:] if "=" in o])
        pos = [o for o in w[2:] if "=" not in o]
        if w[1] == "count":
            print(np.busday_count(pos[0], pos[1], **kw))
        elif w[1] == "offset":
            print(np.busday_offset(pos[0], int(pos[1]), **kw))
        else:
            print(np.is_busday(pos[0], **kw))
    elif cmd == "due":
        df = pd.read_csv(os.path.join("data", w[1]))
        col = pd.to_datetime(df[w[2]])
        off = offset(w[4])
        op = w[3]
        if op == "add":
            r = col + off
        elif op == "sub":
            r = col - off
        elif op == "on":
            r = col.map(off.is_on_offset)
        else:
            r = col.map(getattr(off, op))
        df[w[2]] = col
        df["result"] = r
        sys.stdout.write(df.to_csv(index=False))
    elif cmd == "bucket":
        df = pd.read_csv(os.path.join("data", w[1]), parse_dates=[w[2]])
        g = df.groupby(df[w[2]].dt.to_period(w[3]))[w[4]].agg(["count", "sum"])
        sys.stdout.write(g.round(2).to_csv())
    else:
        raise ValueError(f"unknown job {cmd}")


def warned(caught):
    seen = []
    for c in caught:
        line = f"warn: {c.category.__name__}: {c.message}"
        if line not in seen:
            seen.append(line)
    for line in seen:
        print(line)


def main():
    with open("data/jobs.txt", encoding="utf-8") as fh:
        jobs = [l.rstrip("\n") for l in fh if l.strip()]
    for job in jobs:
        print(f"$ {job}")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                run(job)
            except Exception as e:
                warned(caught)
                caught.clear()
                print(f"! {type(e).__name__}: {e}")
        warned(caught)


main()
