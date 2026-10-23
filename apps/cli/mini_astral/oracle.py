#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py for the job kinds) through the vendored
astral and writes expected.out. Each job prints a header naming the call,
then one line per result: datetimes and times as str(), floats as repr(),
and an exception as "<ExceptionType>: <repr of its first argument>".
Run: python3 -I -B oracle.py > expected.out"""
import datetime
import sys

sys.path.insert(0, "vendor")
from astral import (Depression, Observer, SunDirection, dms_to_float,  # noqa: E402
                    hours_to_time, refraction_at_zenith, time_to_hours, time_to_seconds)
from astral import moon, sun  # noqa: E402
from astral.geocoder import all_locations, database, group, lookup  # noqa: E402
from astral.julian import (Calendar, day_fraction_to_time, julianday,  # noqa: E402
                           julianday_2000, julianday_modified, julianday_to_datetime,
                           julianday_to_juliancentury, juliancentury_to_julianday)
from astral.sidereal import gmst, lmst  # noqa: E402

DB = database()


def exc(e):
    arg = e.args[0] if e.args else ""
    return "%s: %r" % (type(e).__name__, arg)


def out(s):
    sys.stdout.write(s + "\n")


def tzinfo(tz):
    if tz == "naive":
        return None
    if tz == "utc":
        return datetime.timezone.utc
    sign = -1 if tz[0] == "-" else 1
    return datetime.timezone(sign * datetime.timedelta(hours=int(tz[1:3]),
                                                       minutes=int(tz[4:6])))


def pdate(s):
    return datetime.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))


def pdatetime(s, tz=None):
    return datetime.datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]),
                             int(s[14:16]), int(s[17:19]), int(s[20:26]), tzinfo=tz)


def observer(lat, lon, el):
    if "/" in el:
        h, d = el.split("/")
        return Observer(lat, lon, (float(h), float(d)))
    return Observer(lat, lon, float(el))


def show(v):
    if isinstance(v, tuple):
        return "(%s)" % ", ".join(show(x) for x in v)
    if isinstance(v, dict):
        return "{%s}" % ", ".join("%s: %s" % (k, show(x)) for k, x in v.items())
    if isinstance(v, (datetime.datetime, datetime.time, datetime.timedelta)):
        return str(v)
    return repr(v)


def call(name, f):
    try:
        r = show(f())
    except (ValueError, OverflowError, KeyError, ZeroDivisionError) as e:
        r = exc(e)
    out("  %s => %s" % (name, r))


def depression(s):
    if s in ("CIVIL", "NAUTICAL", "ASTRONOMICAL"):
        return Depression[s]
    return float(s) if "." in s else int(s)


def day(f):
    o = observer(f[1], f[2], f[3])
    d = pdate(f[4])
    tz = tzinfo(f[5])
    dep = depression(f[6])
    rising, setting = SunDirection.RISING, SunDirection.SETTING
    out("day(%s)" % ", ".join(f[1:]))
    out("  observer => %r %r %r" % (o.latitude, o.longitude, o.elevation))
    call("dawn", lambda: sun.dawn(o, d, tzinfo=tz))
    call("dawn(dep)", lambda: sun.dawn(o, d, dep, tz))
    call("sunrise", lambda: sun.sunrise(o, d, tz))
    call("noon", lambda: sun.noon(o, d, tz))
    call("midnight", lambda: sun.midnight(o, d, tz))
    call("sunset", lambda: sun.sunset(o, d, tz))
    call("dusk", lambda: sun.dusk(o, d, tzinfo=tz))
    call("dusk(dep)", lambda: sun.dusk(o, d, dep, tz))
    call("daylight", lambda: sun.daylight(o, d, tz))
    call("night", lambda: sun.night(o, d, tz))
    call("twilight(rising)", lambda: sun.twilight(o, d, rising, tz))
    call("twilight(setting)", lambda: sun.twilight(o, d, setting, tz))
    call("golden_hour(rising)", lambda: sun.golden_hour(o, d, rising, tz))
    call("golden_hour(setting)", lambda: sun.golden_hour(o, d, setting, tz))
    call("blue_hour(rising)", lambda: sun.blue_hour(o, d, rising, tz))
    call("blue_hour(setting)", lambda: sun.blue_hour(o, d, setting, tz))
    call("rahukaalam(day)", lambda: sun.rahukaalam(o, d, True, tz))
    call("rahukaalam(night)", lambda: sun.rahukaalam(o, d, False, tz))
    call("sun", lambda: sun.sun(o, d, dep, tz))
    for spec in f[7].split(","):
        e, dr, rf = spec.split(":")
        direction = rising if dr == "R" else setting
        call("time_at_elevation(%s, %s, %s)" % (e, dr, rf),
             lambda: sun.time_at_elevation(o, float(e), d, direction, tz, rf == "1"))
    call("moonrise", lambda: moon.moonrise(o, d, tz))
    call("moonset", lambda: moon.moonset(o, d, tz))
    call("phase", lambda: moon.phase(d))


def pos(f):
    o = observer(f[1], f[2], f[3])
    t = pdatetime(f[4], tzinfo(f[5]))
    out("pos(%s)" % ", ".join(f[1:]))
    call("sun.zenith", lambda: sun.zenith(o, t))
    call("sun.zenith(no refraction)", lambda: sun.zenith(o, t, False))
    call("sun.azimuth", lambda: sun.azimuth(o, t))
    call("sun.elevation", lambda: sun.elevation(o, t))
    call("sun.elevation(no refraction)", lambda: sun.elevation(o, t, False))
    call("moon.azimuth", lambda: moon.azimuth(o, t))
    call("moon.elevation", lambda: moon.elevation(o, t))
    call("moon.zenith", lambda: moon.zenith(o, t))


def city(f):
    out("city(%r, %s, %s)" % (f[1], f[2], f[3]))
    try:
        loc = lookup(f[1], DB)
    except KeyError as e:
        out("  " + exc(e))
        return
    if isinstance(loc, dict):
        names = list(loc)
        out("  group of %d names: %s" % (len(names), ", ".join(names[:6])))
        return
    out("  " + repr(loc))
    out("  timezone_group => %r" % (loc.timezone_group,))
    o = loc.observer
    d = pdate(f[2])
    tz = tzinfo(f[3])
    call("sun", lambda: sun.sun(o, d, tzinfo=tz))
    call("moonrise", lambda: moon.moonrise(o, d, tz))


def run(f):
    k = f[0]
    if k == "day":
        day(f)
    elif k == "pos":
        pos(f)
    elif k == "city":
        city(f)
    elif k == "group":
        out("group(%r)" % f[1])
        try:
            g = group(f[1], DB)
        except KeyError as e:
            out("  " + exc(e))
            return
        names = list(g)
        out("  %d names: %s" % (len(names), ", ".join(names)))
        for n in names[:3]:
            for loc in g[n]:
                out("  " + repr(loc))
    elif k == "dms":
        out("dms(%r, %s)" % (f[1], f[2]))
        lim = None if f[2] == "none" else float(f[2])
        call("dms_to_float", lambda: dms_to_float(f[1], lim))
    elif k == "h2t":
        out("h2t(%s)" % f[1])
        call("hours_to_time", lambda: hours_to_time(float(f[1])))
    elif k == "t2h":
        out("t2h(%s)" % ", ".join(f[1:]))
        try:
            t = datetime.time(*[int(x) for x in f[1:]])
        except ValueError as e:
            out("  " + exc(e))
            return
        call("time_to_hours", lambda: time_to_hours(t))
        call("time_to_seconds", lambda: time_to_seconds(t))
    elif k == "refr":
        out("refr(%s)" % f[1])
        call("refraction_at_zenith", lambda: refraction_at_zenith(float(f[1])))
    elif k == "jd":
        out("jd(%s, %s)" % (f[1], f[2]))
        at = pdatetime(f[1]) if "T" in f[1] else pdate(f[1])
        lon = float(f[2])
        call("julianday", lambda: julianday(at))
        call("julianday(julian)", lambda: julianday(at, Calendar.JULIAN))
        if "T" in f[1]:
            call("julianday_modified", lambda: julianday_modified(at))
        call("julianday_2000", lambda: julianday_2000(at))
        jc = julianday_to_juliancentury(julianday(at))
        call("juliancentury", lambda: jc)
        call("julianday(juliancentury)", lambda: juliancentury_to_julianday(jc))
        call("gmst", lambda: gmst(at))
        call("lmst", lambda: lmst(at, lon))
    elif k == "jd2dt":
        out("jd2dt(%s)" % f[1])
        call("julianday_to_datetime", lambda: julianday_to_datetime(float(f[1])))
    elif k == "dft":
        out("dft(%s)" % f[1])
        call("day_fraction_to_time", lambda: day_fraction_to_time(float(f[1])))
    elif k == "m2td":
        out("m2td(%s)" % f[1])
        call("minutes_to_timedelta", lambda: sun.minutes_to_timedelta(float(f[1])))
    elif k == "mpos":
        out("mpos(%s)" % f[1])
        call("moon_position", lambda: moon.moon_position(float(f[1])))
    elif k == "phase":
        out("phase(%s)" % f[1])
        call("phase", lambda: moon.phase(pdate(f[1])))
    else:
        raise SystemExit("unknown job " + k)


with open("data/jobs.tsv", encoding="utf-8") as fh:
    for ln in fh:
        run(ln.rstrip("\n").split("\t"))
n = sum(1 for _ in all_locations(DB))
out("database: %d groups, %d locations" % (len(DB), n))
