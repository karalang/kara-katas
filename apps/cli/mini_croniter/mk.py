# Writes data/: five TZif files copied from the system's tzdata, and
# data/jobs.jsonl, the schedules to work through.
#
# A time is a float timestamp, or {"dt": [y, mo, d, h, mi, s, us], "tz":
# ..., "fold": ...} where tz is null (naive), "UTC", a fixed offset such as
# "+05:30", or the name of a zone in data/zones.
import json
import os
import random
import shutil

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/zones")

ZONES = ["America/New_York", "Europe/London", "Australia/Lord_Howe",
         "Asia/Kolkata", "Pacific/Apia"]
for key in ZONES:
    with open("/usr/share/zoneinfo/" + key, "rb") as f:
        data = f.read()
    with open("data/zones/" + key.replace("/", "_"), "wb") as f:
        f.write(data)


def dt(y, mo, d, h=0, mi=0, s=0, us=0, tz=None, fold=0):
    t = {"dt": [y, mo, d, h, mi, s, us], "tz": tz}
    if fold:
        t["fold"] = fold
    return t


NY = "America/New_York"
LON = "Europe/London"
LH = "Australia/Lord_Howe"
KOL = "Asia/Kolkata"
APIA = "Pacific/Apia"

jobs = []


def job(name, ops):
    jobs.append({"name": name, "ops": ops})


def it(expr, start, seq, ret="dt", **kw):
    o = {"op": "iter", "expr": expr, "start": start, "seq": seq, "ret": ret}
    o.update(kw)
    return o


def allx(expr, start, n, d="next", ret="dt", **kw):
    o = {"op": "all", "expr": expr, "start": start, "n": n, "dir": d, "ret": ret}
    o.update(kw)
    return o


def expand(expr, **kw):
    o = {"op": "expand", "expr": expr}
    o.update(kw)
    return o


def valid(expr, **kw):
    o = {"op": "valid", "expr": expr}
    o.update(kw)
    return o


def match(expr, t, **kw):
    o = {"op": "match", "expr": expr, "t": t}
    o.update(kw)
    return o


def mrange(expr, a, b, **kw):
    o = {"op": "match_range", "expr": expr, "from": a, "to": b}
    o.update(kw)
    return o


def rng(expr, a, b, **kw):
    o = {"op": "range", "expr": expr, "start": a, "stop": b}
    o.update(kw)
    return o


T0 = dt(2024, 1, 15, 10, 7, 30)

job("basics", [
    it("*/15 * * * *", T0, "nnnnpp"),
    it("0 9 * * mon-fri", T0, "nnnnnnp"),
    it("30 2 * * *", 1705313250.0, "nnnc", ret="float"),
    it("0 0 1 * *", T0, "nnnpppp"),
    it("0 12 * * sun", dt(2024, 2, 27, 12), "nnppp"),
    it("5 4 * * *", T0, "NNnc"),
    it("0 */6 * * *", T0, "nnnnnPpc", ret="float"),
    it("15,45 8-10 * * *", T0, "nnnnnnn"),
    it("59 23 31 12 *", T0, "nnp"),
    it("0 0 29 2 *", T0, "nnnpp"),
    it("* * * * *", dt(2024, 12, 31, 23, 59, 30), "nnp"),
])

job("ranges and steps", [
    expand("*/7 * * * *"),
    expand("10-50/15 0-23/5 1-31/10 1-12/4 0-6/2"),
    expand("50-10/7 * * * *"),
    expand("22-2 * * * *"),
    expand("22-2/3 * * * *"),
    expand("5-5 * * * *"),
    expand("5/20 * * * *"),
    expand("0 0 * jan-mar,oct sun-tue"),
    expand("0 0 * dec-feb fri-mon"),
    expand("0 0 * * 7"),
    expand("0 0 * * 5-7"),
    expand("0 0 * * 1,3,5,7,0"),
    expand("0 0 1-l/7 * *"),
    expand("0 0 l * *"),
    expand("0 0 1,l,15 * *"),
    expand("0 0 * * *,1"),
    expand("0 0 * * 0-6"),
    expand("0 0 1-31 * *"),
    expand("0 0 1-31 * 1"),
    expand("0 0 * 1-12 *"),
    expand("0-59 0-23 * * *"),
    expand("0 0 * * ?"),
    expand("0 0 ? * mon"),
    expand("0 0 * * 6-6"),
    it("50-10/7 * * * *", T0, "nnnnnnnp"),
    it("0 22-2 * * *", T0, "nnnnnnp"),
])

