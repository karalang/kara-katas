# Runs data/jobs.jsonl through croniter 6.2.4 (the package here, with the
# parts of python-dateutil and six it imports) and prints what
# mini_croniter prints. Run mk.py first.
import datetime
import json
import os
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from croniter import croniter, croniter_range  # noqa: E402

TZ = {}


def tz_of(spec):
    if spec is None:
        return None
    if spec not in TZ:
        if spec == "UTC":
            TZ[spec] = datetime.timezone.utc
        elif spec[0] in "+-":
            sign = -1 if spec[0] == "-" else 1
            h, m = spec[1:].split(":")
            TZ[spec] = datetime.timezone(sign * datetime.timedelta(hours=int(h), minutes=int(m)))
        else:
            with open("data/zones/" + spec.replace("/", "_"), "rb") as f:
                TZ[spec] = ZoneInfo.from_file(f, key=spec)
    return TZ[spec]


def time_of(t):
    if isinstance(t, float):
        return t
    y, mo, d, h, mi, s, us = t["dt"]
    return datetime.datetime(y, mo, d, h, mi, s, us, tzinfo=tz_of(t["tz"]), fold=t.get("fold", 0))


def show(v):
    if isinstance(v, datetime.datetime):
        return str(v)
    return repr(v)


def err(e):
    return f"{type(e).__name__}: {e}"


def opts(o, names, as_bytes=False):
    kw = {}
    for k in names:
        if k in o:
            kw[k] = o[k]
    # croniter.expand takes the hash_id as bytes; the constructor and
    # is_valid encode a str themselves.
    if as_bytes and "hash_id" in kw and not o.get("hash_str"):
        kw["hash_id"] = kw["hash_id"].encode()
    if "max_years" in o:
        kw["max_years_between_matches"] = o["max_years"]
    if "precision" in o:
        kw["precision_in_seconds"] = o["precision"]
    return kw


ITER_OPTS = ["day_or", "hash_id", "second_at_beginning", "implement_cron_bug",
             "expand_from_start_time"]
EXPAND_OPTS = ["hash_id", "second_at_beginning", "strict", "strict_year"]


def nth_str(nth):
    parts = []
    for k in sorted(nth):
        vals = ", ".join(repr(x) for x in sorted(nth[k], key=str))
        parts.append(f"{k}: [{vals}]")
    return "{" + ", ".join(parts) + "}"


def ret_of(o):
    return datetime.datetime if o.get("ret", "dt") == "dt" else float


def run_op(i, o):
    n = o["op"]
    tag = f"{i}. {n} {o['expr']!r}"
    if n == "iter" or n == "all":
        start = time_of(o["start"])
        print(f"{tag} from {show(start)}")
        rt = ret_of(o)
        try:
            c = croniter(o["expr"], start, ret_type=rt, **opts(o, ITER_OPTS))
        except Exception as e:
            print(f"  {err(e)}")
            return
        if n == "all":
            g = c.all_next() if o["dir"] == "next" else c.all_prev()
            k = 0
            try:
                for v in g:
                    print(f"  {show(v)}")
                    k += 1
                    if k == o["n"]:
                        break
                else:
                    print("  (end)")
            except Exception as e:
                print(f"  {err(e)}")
            return
        for ch in o["seq"]:
            try:
                if ch == "n":
                    v = c.get_next()
                elif ch == "p":
                    v = c.get_prev()
                elif ch == "N":
                    v = c.get_next(update_current=False)
                elif ch == "P":
                    v = c.get_prev(update_current=False)
                else:
                    v = c.get_current(rt)
                print(f"  {ch} {show(v)}")
            except Exception as e:
                print(f"  {ch} {err(e)}")
    elif n == "expand":
        try:
            ex, nth = croniter.expand(o["expr"], **opts(o, EXPAND_OPTS, True))
            print(f"{tag} -> {ex!r} {nth_str(nth)}")
        except Exception as e:
            print(f"{tag} -> {err(e)}")
    elif n == "valid":
        print(f"{tag} -> {croniter.is_valid(o['expr'], **opts(o, EXPAND_OPTS))}")
    elif n == "match":
        t = time_of(o["t"])
        try:
            r = croniter.match(o["expr"], t, **opts(o, ["day_or", "second_at_beginning"]))
        except Exception as e:
            r = err(e)
        print(f"{tag} at {show(t)} -> {r}")
    elif n == "match_range":
        a, b = time_of(o["from"]), time_of(o["to"])
        try:
            r = croniter.match_range(o["expr"], a, b, **opts(o, ["day_or", "second_at_beginning"]))
        except Exception as e:
            r = err(e)
        print(f"{tag} from {show(a)} to {show(b)} -> {r}")
    elif n == "range":
        a, b = time_of(o["start"]), time_of(o["stop"])
        print(f"{tag} from {show(a)} to {show(b)}")
        kw = opts(o, ["day_or", "exclude_ends", "second_at_beginning", "expand_from_start_time"])
        if "ret" in o:
            kw["ret_type"] = ret_of(o)
        try:
            for v in croniter_range(a, b, o["expr"], **kw):
                print(f"  {show(v)}")
        except Exception as e:
            print(f"  {err(e)}")
    else:
        raise SystemExit(f"unknown op {n}")


with open("data/jobs.jsonl") as f:
    for line in f:
        j = json.loads(line)
        print(f"== {j['name']}")
        for i, o in enumerate(j["ops"]):
            run_op(i + 1, o)
