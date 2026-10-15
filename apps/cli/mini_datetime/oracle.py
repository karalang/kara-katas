# The oracle for mini_datetime: the same program written with Python
# 3.13's datetime (the C implementation) and _strptime. Run it from this
# directory after mk.py writes data/, under LC_ALL=C and TZ=UTC: strftime
# then comes from glibc in the C locale, and %Z and %s see UTC as local.
from datetime import date, datetime, time, timedelta, timezone


def lines(path):
    with open(path) as f:
        return [l for l in f.read().split("\n") if l and not l.startswith("#")]


def show(dt):
    s = dt.isoformat()
    if getattr(dt, "tzinfo", None) is not None:
        s += f" [{dt.tzname()}]"
    return s


def err(e):
    return f"{type(e).__name__}: {e}"


def section_strptime():
    print("== strptime")
    for l in lines("data/strptime.txt"):
        s, _, f = l.partition(" | ")
        try:
            out = show(datetime.strptime(s, f))
        except Exception as e:
            out = err(e)
        print(f"{s!r} {f!r}: {out}")


SAMPLES = [
    datetime(2026, 10, 15, 8, 0, 1, 250000, tzinfo=timezone(timedelta(hours=2))),
    datetime(2027, 1, 1, 0, 0, 0),
    datetime(5, 1, 2, 3, 4, 5),
    datetime(2024, 2, 29, 23, 59, 59, 999999, tzinfo=timezone(timedelta(hours=-3, minutes=-30))),
    datetime(2026, 12, 28, 12, 30, 0, tzinfo=timezone.utc),
]


def section_strftime():
    print("== strftime")
    for f in lines("data/strftime.txt"):
        print(f"{f!r}")
        for d in SAMPLES:
            try:
                out = repr(d.strftime(f))
            except Exception as e:
                out = err(e)
            print(f"  {d.isoformat()}: {out}")


def section_iso():
    print("== fromisoformat")
    for l in lines("data/iso.txt"):
        if l.startswith("date "):
            cls, s = date, l[5:]
        elif l.startswith("time "):
            cls, s = time, l[5:]
        else:
            cls, s = datetime, l
        try:
            out = show(cls.fromisoformat(s))
        except Exception as e:
            out = err(e)
        print(f"{cls.__name__}.fromisoformat({s!r}): {out}")


def delta(fields):
    kw = {}
    for f in fields:
        k, _, v = f.partition("=")
        kw[k] = int(v)
    return timedelta(**kw)


def show_td(td):
    return f"{td} = {td!r}"


def split_fields(words):
    # the timedelta fields, then the rest
    i = 0
    while i < len(words) and "=" in words[i]:
        i += 1
    return words[:i], words[i:]


def section_deltas():
    print("== timedelta")
    for l in lines("data/deltas.txt"):
        cmd, *words = l.split(" ")
        try:
            if cmd == "td":
                out = show_td(delta(words))
            elif cmd == "add":
                d = datetime.fromisoformat(words[0])
                out = show(d + delta(words[1:]))
            elif cmd == "sub":
                a = datetime.fromisoformat(words[0])
                b = datetime.fromisoformat(words[1])
                out = show_td(a - b)
            elif cmd == "mul":
                f, rest = split_fields(words)
                out = show_td(delta(f) * int(rest[0]))
            elif cmd in ("floordiv", "mod"):
                k = words.index("/")
                a = delta(words[:k])
                b = delta(words[k + 1:])
                out = repr(a // b) if cmd == "floordiv" else show_td(a % b)
            elif cmd == "neg":
                out = show_td(-delta(words))
            else:
                out = show_td(abs(delta(words)))
        except Exception as e:
            out = err(e)
        print(f"{l}: {out}")


def find_stamp(line, rule):
    if rule == "bracket":
        a = line.find("[")
        b = line.find("]", a + 1)
        return line[a + 1:b] if a >= 0 and b >= 0 else None
    kind, _, arg = rule.partition(":")
    words = line.split(" ")
    if kind == "field":
        n = int(arg)
        return words[n - 1] if len(words) >= n else None
    if kind == "fields":
        n = int(arg)
        return " ".join(words[:n]) if len(words) >= n else None
    i = line.find(arg)
    return line[:i] if i >= 0 else None


def parse_stamp(s, fmt):
    if fmt == "iso":
        return datetime.fromisoformat(s)
    if fmt == "epoch":
        whole, _, frac = s.partition(".")
        if not whole.isdigit() or (frac and not frac.isdigit()) or len(frac) > 6:
            raise ValueError(f"not an epoch time: {s!r}")
        us = int(frac.ljust(6, "0")) if frac else 0
        return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=int(whole), microseconds=us)
    return datetime.strptime(s, fmt)


def offset(s):
    sign = -1 if s[0] == "-" else 1
    return timezone(sign * timedelta(hours=int(s[1:3]), minutes=int(s[4:6])))


def section_normalize():
    print("== normalize")
    events = []
    for k, l in enumerate(lines("data/sources.txt")):
        name, log, rule, fmt, off = l.split(" | ")
        good = bad = 0
        notes = []
        last = None
        for n, line in enumerate(lines(f"data/logs/{log}"), 1):
            stamp = find_stamp(line, rule)
            try:
                if stamp is None:
                    raise ValueError("no timestamp found")
                dt = parse_stamp(stamp, fmt)
            except ValueError as e:
                bad += 1
                notes.append(f"  line {n}: {err(e)}")
                continue
            assumed = dt.tzinfo is None
            if assumed:
                dt = dt.replace(tzinfo=offset(off))
            utc = dt.astimezone(timezone.utc)
            if last is not None and utc < last:
                notes.append(f"  line {n}: {utc - last} out of order")
            last = utc
            good += 1
            cut = f"[{stamp}]" if rule == "bracket" else stamp
            rest = " ".join(line.replace(cut, "", 1).split()).strip(" ,|")
            events.append((utc, k, n, name, dt, assumed, rest))
        print(f"{name}: {good + bad} lines, {good} parsed, {bad} failed")
        for x in notes:
            print(x)
    events.sort(key=lambda e: (e[0], e[1], e[2]))
    print("-- timeline (UTC)")
    prev = None
    for utc, _, n, name, dt, assumed, rest in events:
        gap = "-" if prev is None else str(utc - prev)
        prev = utc
        mark = "*" if assumed else " "
        print(f"{utc.isoformat(timespec='milliseconds')} {gap:>15} {name:8} {dt.isoformat(sep=' ', timespec='microseconds')}{mark} {rest}")
    print("-- per minute")
    counts = {}
    for e in events:
        key = e[0].replace(second=0, microsecond=0)
        counts[key] = counts.get(key, 0) + 1
    for key in sorted(counts):
        print(f"{key.strftime('%m-%d %H:%M')} {'#' * counts[key]} {counts[key]}")
    first, last = events[0][0], events[-1][0]
    print(f"span {first.isoformat()} to {last.isoformat()}: {last - first}, {len(events)} events")


section_strptime()
section_strftime()
section_iso()
section_deltas()
section_normalize()
