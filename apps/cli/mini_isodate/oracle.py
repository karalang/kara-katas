# Runs data/jobs.tsv through isodate 0.7.2 (the files in isodate/,
# unchanged) and prints what each operation returns; the two report jobs
# read data/subscriptions.tsv and data/incidents.tsv. Run mk.py first.
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import isodate  # noqa: E402
from isodate.duration import Duration  # noqa: E402
from isodate.tzinfo import Utc  # noqa: E402


def unesc(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append({"t": "\t", "n": "\n", "\\": "\\"}[s[i + 1]])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def tzdesc(tz):
    if tz is None:
        return "naive"
    if isinstance(tz, Utc):
        return "UTC"
    off = tz.utcoffset(None)
    return f"{tz!r} {off.days * 86400 + off.seconds}"


def show(v):
    if isinstance(v, datetime.datetime):
        return (f"datetime {v.year:04d}-{v.month:02d}-{v.day:02d} {v.hour:02d}:{v.minute:02d}:"
                f"{v.second:02d}.{v.microsecond:06d} {tzdesc(v.tzinfo)}")
    if isinstance(v, datetime.date):
        return f"date {v.year:04d}-{v.month:02d}-{v.day:02d}"
    if isinstance(v, datetime.time):
        return (f"time {v.hour:02d}:{v.minute:02d}:{v.second:02d}.{v.microsecond:06d} "
                f"{tzdesc(v.tzinfo)}")
    if isinstance(v, (Duration, datetime.timedelta)):
        return f"{v!r} = {v}"
    return repr(v)


def value(a):
    kind, text = a.split(":", 1)
    if kind == "d":
        return isodate.parse_date(text)
    if kind == "t":
        return isodate.parse_time(text)
    if kind == "dt":
        return isodate.parse_datetime(text)
    if kind == "p":
        return isodate.parse_duration(text)
    return isodate.parse_duration(text, False)


def err(e):
    return f"error: {type(e).__name__}: {e}"


def fmt_point(x):
    if isinstance(x, datetime.datetime):
        return isodate.datetime_isoformat(x)
    return isodate.date_isoformat(x)


def subscriptions(path):
    with open(path, encoding="utf-8") as fh:
        rows = [ln.rstrip("\n").split("\t") for ln in fh if not ln.startswith("#")]
    for sid, starts, period_text, count, grace_text, plan in rows:
        print(f"   {sid}: {plan}")
        try:
            start = isodate.parse_datetime(starts) if "T" in starts else isodate.parse_date(starts)
            period = isodate.parse_duration(period_text)
            grace = isodate.parse_duration(grace_text)
            print(f"     starts {fmt_point(start)}, every {isodate.duration_isoformat(period)}"
                  f" ({period}), grace {isodate.duration_isoformat(grace)}")
            cur = start
            for k in range(1, int(count) + 1):
                cur = cur + period
                line = f"     renewal {k}: {fmt_point(cur)}, due by {fmt_point(cur + grace)}"
                mult = start + period * k
                if mult != cur:
                    line += f" (period x {k} from the start gives {fmt_point(mult)})"
                print(line)
            covered = cur - start
            print(f"     covered {isodate.duration_isoformat(covered)} ({covered})")
        except Exception as e:
            print("     " + err(e))


def incidents(path):
    with open(path, encoding="utf-8") as fh:
        rows = [ln.rstrip("\n").split("\t") for ln in fh if not ln.startswith("#")]
    totals = {}
    for svc, started, resolved, budget_text, note in rows:
        try:
            a = isodate.parse_datetime(started)
            b = isodate.parse_datetime(resolved)
            budget = isodate.parse_duration(budget_text)
            dur = b - a
        except Exception as e:
            print(f"   {svc}: {note}: {err(e)}")
            continue
        if dur <= budget:
            verdict = "within budget"
        else:
            verdict = "over by " + isodate.duration_isoformat(dur - budget)
        print(f"   {svc}: {note}: down {isodate.duration_isoformat(dur)} ({dur}),"
              f" budget {isodate.duration_isoformat(budget)}, {verdict}")
        t = totals.setdefault(svc, [0, datetime.timedelta(0), 0, None])
        t[0] += 1
        t[1] += dur
        t[2] += 0 if dur <= budget else 1
        if t[3] is None or dur > t[3]:
            t[3] = dur
    for svc in sorted(totals):
        n, total, over, longest = totals[svc]
        print(f"   {svc}: {n} incidents, {isodate.duration_isoformat(total)} down,"
              f" {over} over budget, longest {isodate.duration_isoformat(longest)}")


def run(f):
    op, args = f[0], f[1:]
    print("-- " + op + "".join(" " + repr(a) for a in args))
    try:
        if op == "date":
            yd = int(args[1]) if len(args) > 1 else 4
            ex = len(args) > 2 and args[2] == "1"
            dm = int(args[3]) if len(args) > 3 else 1
            dd = int(args[4]) if len(args) > 4 else 1
            r = isodate.parse_date(args[0], yd, ex, dm, dd)
        elif op == "date_fmt":
            yd = int(args[2]) if len(args) > 2 else 4
            r = isodate.date_isoformat(isodate.parse_date(args[0]), args[1], yd)
        elif op == "time":
            r = isodate.parse_time(args[0])
        elif op == "time_fmt":
            r = isodate.time_isoformat(isodate.parse_time(args[0]), args[1])
        elif op == "tz":
            r = isodate.parse_tzinfo(args[0])
            r = tzdesc(r)
        elif op == "datetime":
            r = isodate.parse_datetime(args[0])
        elif op == "datetime_fmt":
            r = isodate.datetime_isoformat(isodate.parse_datetime(args[0]), args[1])
        elif op == "duration":
            r = isodate.parse_duration(args[0], len(args) == 1)
        elif op == "duration_fmt":
            r = isodate.duration_isoformat(isodate.parse_duration(args[0], len(args) == 2), args[1])
        elif op == "add":
            r = value(args[0]) + value(args[1])
        elif op == "sub":
            r = value(args[0]) - value(args[1])
        elif op == "mul":
            r = value(args[0]) * int(args[1])
        elif op == "neg":
            r = -value(args[0])
        elif op == "eq":
            a, b = value(args[0]), value(args[1])
            r = f"{a == b} {a != b}"
        elif op == "totd":
            d, x = value(args[0]), value(args[2])
            if args[1] == "start":
                r = d.totimedelta(start=x)
            elif args[1] == "end":
                r = d.totimedelta(end=x)
            elif args[1] == "both":
                r = d.totimedelta(start=x, end=x)
            else:
                r = d.totimedelta()
        elif op == "subscriptions":
            subscriptions(os.path.join("data", args[0]))
            return
        elif op == "incidents":
            incidents(os.path.join("data", args[0]))
            return
        else:
            raise SystemExit("unknown op " + op)
    except Exception as e:
        print("   " + err(e))
        return
    print("   " + (r if isinstance(r, str) else show(r)))


with open("data/jobs.tsv", encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if line.startswith("== "):
            print(line)
            continue
        run([unesc(x) for x in line.split("\t")])
