# Runs data/jobs.jsonl through the real humanize 4.16.0 (CPython 3.13);
# its output is expected.out.
import datetime as dt
import json
import os

import humanize


def conv(v):
    if isinstance(v, list):
        return [conv(x) for x in v]
    if isinstance(v, dict):
        if "td" in v:
            d, s, us = v["td"]
            return dt.timedelta(days=d, seconds=s, microseconds=us)
        if "dt" in v:
            return dt.datetime(*v["dt"])
        if "date" in v:
            return dt.date(*v["date"])
        if "big" in v:
            return int(v["big"])
        if "float" in v:
            return float(v["float"])
        if "fn" in v:
            return getattr(humanize, v["fn"])
    return v


for line in open("data/jobs.jsonl", encoding="utf-8"):
    line = line.rstrip("\n")
    print("== " + line)
    j = json.loads(line)
    kind = j["kind"]
    try:
        if kind == "activate":
            humanize.activate(j["locale"], path="data/locale")
            print("  ok")
        elif kind == "deactivate":
            humanize.deactivate()
            print("  ok")
        elif kind == "remove":
            os.remove(j["path"])
            print("  ok")
        else:
            fn = getattr(humanize, j["fn"])
            r = fn(*conv(j["args"]), **{k: conv(v) for k, v in j["kw"].items()})
            print("  " + repr(r))
    except Exception as e:
        print("  %s: %s" % (type(e).__name__, e))