job("the last day and nearest weekday", [
    it("0 0 l * *", T0, "nnnnnpppp"),
    it("0 18 l * *", dt(2024, 2, 1), "nnnp"),
    it("0 0 l 2 *", T0, "nnnnp"),
    it("0 0 20-l/5 * *", T0, "nnnnnn"),
    it("0 9 15w * *", T0, "nnnnnnpppp"),
    it("0 9 1w * *", dt(2024, 5, 20), "nnnnnnppp"),
    it("0 9 w31 * *", dt(2024, 1, 1), "nnnnnnnnppp"),
    it("0 9 30w * *", dt(2024, 1, 1), "nnnnnnnp"),
    expand("0 0 15w * *"),
    expand("0 0 w3 * *"),
    expand("0 0 1,15w * *"),
    expand("0 0 15w,1 * *"),
    expand("0 0 0w * *"),
    expand("0 0 32w * *"),
    expand("0 0 1-5w * *"),
    expand("0 0 lw * *"),
])

job("nth weekdays", [
    it("0 10 * * 2#2", T0, "nnnnpp"),
    it("0 10 * * fri#5", T0, "nnnnpp"),
    it("0 10 * * l5", T0, "nnnnpppp"),
    it("0 10 * * l0", dt(2024, 3, 31, 10), "nnpp"),
    it("0 10 * * mon#1,mon#3", T0, "nnnnp"),
    it("0 10 * * mon-wed#2", T0, "nnnnnp"),
    it("0 10 * * 1#1,l1", T0, "nnnnp"),
    it("30 7 1-7 * mon", T0, "nnnp"),
    it("30 7 1-7 * mon", T0, "nnnp", day_or=False),
    it("0 10 13 * fri", T0, "nnnn", day_or=False),
    it("0 10 13 * fri", T0, "nnnn"),
    expand("0 0 * * 2#2"),
    expand("0 0 * * mon#1,wed#3,l5"),
    expand("0 0 * * 1#6"),
    expand("0 0 * * 1#0"),
    expand("0 0 * * 1#2,3"),
    expand("0 0 * * 0-6,1#2"),
    expand("0 0 * * monday#2"),
    expand("0 0 * * jan#2"),
    expand("0 0 * * 9#2"),
    expand("0 0 * * l8"),
    expand("0 0 * * *#2"),
    expand("0 0 * * l"),
    expand("0 0 * * 5l"),
    expand("0 0 * * sun-x#1"),
])

job("day_or and the cron bug", [
    it("0 0 1,15 * 1", T0, "nnnnnnp"),
    it("0 0 1,15 * 1", T0, "nnnnp", day_or=False),
    it("0 0 */2 * 1", T0, "nnnnn"),
    it("0 0 */2 * 1", T0, "nnnnn", implement_cron_bug=True),
    it("0 0 1 * */3", T0, "nnnn", implement_cron_bug=True),
    it("0 0 1 * 0-3", T0, "nnnn", implement_cron_bug=True),
    it("0 0 1-31 * 1", T0, "nnn"),
    it("0 0 * * 0-6", T0, "nnn"),
    it("0 12 l * fri", T0, "nnnnnn"),
    it("0 12 l * fri", T0, "nnnn", day_or=False),
    it("0 9 15w * 6", T0, "nnnnn"),
])

