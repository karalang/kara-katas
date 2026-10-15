# The oracle: mini_zoneinfo written with Python 3.13's zoneinfo (its
# pure-Python implementation, zoneinfo._zoneinfo) and datetime.
import os
from datetime import datetime, timedelta, timezone
from zoneinfo import _zoneinfo, _common

ZoneInfo = _zoneinfo.ZoneInfo
ROOT = "data/zones"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def keys():
    out = []
    for dirpath, _, names in os.walk(ROOT):
        for n in names:
            out.append(os.path.relpath(os.path.join(dirpath, n), ROOT))
    return sorted(out)

def secs(td):
    return int(td.total_seconds())

def off(td):
    # datetime's offset format, as isoformat writes it
    s = secs(td)
    sign = "-" if s < 0 else "+"
    s = abs(s)
    h, m, sec = s // 3600, s // 60 % 60, s % 60
    return f"{sign}{h:02d}:{m:02d}" + (f":{sec:02d}" if sec else "")

def tti(t):
    return f"{t.tzname} {off(t.utcoff)} dst {secs(t.dstoff)}"

def load(key):
    with open(f"{ROOT}/{key}", "rb") as f:
        return ZoneInfo.from_file(f, key=key)

def rule(r):
    if isinstance(r, _zoneinfo._CalendarOffset):
        d = f"M{r.m}.{r.w}.{r.d}"
    else:
        d = f"{'J' if r.julian else ''}{r.d}"
    return f"{d}/{r.hour * 3600 + r.minute * 60 + r.second}"

def after(a):
    if isinstance(a, _zoneinfo._TZStr):
        return f"rule {tti(a.std)} / {tti(a.dst)}, {rule(a.start)} to {rule(a.end)}"
    return f"fixed {tti(a)}"

def show_zones():
    print("== zones")
    zones = {}
    for key in keys():
        try:
            with open(f"{ROOT}/{key}", "rb") as f:
                raw = _common.load_data(f)
            z = load(key)
        except ValueError as e:
            print(f"{key}: ValueError: {e}")
            continue
        trans_idx, trans_utc, utcoff, isdst, abbr, tz_str = raw
        with open(f"{ROOT}/{key}", "rb") as f:
            version = _common._TZifHeader.from_file(f).version
        print(f"{key}: version {version}, {len(trans_utc)} transitions, {len(utcoff)} types, "
              f"footer {tz_str.decode() if tz_str is not None else None!r}")
        dstoff = ZoneInfo._utcoff_to_dstoff(trans_idx, utcoff, isdst)
        for i in range(len(utcoff)):
            print(f"  type {i}: {abbr[i]} {off(timedelta(seconds=utcoff[i]))} isdst {isdst[i]} dst {dstoff[i]}")
        if trans_utc:
            first = datetime(1970, 1, 1) + timedelta(seconds=trans_utc[0])
            last = datetime(1970, 1, 1) + timedelta(seconds=trans_utc[-1])
            print(f"  first {first.isoformat()}Z, last {last.isoformat()}Z")
        print(f"  before {tti(z._tti_before) if z._tti_before else None}")
        print(f"  after {after(z._tz_after)}")
        zones[key] = z
    return zones

def show_tzstrings():
    print("== tz strings")
    for s in open("data/tzstrings.txt").read().splitlines():
        try:
            r = _zoneinfo._parse_tz_str(s)
        except ValueError as e:
            print(f"{s!r}: ValueError: {e}")
            continue
        print(f"{s!r}: {after(r)}")
        if isinstance(r, _zoneinfo._TZStr):
            for y in (2024, 2025):
                a, b = r.transitions(y)
                da = datetime(1970, 1, 1) + timedelta(seconds=a)
                db = datetime(1970, 1, 1) + timedelta(seconds=b)
                print(f"  {y}: {da.isoformat()} to {db.isoformat()}")

def stamp(z, utc):
    loc = utc.replace(tzinfo=timezone.utc).astimezone(z)
    return loc

def show_local(loc):
    return f"{loc.isoformat()} fold {loc.fold} {loc.tzname()} dst {secs(loc.dst())}"

