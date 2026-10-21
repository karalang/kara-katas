# Runs jobs.tsv through ua_parser itself (the copy in ua_parser/,
# unchanged) and prints what mini_uaparser prints.
import os
import re
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

from ua_parser import user_agent_parser as uap  # noqa: E402

with open(os.path.join(HERE, "data", "agents.txt"), encoding="utf-8") as f:
    UAS = f.read().split("\n")[:-1]

LOG_RE = re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d{3}) (\d+|-) "([^"]*)" "([^"]*)"$')

fill_count = [0]


def opt(s):
    return None if s == "~" else s


def bits(spec):
    out = {}
    for part in spec.split("|"):
        k, _, v = part.partition("=")
        out[k] = v
    return out


def fail(e):
    return "! %s: %s" % (type(e).__name__, e)


def table(title, counts):
    print("  %s:" % title)
    for name, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print("    %5d  %s" % (n, name))


def bump(d, k, n=1):
    d[k] = d.get(k, 0) + n


def report():
    with open(os.path.join(HERE, "data", "access.log"), encoding="utf-8") as f:
        lines = f.read().split("\n")[:-1]
    browsers, oses, devices, brands = {}, {}, {}, {}
    errors, bot_paths = {}, {}
    bad = 0
    total = 0
    bot_requests, bot_bytes, human_bytes = 0, 0, 0
    agents = []
    for line in lines:
        m = LOG_RE.match(line)
        if not m:
            bad += 1
            continue
        total += 1
        ua = m.group(8)
        r = uap.Parse(ua)
        if ua not in agents:
            agents.append(ua)
        u, o, d = r["user_agent"], r["os"], r["device"]
        bump(browsers, uap.PrettyUserAgent(u["family"], u["major"], u["minor"]))
        bump(oses, uap.PrettyOS(o["family"], o["major"]))
        bump(devices, d["family"])
        bump(brands, d["brand"] or "(none)")
        size = 0 if m.group(6) == "-" else int(m.group(6))
        if d["family"] == "Spider":
            bot_requests += 1
            bot_bytes += size
            bump(bot_paths, m.group(4))
        else:
            human_bytes += size
        status = int(m.group(5))
        if status >= 400:
            bump(errors, "%s %d" % (u["family"], status))
    print("  %d requests, %d lines not in the log format, %d user agents" % (total, bad, len(agents)))
    table("browsers", browsers)
    table("operating systems", oses)
    table("devices", devices)
    table("brands", brands)
    print("  bots: %d requests, %d bytes (others %d bytes)" % (bot_requests, bot_bytes, human_bytes))
    table("bot paths", bot_paths)
    table("errors", errors)


def run(job):
    kind = job[0]
    if kind == "parse":
        print(repr(uap.Parse(UAS[int(job[1])])))
    elif kind == "report":
        report()
    elif kind == "ua":
        print(repr(uap.ParseUserAgent(UAS[int(job[1])])))
    elif kind == "os":
        print(repr(uap.ParseOS(UAS[int(job[1])])))
    elif kind == "device":
        print(repr(uap.ParseDevice(UAS[int(job[1])])))
    elif kind == "ua_js":
        print(repr(uap.ParseUserAgent(UAS[int(job[1])], **bits(job[2]))))
    elif kind == "parse_js":
        print(repr(uap.Parse(UAS[int(job[1])], **bits(job[2]))))
    elif kind == "os_js":
        print(repr(uap.ParseOS(UAS[int(job[1])], **bits(job[2]))))
    elif kind == "cache":
        print(len(uap._PARSE_CACHE))
    elif kind == "clear":
        uap._PARSE_CACHE.clear()
    elif kind == "pretty_ua":
        print(repr(uap.PrettyUserAgent(*[opt(a) for a in job[1:]])))
    elif kind == "pretty":
        print(repr(uap.Pretty(*[opt(a) for a in job[1:]])))
    elif kind == "pretty_os":
        print(repr(uap.PrettyOS(*[opt(a) for a in job[1:]])))
    elif kind == "pretty_parse":
        r = uap.Parse(UAS[int(job[1])])
        u, o = r["user_agent"], r["os"]
        print(repr(uap.PrettyUserAgent(u["family"], u["major"], u["minor"], u["patch"])))
        print(repr(uap.PrettyOS(o["family"], o["major"], o["minor"], o["patch"], o["patch_minor"])))
    elif kind == "jsov":
        print(repr(uap.ParseWithJSOverrides(UAS[int(job[1])], *[opt(a) for a in job[2:]])))
    elif kind == "filters":
        print(repr(uap.GetFilters(*[opt(a) for a in job[1:]])))
    elif kind == "spans":
        parsers = {"ua": uap.USER_AGENT_PARSERS, "os": uap.OS_PARSERS,
                   "device": uap.DEVICE_PARSERS}[job[1]]
        text = UAS[0] if job[3] == "~" else job[3]
        print(repr(parsers[int(job[2])].MatchSpans(text)))
    elif kind == "fill":
        for _ in range(int(job[1])):
            fill_count[0] += 1
            uap.ParseUserAgent("", js_user_agent_family="F%d" % fill_count[0])


with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as f:
    jobs = [line.split("\t") for line in f.read().split("\n")[:-1]]
for job in jobs:
    print("-- " + " ".join(repr(a) if a == "" or " " in a else a for a in job))
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter("always")
        try:
            run(job)
        except Exception as e:
            print(fail(e))
    shown = {}
    for w in seen:
        bump(shown, "%s: %s" % (w.category.__name__, w.message))
    for msg, n in shown.items():
        print("  warning x%d %s" % (n, msg))