job("seconds and years", [
    it("* * * * * */20", dt(2024, 1, 15, 10, 7, 30, 500000), "nnnnpp"),
    it("*/20 * * * * *", dt(2024, 1, 15, 10, 7, 30), "nnnpp", second_at_beginning=True),
    it("0 0 * * * 30", T0, "nnp"),
    it("0 0 1 1 * 0 2030", T0, "nnp"),
    it("0 0 1 1 * 0 2025-2027", T0, "nnnnppp"),
    it("0 0 29 2 * 0 *", T0, "nnn"),
    it("0 0 1 1 * 0 2099", T0, "n"),
    it("0 0 1 1 * 0 1999", T0, "np"),
    it("0 0 31 * * 0 2025", dt(2025, 11, 1), "nnp"),
    it("* * * * * * 2026", dt(2026, 12, 31, 23, 59, 58), "nnnpp", ret="float"),
    expand("0 0 * * * 0"),
    expand("0 0 0 0 * 0"),
    expand("0 0 0 * * 0"),
    expand("0 0 0 * *"),
    expand("0 0 1 1 7 0 *"),
    expand("0 0 0 1 * 0 2024"),
    expand("0 0 1 1 * 0 1969"),
    expand("0 0 1 1 * 0 2100"),
    expand("0 0 1 1 * 0 2000-2099/25"),
    expand("0 0 1 1 * 0 1970-2099"),
    expand("0 0 1 1 * */15"),
    expand("5 0 0 1 1 *", second_at_beginning=True),
    expand("0 0 0 * * 0 0", second_at_beginning=True),
])

job("errors", [
    valid("* * * * *"),
    valid("* * * *"),
    valid("* * * * * * * *"),
    valid(""),
    valid("@daily"),
    valid("@DAILY"),
    valid("@reboot"),
    valid("60 * * * *"),
    valid("* 24 * * *"),
    valid("* * 32 * *"),
    valid("* * 0 * *"),
    valid("* * * 13 *"),
    valid("* * * 0 *"),
    valid("-5 * * * *"),
    valid("-5/2 * * * *"),
    valid("*/0 * * * *"),
    valid("*/00 * * * *"),
    valid("1-5/x * * * *"),
    valid("a/b/c * * * *"),
    valid("5-70 * * * *"),
    valid("0-5 * 0-5 * *"),
    valid("* * * foo *"),
    valid("* * * * fri-foo"),
    valid("* * * * l"),
    valid("* * ? * *"),
    valid("? * * * *"),
    valid("* * ?? * *"),
    valid("* * 1? * *"),
    valid("1,,2 * * * *"),
    valid("1,2, * * * *"),
    valid("* * * * MON-FRI"),
    valid("\t0\t0  * *\n*"),
    expand("0 0 * Foo *"),
    expand("0 0 * * mon-foo"),
    expand("0 0 31 2 *", strict=True),
    expand("0 0 30 2 *", strict=True),
    expand("0 0 29 2 *", strict=True),
    expand("0 0 29 2 *", strict=True, strict_year=2023),
    expand("0 0 29 2 *", strict=True, strict_year=[2023, 2024]),
    expand("0 0 29 2 * 0 2023,2025", strict=True),
    expand("0 0 29 2 * 0 2024", strict=True),
    expand("0 0 31 4,6 *", strict=True),
    expand("0 0 31 4,5 *", strict=True),
    expand("0 0 30,31 2 *", strict=True),
    expand("0 0 l 2 *", strict=True),
    it("0 0 31 2 *", T0, "np"),
    it("0 0 30 2 *", T0, "n", max_years=3),
    allx("0 0 30 2 *", T0, 3, max_years=3),
    allx("0 0 1 1 * 0 2025-2026", T0, 5),
    allx("0 0 1 1 * 0 2025-2026", T0, 5, max_years=100),
    allx("0 0 1 1 * 0 2020-2023", T0, 6, d="prev"),
    it("0 0 1 1 * 0 2090", T0, "n"),
    it("0 0 1 1 * 0 2090", T0, "n", max_years=70),
    it("0 0 1 1 * 0 2090", T0, "n", max_years=0),
    it("0 0 * * * 0 2090", dt(2089, 12, 31), "nn", max_years=0),
])

