# Runs data/jobs.jsonl through the real dateutil 2.9.0 (pip install
# python-dateutil==2.9.0.post0) and prints what mini_dateparse must print.
# The clock is pinned: the local zone is UTC and "this year" is 2026, the
# two things dateutil reads from the machine.
import os, time
os.environ["TZ"] = "UTC"
time.tzset()
import json, sys, warnings, datetime
import dateutil
from dateutil import parser as dparser
from dateutil.parser import isoparser
from dateutil.relativedelta import relativedelta, weekdays

assert dateutil.__version__ == "2.9.0.post0"
info = dparser._parser.DEFAULTPARSER.info
info._year = 2026
info._century = 2000

DEF = datetime.datetime(2003, 9, 25)
LOGTZ = {"BRST": -7200, "EST": -18000, "IST": 19800}
TODAY = datetime.datetime(2026, 10, 18)


def err(e):
    return "%s: %s" % (type(e).__name__, e)


def parse(s, **kw):
    kw.setdefault("default", DEF)
    return dparser.parse(s, **kw)


def run_parse(j):
    kw = {k: v for k, v in j.items() if k not in ("kind", "s")}
    if "default" in kw:
        kw["default"] = isoparser().isoparse(kw["default"])
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            print(repr(parse(j["s"], **kw)))
        except Exception as e:
            print(err(e))
    for x in w:
        print("warning: " + str(x.message))


def run_iso(j):
    try:
        p = isoparser(j["sep"]) if "sep" in j else isoparser()
        print(repr(p.isoparse(j["s"])))
    except Exception as e:
        print(err(e))


def make_rd(kw):
    kw = dict(kw)
    if "weekday" in kw:
        d, n = kw["weekday"]
        kw["weekday"] = weekdays[d] if n is None else weekdays[d](n)
    return relativedelta(**kw)


def run_diff(j):
    try:
        print(repr(relativedelta(parse(j["a"]), parse(j["b"]))))
    except Exception as e:
        print(err(e))


def run_shift(j):
    try:
        rd = make_rd(j["rd"])
        print(repr(rd))
        dt = parse(j["dt"])
        print(repr(dt - rd if j.get("sub") else dt + rd))
    except Exception as e:
        print(err(e))


def utc_naive(dt):
    if dt.tzinfo is None:
        return dt
    return dt.replace(tzinfo=None) - dt.utcoffset()


def lines_of(name):
    return open("data/files/" + name, encoding="utf-8").read().split("\n")[:-1]


def run_logs(name):
    good = []
    for n, line in enumerate(lines_of(name), 1):
        ts, src, msg = line.split(" | ")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                dt = parse(ts, tzinfos=LOGTZ)
            except Exception as e:
                print("line %d skipped: %s" % (n, err(e)))
                continue
        for x in w:
            print("line %d: %s" % (n, x.message))
        good.append((utc_naive(dt), n, src, msg))
    good.sort(key=lambda g: (g[0], g[1]))
    for t, n, src, msg in good:
        print("%sZ  %-8s %s (line %d)" % (t.isoformat(), src, msg, n))


def run_mail(name):
    for line in lines_of(name):
        v = line[len("Date: "):]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                dt = parse(v)
        except Exception as e:
            print(err(e))
            continue
        off = dt.utcoffset()
        print("%s %s offset=%s utc=%s" % (dt.isoformat(), dt.strftime("%a"),
              "none" if off is None else int(off.total_seconds()),
              utc_naive(dt).isoformat()))


def run_ages(name):
    for line in lines_of(name)[1:]:
        who, born = line.split(",")
        try:
            b = parse(born)
            rd = relativedelta(TODAY, b)
            nxt = b + relativedelta(years=rd.years + 1)
            print("%s: %d years %d months %d days, next %s, %r" % (
                who, rd.years, rd.months, rd.days, nxt.date().isoformat(), rd))
        except Exception as e:
            print("%s: %s" % (who, err(e)))


def run_renew(name):
    for line in lines_of(name)[1:]:
        who, start, plan = line.split(",")
        s = parse(start)
        if plan == "monthly":
            steps = [relativedelta(months=k) for k in range(1, 7)]
        elif plan == "yearly":
            steps = [relativedelta(years=k) for k in range(1, 4)]
        elif plan == "quarterly":
            steps = [relativedelta(months=3 * k) for k in range(1, 5)]
        else:
            steps = [relativedelta(weeks=k) for k in range(1, 5)]
        print("%s (%s from %s): %s" % (who, plan, s.isoformat(),
              ", ".join((s + r).isoformat() for r in steps)))


def run_notes(name):
    for line in lines_of(name):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                print(repr(parse(line, fuzzy_with_tokens=True)))
        except Exception as e:
            print(err(e))


for raw in open("data/jobs.jsonl", encoding="utf-8").read().split("\n"):
    if not raw:
        continue
    j = json.loads(raw)
    print("== " + raw)
    k = j["kind"]
    if k == "parse":
        run_parse(j)
    elif k == "iso":
        run_iso(j)
    elif k == "diff":
        run_diff(j)
    elif k == "shift":
        run_shift(j)
    else:
        {"logs": run_logs, "mail": run_mail, "ages": run_ages,
         "renew": run_renew, "notes": run_notes}[j["mode"]](j["name"])