def show_convert(zones):
    print("== conversions")
    for line in open("data/convert.txt").read().splitlines():
        if not line or line.startswith("#"):
            continue
        w = line.split(" ")
        z = zones[w[1]]
        t = datetime.fromisoformat(w[2])
        if w[0] == "utc":
            print(f"utc {w[1]} {t.isoformat()}Z -> {show_local(stamp(z, t))}")
        else:
            loc = t.replace(tzinfo=z, fold=int(w[3]))
            u = loc.astimezone(timezone.utc).replace(tzinfo=None)
            back = stamp(z, u)
            note = "" if back.replace(tzinfo=None) == t else f" (round trip {back.replace(tzinfo=None).isoformat()})"
            print(f"local {w[1]} {t.isoformat()} fold {w[3]} -> {loc.tzname()} {off(loc.utcoffset())} "
                  f"dst {secs(loc.dst())} = {u.isoformat()}Z{note}")

def state(z, ts):
    loc = stamp(z, datetime(1970, 1, 1) + timedelta(seconds=ts))
    return (secs(loc.utcoffset()), secs(loc.dst()), loc.tzname())

def show_years(zones):
    print("== transitions")
    step = 3 * 3600
    for line in open("data/years.txt").read().splitlines():
        w = line.split(" ")
        z = zones[w[0]]
        for y in w[1:]:
            y = int(y)
            print(f"{w[0]} {y}:")
            lo = int((datetime(y, 1, 1) - datetime(1970, 1, 1)).total_seconds())
            hi = int((datetime(y + 1, 1, 1) - datetime(1970, 1, 1)).total_seconds())
            prev = state(z, lo)
            t = lo
            count = 0
            while t < hi:
                n = min(t + step, hi)
                cur = state(z, n)
                if cur != prev:
                    a, b = t, n   # prev at a, cur at b
                    while b - a > 1:
                        mid = (a + b) // 2
                        if state(z, mid) == prev:
                            a = mid
                        else:
                            b = mid
                    when = datetime(1970, 1, 1) + timedelta(seconds=b)
                    before = (datetime(1970, 1, 1) + timedelta(seconds=b - 1 + prev[0]))
                    print(f"  {when.isoformat()}Z {prev[2]} {off(timedelta(seconds=prev[0]))} -> "
                          f"{cur[2]} {off(timedelta(seconds=cur[0]))} dst {cur[1]}, "
                          f"clocks go from {before.isoformat()} to "
                          f"{(when + timedelta(seconds=cur[0])).isoformat()}")
                    prev = state(z, b)
                    t = b
                    count += 1
                    continue
                t = n
            if count == 0:
                print(f"  none, {prev[2]} {off(timedelta(seconds=prev[0]))} all year")

def show_meetings(zones):
    print("== meetings")
    utc = timezone.utc
    for line in open("data/meetings.txt").read().splitlines():
        if not line or line.startswith("#"):
            continue
        name, org, first, weeks, others = [x.strip() for x in line.split("|")]
        z = zones[org]
        print(f"{name} ({org}):")
        start = datetime.fromisoformat(first)
        for k in range(int(weeks)):
            t = start + timedelta(days=7 * k)
            a = t.replace(tzinfo=z, fold=0)
            b = t.replace(tzinfo=z, fold=1)
            u = a.astimezone(utc)
            back = u.astimezone(z).replace(tzinfo=None)
            head = f"  {DAYS[t.weekday()]} {t.isoformat()} {a.tzname()}"
            if back != t:
                print(f"{head}: does not exist, clocks skip it; moved to {back.isoformat()}")
            elif a.utcoffset() != b.utcoffset():
                print(f"{head}: happens twice, using the first")
            else:
                print(f"{head}")
            for o in others.split(" "):
                loc = u.astimezone(zones[o])
                day = (loc.date() - t.date()).days
                shift = f" ({day:+d} day)" if day else ""
                print(f"    {o}: {DAYS[loc.weekday()]} {loc.strftime('%H:%M')} {loc.tzname()}{shift}")

def main():
    zones = show_zones()
    show_tzstrings()
    show_convert(zones)
    show_years(zones)
    show_meetings(zones)

main()