job("hashed and aliased", [
    expand("H H * * *", hash_id="backup-job"),
    expand("H H * * *", hash_id="report-job"),
    expand("H(0-29) H(9-17) * * H(1-5)", hash_id="report-job"),
    expand("H/15 * * * *", hash_id="poller"),
    expand("H(0-29)/10 * * * *", hash_id="poller"),
    expand("H(30-59)/7 * * * *", hash_id="poller"),
    expand("H * * * * H H", hash_id="quartz"),
    expand("h * * * *", hash_id="lower"),
    expand("h * * * *", hash_id="lower", hash_str=True),
    expand("H * * * *"),
    expand("H(5-5) * * * *", hash_id="x"),
    expand("H(9-3) * * * *", hash_id="x"),
    expand("H(0-29)/0 * * * *", hash_id="x"),
    expand("H/0 * * * *", hash_id="x"),
    expand("H(1-2)(3-4) * * * *", hash_id="x"),
    expand("@midnight", hash_id="nightly"),
    expand("@hourly", hash_id="nightly"),
    expand("@daily", hash_id="nightly"),
    expand("@weekly", hash_id="nightly"),
    expand("@monthly", hash_id="nightly"),
    expand("@yearly", hash_id="nightly"),
    expand("@annually", hash_id="été"),
    expand("@midnight"),
    expand("@Hourly"),
    expand("@weekly"),
    expand("@monthly"),
    expand("@annually"),
    it("H H * * *", T0, "nnnp", hash_id="backup-job"),
    it("@daily", T0, "nnp", hash_id="nightly"),
    it("@weekly", T0, "nnp"),
    valid("H H * * *"),
    valid("H H * * *", hash_id="job"),
])

job("expand from the start time", [
    it("*/7 * * * *", dt(2024, 1, 15, 10, 4), "nnnnn", expand_from_start_time=True),
    it("*/7 * * * *", dt(2024, 1, 15, 10, 4), "nnnnn"),
    it("0 */5 * * *", dt(2024, 1, 15, 13, 0), "nnnnn", expand_from_start_time=True),
    it("0 0 */10 * *", dt(2024, 1, 15), "nnnnn", expand_from_start_time=True),
    it("0 0 1 */5 *", dt(2024, 4, 9), "nnnn", expand_from_start_time=True),
    it("0 0 * * */3", dt(2024, 1, 18), "nnnnn", expand_from_start_time=True),
    it("0 0 * * 1-5", dt(2024, 1, 18), "nnnnn", expand_from_start_time=True),
    it("0 0 * * * */10", dt(2024, 1, 18), "nn", expand_from_start_time=True),
    it("*/7 * * * *", 0.0, "nn", ret="float", expand_from_start_time=True),
])

job("timestamps", [
    it("*/5 * * * *", 1700000000.25, "cnnpc", ret="float"),
    it("*/5 * * * *", 1700000000.5, "cnn", ret="dt"),
    it("* * * * * *", 1700000000.999999, "cnn", ret="float"),
    it("0 0 * * *", -86400.5, "cnnpp", ret="float"),
    it("0 0 * * *", 0.0, "nnpp", ret="float"),
    it("*/10 * * * *", dt(2024, 1, 15, 10, 7, 30, 123456), "cnc", ret="float"),
    it("*/10 * * * *", dt(1969, 12, 31, 23, 59, 59, 999999), "cnpc", ret="float"),
    it("0 0 1 1 *", dt(2199, 6, 1), "np", ret="float"),
    it("0 0 1 1 *", 7258118400.0, "pp", ret="float"),
])

job("fixed offsets", [
    it("0 9 * * *", dt(2024, 1, 15, 10, tz="+05:30"), "nnnppc"),
    it("0 9 * * *", dt(2024, 1, 15, 10, tz="+05:30"), "nnpc", ret="float"),
    it("0 0 * * *", dt(2024, 1, 15, 10, tz="UTC"), "nnp"),
    it("30 23 * * *", dt(2024, 1, 15, 23, 45, tz="-09:30"), "nnp"),
    it("0 0 l * *", dt(2024, 2, 28, 22, tz="-03:00"), "nnp", ret="float"),
    it("*/20 * * * *", dt(2024, 6, 1, 0, 5, tz="+12:45"), "nnnppp"),
])

job("New York", [
    it("30 2 * * *", dt(2024, 3, 9, 12, tz=NY), "nnnnpppp"),
    it("30 1 * * *", dt(2024, 11, 2, 12, tz=NY), "nnnnpppp"),
    it("0 * * * *", dt(2024, 3, 10, 0, 30, tz=NY), "nnnnnpppp"),
    it("0 * * * *", dt(2024, 11, 3, 0, 30, tz=NY), "nnnnnnpppppp"),
    it("*/30 * * * *", dt(2024, 11, 3, 0, 50, tz=NY), "nnnnnnnppppppp"),
    it("*/30 * * * *", dt(2024, 3, 10, 1, 10, tz=NY), "nnnnppppp"),
    it("0 2 * * *", dt(2024, 3, 9, 23, tz=NY), "nnpp"),
    it("0 2 * * *", dt(2024, 3, 9, 23, tz=NY), "nnpp", ret="float"),
    it("15 1 * * *", dt(2024, 11, 3, 1, 20, tz=NY), "nnpp"),
    it("15 1 * * *", dt(2024, 11, 3, 1, 20, tz=NY, fold=1), "nnpp"),
    it("15 1 * * *", dt(2024, 11, 3, 1, 10, tz=NY, fold=1), "nnpppp"),
    it("0 0 * * * 0", dt(2024, 3, 10, 1, 59, 50, tz=NY), "nnnpp"),
    it("* * * * * */20", dt(2024, 3, 10, 1, 59, 30, tz=NY), "nnnppp"),
    it("* 2 * * *", dt(2024, 3, 10, 1, 58, tz=NY), "nnnppp"),
    it("59 1 * * *", dt(2024, 11, 3, 0, 0, tz=NY), "nnnppp"),
    it("0 9 * * mon-fri", dt(2024, 3, 8, 17, tz=NY), "nnnppp", ret="float"),
    it("0 0 1 * *", dt(2024, 1, 15, 10, tz=NY), "nnnnnnnnnnnppp"),
    it("30 2 * * *", dt(2024, 3, 10, 2, 30, tz=NY), "cnp"),
    it("30 2 * * *", dt(2024, 3, 10, 2, 30, tz=NY, fold=1), "cnp"),
])

job("London and Lord Howe", [
    it("30 1 * * sun", dt(2024, 3, 20, tz=LON), "nnppp"),
    it("30 1 * * sun", dt(2024, 10, 20, tz=LON), "nnnpp"),
    it("0,30 1 * * *", dt(2024, 10, 27, 0, 15, tz=LON), "nnnnnpppppp"),
    it("15 2 * * *", dt(2024, 4, 6, 1, tz=LH), "nnnpppp"),
    it("15 1 * * *", dt(2024, 4, 6, 1, tz=LH), "nnnpppp"),
    it("*/15 1-2 * * *", dt(2024, 4, 7, 0, 50, tz=LH), "nnnnnnnnnppppppppp"),
    it("*/15 1-2 * * *", dt(2024, 10, 6, 1, 20, tz=LH), "nnnnnppppp"),
    it("0 9 * * *", dt(2024, 6, 1, 8, tz=KOL), "nnp"),
])

job("Apia's missing day", [
    it("0 12 * * *", dt(2011, 12, 28, 13, tz=APIA), "nnnnpppp"),
    it("0 12 30 * *", dt(2011, 12, 1, tz=APIA), "nnnpp"),
    it("0 */8 * * *", dt(2011, 12, 29, 9, tz=APIA), "nnnnnppppp"),
    it("0 12 * * fri", dt(2011, 12, 20, tz=APIA), "nnnpp"),
    it("0 0 l * *", dt(2011, 11, 1, tz=APIA), "nnpp"),
])

job("match", [
    match("0 9 * * mon-fri", dt(2024, 1, 15, 9)),
    match("0 9 * * mon-fri", dt(2024, 1, 15, 9, 0, 59)),
    match("0 9 * * mon-fri", dt(2024, 1, 15, 9, 1)),
    match("0 9 * * mon-fri", dt(2024, 1, 14, 9)),
    match("0 9 * * mon-fri", dt(2024, 1, 15, 9, 0, 0, 500)),
    match("0 9 * * mon-fri", dt(2024, 1, 15, 8, 59, 59, 999999)),
    match("*/5 * * * * */10", dt(2024, 1, 15, 9, 5, 10)),
    match("*/5 * * * * */10", dt(2024, 1, 15, 9, 5, 11)),
    match("*/5 * * * * */10", dt(2024, 1, 15, 9, 5, 9)),
    match("0 0 l * *", dt(2024, 2, 29)),
    match("0 0 l * *", dt(2023, 2, 28)),
    match("0 0 l * *", dt(2024, 2, 28)),
    match("0 0 1,15 * 1", dt(2024, 1, 22)),
    match("0 0 1,15 * 1", dt(2024, 1, 22), day_or=False),
    match("0 0 * * 2#3", dt(2024, 1, 16)),
    match("0 0 * * 2#3", dt(2024, 1, 9)),
    match("30 2 * * *", dt(2024, 3, 10, 3, 0, tz=NY)),
    match("30 1 * * *", dt(2024, 11, 3, 1, 30, tz=NY, fold=1)),
    match("0 0 * * *", dt(2024, 1, 15, 0, 0, 30), precision=10),
    match("0 0 * * *", dt(2024, 1, 15, 0, 0, 30), precision=40),
    match("0 0 * * *", dt(2024, 1, 15, 0, 0, 30), precision=0),
    match("0 0 1 1 * 0 2030", dt(2024, 1, 15)),
    match("* * * * *", 1705313250.0),
    match("0 5 * * *", dt(2024, 1, 15, 0, 0, 0, tz="+05:00")),
    mrange("0 9 * * *", dt(2024, 1, 15, 8), dt(2024, 1, 15, 10)),
    mrange("0 9 * * *", dt(2024, 1, 15, 9, 30), dt(2024, 1, 15, 10)),
    mrange("0 9 * * *", dt(2024, 1, 15, 8), dt(2024, 1, 15, 8, 59)),
    mrange("0 9 * * *", dt(2024, 1, 15, 8, tz="+01:00"), dt(2024, 1, 15, 8, 30, tz="UTC")),
    mrange("0 9 * * *", dt(2024, 1, 15, 8, tz=NY), dt(2024, 1, 15, 10)),
    mrange("0 9 * * *", dt(2024, 1, 15, 8), dt(2024, 1, 15, 10, tz=NY)),
    mrange("0 9 * * *", dt(2024, 1, 15, 10), dt(2024, 1, 15, 8)),
    mrange("0 9 * * *", dt(2024, 1, 15, 8, 0, 0, 1), dt(2024, 1, 15, 9)),
    mrange("0 9 * * * 0 2030", dt(2024, 1, 15, 8), dt(2024, 1, 15, 10)),
    mrange("15 1 * * *", dt(2024, 11, 3, 1, 20, tz=NY), dt(2024, 11, 3, 1, 10, tz=NY, fold=1)),
])

job("croniter_range", [
    rng("0 9 * * mon-fri", dt(2024, 1, 12), dt(2024, 1, 20)),
    rng("0 9 * * mon-fri", dt(2024, 1, 20), dt(2024, 1, 12)),
    rng("0 0 * * *", dt(2024, 1, 1), dt(2024, 1, 4)),
    rng("0 0 * * *", dt(2024, 1, 1), dt(2024, 1, 4), exclude_ends=True),
    rng("0 0 * * *", dt(2024, 1, 4), dt(2024, 1, 1), exclude_ends=True),
    rng("0 0 * * *", 1704067200.0, 1704326400.0),
    rng("0 0 * * *", 1704067200.0, 1704326400.0, ret="dt"),
    rng("0 0 * * *", dt(2024, 1, 1), dt(2024, 1, 4), ret="float"),
    rng("0 0 * * *", 1704067200.0, dt(2024, 1, 4)),
    rng("0 0 * * *", dt(2024, 1, 1), dt(2024, 1, 4, tz="UTC")),
    rng("0 0 1 1 *", dt(2020, 6, 1), dt(2027, 6, 1)),
    rng("0 0 29 2 *", dt(2023, 1, 1), dt(2024, 1, 1)),
    rng("0 0 29 2 *", dt(2023, 1, 1), dt(2025, 1, 1)),
    rng("0 0 29 2 *", dt(2025, 1, 1), dt(2023, 1, 1)),
    rng("30 2 * * *", dt(2024, 3, 8, tz=NY), dt(2024, 3, 12, tz=NY)),
    rng("30 1 * * *", dt(2024, 11, 2, tz=NY), dt(2024, 11, 5, tz=NY)),
    rng("0 * * * *", dt(2024, 11, 3, 0, 30, tz=NY), dt(2024, 11, 3, 4, tz=NY), ret="float"),
    rng("0 * * * *", dt(2024, 11, 3, 4, tz=NY), dt(2024, 11, 3, 0, 30, tz=NY)),
    rng("0 0 * * *", dt(2024, 1, 1, tz=NY), dt(2024, 1, 3, 6, tz=LON)),
    rng("*/20 * * * * *", dt(2024, 1, 1, 0, 0, 0), dt(2024, 1, 1, 0, 1, 0)),
    rng("0 0 * * *", dt(2024, 1, 1), dt(2024, 1, 1)),
    rng("0 0 * * *", dt(2024, 1, 1), dt(2024, 1, 1), exclude_ends=True),
    rng("*/7 * * * *", dt(2024, 1, 1, 0, 4), dt(2024, 1, 1, 1, 0), expand_from_start_time=True),
    rng("* * * * *", dt(2024, 1, 1), dt(2024, 1, 1, 0, 5), day_or=False),
    rng("0 0 30 2 *", dt(2024, 1, 1), dt(2026, 1, 1)),
    rng("bad", dt(2024, 1, 1), dt(2026, 1, 1)),
])

# Random schedules: each field drawn from a small grammar.
rnd = random.Random(20261019)
ATOM = {
    0: lambda: str(rnd.randint(0, 59)),
    1: lambda: str(rnd.randint(0, 23)),
    2: lambda: rnd.choice([str(rnd.randint(1, 31)), "l", str(rnd.randint(1, 28))]),
    3: lambda: rnd.choice([str(rnd.randint(1, 12)), rnd.choice(["jan", "apr", "jul", "oct", "dec"])]),
    4: lambda: rnd.choice([str(rnd.randint(0, 6)), rnd.choice(["mon", "wed", "fri", "sun"])]),
    5: lambda: str(rnd.randint(0, 59)),
}


def field(i):
    k = rnd.random()
    if k < 0.35:
        return "*"
    if k < 0.5:
        return "*/" + str(rnd.choice([2, 3, 5, 7, 10, 15]))
    if k < 0.65:
        a, b = ATOM[i](), ATOM[i]()
        if "l" in (a, b) and i == 2:
            return a
        return a + "-" + b + (("/" + str(rnd.randint(1, 4))) if rnd.random() < 0.4 else "")
    if k < 0.8:
        return ",".join(ATOM[i]() for _ in range(rnd.randint(2, 3)))
    if i == 4 and k < 0.88:
        return rnd.choice(["mon", "tue", "fri", "1", "5"]) + "#" + str(rnd.randint(1, 5))
    if i == 2 and k < 0.88:
        return str(rnd.randint(1, 31)) + "w"
    return ATOM[i]()


TZS = [None, None, None, "UTC", "+05:30", NY, LON, LH]
for n in range(24):
    ops = []
    for _ in range(6):
        nf = rnd.choice([5, 5, 5, 6])
        expr = " ".join(field(i) for i in range(nf))
        start = dt(rnd.randint(2023, 2026), rnd.randint(1, 12), rnd.randint(1, 28),
                   rnd.randint(0, 23), rnd.randint(0, 59), rnd.randint(0, 59),
                   tz=rnd.choice(TZS))
        seq = "".join(rnd.choice("nnnp") for _ in range(rnd.randint(3, 6)))
        kw = {}
        if rnd.random() < 0.2:
            kw["day_or"] = False
        ops.append(it(expr, start, seq, ret=rnd.choice(["dt", "dt", "float"]), **kw))
        if rnd.random() < 0.4:
            ops.append(expand(expr))
    job(f"random {n + 1}", ops)

with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(jobs), "jobs,", sum(len(j["ops"]) for j in jobs), "operations")
