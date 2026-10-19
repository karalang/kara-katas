# Writes data/ for mini_crondesc: the catalogs cron_descriptor ships, a few
# made-up catalogs for locale_location, some crontabs, and data/jobs.jsonl.
import json
import os
import random
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def write(path, body, binary=False):
    full = os.path.join(DATA, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb" if binary else "w", encoding=None if binary else "utf-8", newline=None if binary else "") as f:
        f.write(body)


def mo(entries, header="Content-Type: text/plain; charset=UTF-8\n"):
    # msgfmt's layout: the header first, then the ids in sorted order.
    items = []
    if header is not None:
        items.append((b"", header.encode("utf-8")))
    for k in sorted(entries):
        items.append((k.encode("utf-8"), entries[k].encode("utf-8")))
    items.sort(key=lambda kv: kv[0])
    n = len(items)
    ids = b""
    strs = b""
    offs = []
    for k, v in items:
        offs.append((len(ids), len(k), len(strs), len(v)))
        ids += k + b"\0"
        strs += v + b"\0"
    start = 7 * 4 + 16 * n
    out = struct.pack("<7I", 0x950412DE, 0, n, 28, 28 + 8 * n, 0, start)
    for io, il, so, sl in offs:
        out += struct.pack("<2I", il, start + io)
    for io, il, so, sl in offs:
        out += struct.pack("<2I", sl, start + len(ids) + so)
    return out + ids + strs


if os.path.isdir(DATA):
    shutil.rmtree(DATA)
os.makedirs(DATA)

# The catalogs as the package ships them.
pkg = os.path.join(HERE, "cron_descriptor", "locale")
LOCALES = sorted(f[:-3] for f in os.listdir(pkg) if f.endswith(".mo"))
for f in LOCALES:
    write(f"locale/{f}.mo", open(os.path.join(pkg, f + ".mo"), "rb").read(), True)

# A team's own catalogs, read through locale_location.
GB = {
    "At ": "At ",
    "At": "At",
    " and": " and",
    " and ": " and ",
    "every minute": "every minute",
    "every second": "every second",
    "every hour": "every hour",
    ", every day": ", every day",
    "every {0} minutes": "every {0} minutes",
    "every {0} hours": "every {0} hours",
    "every {0} seconds": "every {0} seconds",
    "at {0} minutes past the hour": "at {0} minutes past the hour",
    "at {0} seconds past the minute": "at {0} seconds past the minute",
    "at {0}": "at {0}",
    "between {0} and {1}": "from {0} to {1}",
    ", only on {0}": ", on {0} only",
    ", {0} through {1}": ", {0} to {1}",
    ", only in {0}": ", in {0} only",
    ", on day {0} of the month": ", on the {0} of the month",
    ", on the last day of the month": ", on the final day of the month",
    "minutes {0} through {1} past the hour": "minutes {0} to {1} past the hour",
    "Every minute between {0} and {1}": "Every minute from {0} to {1}",
    ", every {0} days of the week": ", every {0} days of the week",
    ", every {0} months": ", every {0} months",
    ", every {0} days": ", every {0} days",
    ", between day {0} and {1} of the month": ", from day {0} to {1} of the month",
    ", every {0} weeks": ", every {0} weeks",
    "AM": "am",
    "PM": "pm",
    "An error occurred when generating the expression description.  Check the cron expression syntax.":
        "Sorry, that cron expression could not be described.",
}
write("teamlocale/en_GB.mo", mo(GB), True)
# Half a pirate catalogue: everything it lacks comes back empty.
PIRATE = {
    "At ": "Ahoy at ",
    "every minute": "every blessed minute",
    "every hour": "every bell",
    ", every day": ", every day o' the week",
    "every {0} minutes": "every {0} minutes, arr",
    "at {0}": "at {0} sharp",
    "AM": "in the forenoon",
    "PM": "in the dog watch",
    ", only on {0}": ", only of a {0}",
    "between {0} and {1}": "from {0} till {1}",
}
write("teamlocale/en_PIRATE.mo", mo(PIRATE), True)
# A catalog with no header at all, so its strings are decoded as ASCII.
write("teamlocale/en_PLAIN.mo", mo({"At ": "Fires at ", "AM": "a.m.", "PM": "p.m.", "every minute": "each minute"}, None), True)
# Broken catalogs: a bad magic number and a truncated table fall back to
# the package's en_US; a file too short to hold a magic number does not.
write("teamlocale/xx_BAD.mo", b"\xde\xad\xbe\xef" + bytes(24), True)
whole = mo({"At ": "At "})
write("teamlocale/xx_CUT.mo", whole[:40], True)
write("teamlocale/xx_TINY.mo", b"\x95\x04", True)

# --------------------------------------------------------- expressions

REAL = [
    # system crontabs and packages
    "17 * * * *", "25 6 * * *", "47 6 * * 7", "52 6 1 * *",
    "*/5 * * * *", "0 */2 * * *", "30 2 * * 1-5", "0 0 1 1 *",
    "0 3 * * 0", "15 4 * * 1,3,5", "0 12 * * MON-FRI", "0 0 * * SUN",
    "0 9-17 * * 1-5", "*/15 9-17 * * MON-FRI", "0 22 * * 1-5",
    "0 0 1,15 * *", "0 4 1 */3 *", "0 0 L * *", "0 0 LW * *", "0 0 15W * *",
    "0 0 1W * *", "0 0 W1 * *", "0 6 L-3 * *", "0 10 ? * 6#3", "0 10 ? * 2#1",
    "0 12 ? * 5L", "0 23 ? * FRI#5", "0 0 * * 0#2",
    "5 4 * * sun", "0 0,12 1 */2 *", "23 0-20/2 * * *", "0 0-5 * * *",
    "0-10 11 * * *", "30 6,14,16 * * *", "15 10 * * ?", "0 0 12 1/1 * ? *",
    "0 0/5 14 * * ?", "0 0/5 14,18 * * ?", "0 0-5 14 * * ?", "0 10,44 14 ? 3 WED",
    "0 15 10 ? * MON-FRI", "0 15 10 15 * ?", "0 15 10 L * ?", "0 15 10 ? * 6L",
    "0 15 10 ? * 6L 2002-2005", "0 15 10 ? * 6#3", "0 0 12 1/5 * ?", "0 11 11 11 11 ?",
    "0 15 10 * * ? 2025", "30 11 * * ? 2031",
    # Kubernetes CronJobs, Airflow, GitHub Actions
    "0 */6 * * *", "*/30 * * * *", "0 1 * * *", "0 0 * * 1", "0 8 1-7 * 1",
    "45 23 * * 6", "*/10 0-6 * * *", "0 5 * * 1,2,3,4,5", "0 18 * * 5",
    "5,35 * * * *", "0 0 */3 * *", "0 2 * 1,4,7,10 *", "0 0 1 JAN,JUL *",
    "0 0 1 jan-mar *", "30 3 * * 6,0", "1 0 * * *",
    # AWS EventBridge
    "0 10 * * ? *", "15 12 * * ? *", "0 18 ? * MON-FRI *", "0 8 1 * ? *",
    "0/15 * * * ? *", "0/10 * ? * MON-FRI *", "0/5 8-17 ? * MON-FRI *", "0 9 ? * 2#1 *",
    # seconds and years
    "*/10 * * * * *", "30 * * * * *", "0-30 * * * * *", "5/15 * * * * *",
    "10-40/5 * * * * *", "15,45 * * * * *", "0 0 0 * * * 2030", "0 0 0 1 1 * 2025-2030",
    "0 0 0 1 1 * 2020/4", "0 0 0 1 1 * */2", "0 0 0 1 1 * 2025,2027,2029",
    "0 0 0 1 1 * 1800", "* * * * * * *",
    # odd and extreme
    "* * * * *", "0 0 * * *", "0 0 * * 7", "0 0 * * 1-7", "0 0 * * 0-6",
    "0 0 * * 1-3/2,5", "0 0 * * FRI/2", "0 0 * * 1-5/2", "0 0 * * 1-5/7",
    "0 0 * * 1,3,5/2", "0 0 * * 1-2/3", "0 0 * * 3/2", "0 0 */2 */3 *",
    "0 0 3/2 * *", "0 0 * 3/2 *", "0 0 1-15/3 * *", "*/1 * * * *", "0 */1 * * *",
    "0/1 * * * *", "0 0/1 * * *", "1/5 * * * *", "0 1/3 * * *", "0 0 1/1 * *",
    "0 0 * 1/1 *", "0 0 * * 1/1", "0 0 0/7 * *",
    "0 0,6-23/2 * * *", "0 6-23/2,0 * * *", "0,30 6-23/2 * * *", "*/7,30 * * * *",
    "5-10,20-25 * * * *", "1,2 * * * *", "1,2,3 * * * *", "0 1,2 * * *",
    "0 0 1,2,3,4 * *", "0 0 * 1,2 *", "0 0 * * 1,2", "0 0 1-3,5 * *",
    "0 0 * 1-3,5 *", "0 0 * * 1-3,5", "0 0 1 2-11/3 *",
    "59 23 31 12 5", "0 12 29 2 *", "30 0 * * *", "0 12 * * *", "0 13 * * *",
    "7 23 * * *", "0 0 * * *", "00 09 * * *", "+5 7 * * *", "05 007 * * *",
    "0-0 * * * *", "0 0-0 * * *", "30-45 9 * * *", "0-59 * * * *",
    "0 0 * * mon,wed", "0 0 * * Mon-Wed", "0 0 * DEC *", "0 0 * dec-feb *",
    "0 0 1-31 * *", "0 0 25 12 *", "0 0 ? * *", "0 0 * * ?", "? ? ? ? ?",
    "0 0 13W * *", "0 0 31W * *", "0 0 wl * *", "0 0 WL * *", "0 0 L-15 * *",
    "0 0 L-1 * *", "0 0 ? * 1#1", "0 0 ? * 7#4", "0 0 ? * 0L", "0 0 ? * SUNL",
    "0 0 ? * MON#2,FRI#4", "0 0 ? * 1#6", "0 0 ? * 3#0",
]

BROKEN = [
    "", "   ", "* * *", "* * * *", "1 2 3 4 5 6 7 8", "* * * * * * * * *",
    "a b c d e", "60 * * * *", "0 25 * * *", "0 0 32 * *", "0 0 * 13 *",
    "0 0 * 0 *", "0 0 * * 8", "0 0 * * 9", "x * * * *", "0 x * * *",
    "0 0 x * *", "0 0 * x *", "0 0 * * x", "0 0 * * L", "0 0 * FOO *",
    "0 0 * * MON-FOO", "0 0 * * 1#", "0 0 * * #1", "*/x * * * *",
    "*/{1} * * * *", "*/{ * * * *", "*/} * * * *", "*/{x} * * * *",
    "0 0 * * 1-", "0 0 * * -1", "0 0 L-x * *", "0 0 xW * *",
    "1-2-3 * * * *", "5/ * * * *", "/5 * * * *", "0 0 * 1-13 *",
    "0 0 0 1 1 * 10000", "0 0 0 1 1 * 99999", "0 0 0 1 1 * 0", "0 0 0 1 1 * x",
    "0 0 * * 6-", "0 0 * * 9-12", "0 0 1--2 * *",
]

# A random walk over the field syntax, seeded so data/ is the same each time.
rng = random.Random(1137)


def field(kind):
    lo, hi = {"s": (0, 59), "m": (0, 59), "h": (0, 23), "dom": (1, 31), "mon": (1, 12), "dow": (0, 6), "y": (1990, 2040)}[kind]
    names_mon = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    names_dow = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

    def one():
        v = rng.randint(lo, hi)
        if kind == "mon" and rng.random() < 0.3:
            return names_mon[v - 1]
        if kind == "dow" and rng.random() < 0.3:
            return names_dow[v]
        return str(v)

    r = rng.random()
    if r < 0.25:
        return "*"
    if r < 0.45:
        return one()
    if r < 0.55:
        return "*/" + str(rng.randint(1, 15))
    if r < 0.65:
        a = rng.randint(lo, hi)
        b = rng.randint(a, hi)
        return f"{a}-{b}"
    if r < 0.72:
        a = rng.randint(lo, hi)
        b = rng.randint(a, hi)
        return f"{a}-{b}/{rng.randint(1, 9)}"
    if r < 0.8:
        return f"{rng.randint(lo, hi)}/{rng.randint(1, 9)}"
    if r < 0.92:
        return ",".join(one() for _ in range(rng.randint(2, 4)))
    if kind == "dom":
        return rng.choice(["L", "LW", f"{rng.randint(1, 28)}W", f"L-{rng.randint(1, 9)}", "?"])
    if kind == "dow":
        return rng.choice([f"{rng.randint(0, 6)}L", f"{rng.randint(0, 6)}#{rng.randint(1, 5)}", "?"])
    return f"{one()},{rng.randint(lo, hi)}-{hi}"


RANDOM = []
for _ in range(260):
    shape = rng.choice([5, 5, 5, 6, 7])
    parts = [field(k) for k in ["m", "h", "dom", "mon", "dow"]]
    if shape >= 6:
        parts = [field("s")] + parts
    if shape == 7:
        parts.append(field("y"))
    RANDOM.append(" ".join(parts))

jobs = []
OPTS = [
    {},
    {"casing": "Title"},
    {"casing": "LowerCase"},
    {"verbose": True},
    {"h24": False},
    {"dow0": False},
    {"verbose": True, "casing": "Title", "h24": False},
]
# Every option set on a quarter of the schedules; the rest get the default,
# the three casings and verbose, plus a one-indexed week where they name days.
for k, e in enumerate(REAL):
    for o in OPTS if k % 4 == 0 else OPTS[:4]:
        jobs.append(["desc", e, o])
    if k % 4 != 0 and len(e.split()) >= 5 and e.split()[-1 if len(e.split()) == 5 else 5] not in ("*", "?"):
        jobs.append(["desc", e, {"dow0": False}])
for e in BROKEN:
    jobs.append(["desc", e, {}])
for e in RANDOM:
    jobs.append(["desc", e, rng.choice(OPTS)])

# Every catalog over a handful of schedules, 12-hour and 24-hour.
SAMPLE = [
    "*/5 * * * *", "30 6,14,16 * * *", "0 9-17 * * 1-5", "0 0 L * *", "0 10 ? * 6#3",
    "15,45 * * * * *", "0 4 1 */3 *", "0 0 * * FRI/2", "0-10 11 * * *", "0 0 0 1 1 * 2025-2030",
    "0 0 15W * *", "0 12 ? * 5L", "5 4 * * sun", "23 0-20/2 * * *", "0 0 L-3 * *",
    "x * * * *",
]
for loc in LOCALES + ["xx_XX", "de"]:
    for e in SAMPLE:
        jobs.append(["desc", e, {"locale": loc}])
    for e in SAMPLE[:4]:
        jobs.append(["desc", e, {"locale": loc, "casing": "Title", "h24": True}])
for loc in ["en_GB", "en_PIRATE", "en_PLAIN", "xx_BAD", "xx_CUT", "xx_TINY", "fr_FR"]:
    for e in SAMPLE:
        jobs.append(["desc", e, {"locale": loc, "location": "data/teamlocale"}])

# The parts on their own, as get_description(DescriptionTypeEnum.X) gives them.
PARTS = ["TIMEOFDAY", "SECONDS", "MINUTES", "HOURS", "DAYOFWEEK", "MONTH", "DAYOFMONTH", "YEAR", "FULL"]
for e in ["*/5 * * * *", "0 15 10 ? * 6L 2002-2005", "10-40/5 * * * * *", "0 0 * 13 *", "0 0 * * 9",
          "*/{1} * * * *", "*/{ * * * *", "*/{x} * * * *", "0 0 0 1 1 * 10000", "0 0 x * *", "0 0 * * L",
          "0 0 * * 1-", "0 0 * * -1", "0 x * * *", "0 0 L-x * *"]:
    for p in PARTS:
        jobs.append(["desc", e, {"part": p}])

# Options set through keyword arguments, including unknown ones.
for kw in [{"verbose": True}, {"casing_type": "Title"}, {"use_24hour_time_format": False},
           {"locale_code": "de_DE"}, {"locale_code": "en_US"}, {"day_of_week_start_index_zero": False},
           {"locale": "de_DE"}, {"use_24_hour": True}, {"verbose": True, "colour": "red"}]:
    for e in ["0 9-17 * * 1-5", "30 6,14,16 * * 0"]:
        jobs.append(["desc", e, {"kwargs": kw}])

# The system locale, for an Options() that is not told one.
for sysloc in ["en_US", "en_GB", "de_DE", "fr_CA", "es_MX", None]:
    for e in ["30 6,14,16 * * *", "0 22 * * 1-5"]:
        jobs.append(["desc", e, {"system": sysloc, "auto": True}])

# ExpressionValidator, over the good and the bad.
VALIDATE = REAL + BROKEN + RANDOM[:120] + [
    "60 0 * * *", "0 24 * * *", "0 0 0 * *", "0 0 * 0 *", "0 0 * * 8", "0 0 * * 7",
    "0-60 * * * *", "30-10 * * * *", "0 20-10 * * *", "0 0 20-10 * *", "0 0 * 10-2 *",
    "0 0 * * 5-1", "0 0 * * FRI-MON", "0 0 * NOV-FEB *", "0 0 * jan *", "0 0 * JAN-mar *",
    "0 0 * jan,FEB *", "0 0 * Jan-Mar,Dec *", "0 0 * JAN,13 *", "0 0 * * mon", "0 0 * * Mon-Fri",
    "0 0 * * MON,BAD", "0 0 * * mon#2", "0 0 * * BAD#2", "0 0 * * 1#6", "0 0 * * 1#0",
    "0 0 * * 8L", "0 0 * * 6l", "*/60 * * * *", "*/0 * * * *", "0 */24 * * *",
    "0 0 */32 * *", "0 0 * */13 *", "0 0 * * */8", "0 0 0 1 1 * 1969", "0 0 0 1 1 * 2100",
    "0 0 0 1 1 * 2030-2020", "0 0 0 1 1 * 2020/130", "0 0 0 1 1 * */130", "0 0 0 1 1 * 5/10",
    "0 0 0 1 1 * 2020,2021-2023", "0 0 0 1 1 * 20,21",
    ",".join(str(i) for i in range(25)) + " * * * *",
    "0 " + ",".join(str(i) for i in range(24)) + " * * *",
    "0 " + ",".join(str(i % 24) for i in range(25)) + " * * *",
    "0 0 " + ",".join(str(i) for i in range(1, 32)) + " * *",
    "0 0 " + ",".join(str(i % 31 + 1) for i in range(32)) + " * *",
    "0 0 * 1,2,3,4,5,6,7,8,9,10,11,12,1 *", "0 0 * * 0,1,2,3,4,5,6,0",
    "0 0 L-32 * *", "0 0 L-0 * *", "0 0 l-5 * *", "0 0 32W * *", "0 0 W32 * *", "0 0 Lw * *",
    "0 0 w * *", "0 0 LL * *", "0 0 ?? * *", "0 0 * * ??", "0 0 1-5/40 * *", "0 0 1/0 * *",
    "0 0 1-2-3 * *", "0 1-2-3 * * *", "1-2-3 * * * *", "0 0 * 1-2-3 *",
    "0 0 0 1 1 * 2030 extra", "0 0 * * 1 2020", "0 0 * * ? 2020", "0 0 ? * 1 2020",
    "5 0 0 * * *", "0 5 0 * * *", "0 0 * * 1 *",
]
for e in VALIDATE:
    jobs.append(["validate", e])

# The cron_descriptor command line.
CLI = [
    ["*/5 * * * *"], ["30 6 * * 1-5", "-H"], ["30 6 * * 1-5", "-c", "Title"],
    ["-c", "LowerCase", "0 0 L * *"], ["--casing=Title", "-v", "0 9-17 * * *"], ["-vW", "0 9 * * 1"],
    ["-W", "0 9 * * 1-5"], ["--one-indexed-week", "0 9 * * 7"], ["-cTitle", "0 */2 * * *"],
    ["--use-24-hour-time-format", "30 18 * * *"], ["--verbose", "* * * * *"], ["--verb", "0 0 * * *"],
    ["--cas", "Title", "0 0 * * *"], ["-c", "Bogus", "0 0 * * *"], [], ["-v"], ["0 0 * * *", "extra"],
    ["-x", "0 0 * * *"], ["--", "-5 * * * *"], ["0 0 * * *", "--bogus"], ["-h"], ["--help"],
    ["0 0 *"], ["0 0 * 13 *"], ["-c"], ["--casing"], ["-H", "-H", "0 12 * * *"],
    ["--casing", "LowerCase", "--casing", "Title", "15 10 * * *"], ["-vH", "-cLowerCase", "*/10 9-17 * * 1-5"],
    ["-5 * * * *"], ["-5"], ["-5.5", "-v"], ["--u", "0 18 * * *"], ["-c", "-v", "0 0 * * *"], ["-vx", "0 0 * * *"],
    ["--verbose=yes", "0 0 * * *"], ["--casing=", "0 0 * * *"], ["-c=Title", "0 6 * * *"],
    ["-Hc", "Title", "0 6 * * *"], ["-cH", "0 6 * * *"], ["-", "0 6 * * *"], ["0 6 * * *", "-"],
    ["--casing", "Title", "-h", "0 0 *"], ["-c", "Bogus", "-h"], ["a", "b", "c"], ["-x", "-y"],
    ["--", "--", "0 0 * * *"], ["0 0 * * *", "--", "-v"], ["-v", "--", "0 0 * * 1"],
]
for argv in CLI:
    jobs.append(["cli", argv, "en_US"])
jobs.append(["cli", ["30 6,14,16 * * *"], "de_DE"])
jobs.append(["cli", ["0 22 * * 1-5", "-H"], "fr_FR"])

# Crontabs, described line by line.
CRONTABS = {
    "web01.crontab": """# m h  dom mon dow   command
SHELL=/bin/bash
MAILTO=ops@example.com
*/5 * * * * /usr/local/bin/healthcheck --quiet
0 3 * * * /opt/app/bin/backup-db --retain 14
30 4 * * 0 /usr/sbin/logrotate /etc/logrotate.conf
@reboot /opt/app/bin/start-workers
@daily /usr/bin/certbot renew --quiet
@hourly /opt/app/bin/flush-metrics
15 9-17 * * MON-FRI /opt/app/bin/sync-crm
0 0 1 * * /opt/app/bin/invoice-run --month last

# end of file
""",
    "k8s-cronjobs.txt": """# schedule from each CronJob in the cluster
reports-weekly	0 6 * * 1
cache-warm	*/10 6-22 * * *
db-vacuum	30 2 * * 6,0
token-rotate	0 0 1 */2 *
quarterly-close	0 18 L 3,6,9,12 *
bad-one	0 25 * * *
""",
    "quartz.properties": """org.quartz.job.cleanup.cron = 0 0/30 8-18 ? * MON-FRI
org.quartz.job.digest.cron = 0 0 7 ? * 2#1
org.quartz.job.archive.cron = 0 15 10 L * ?
org.quartz.job.newyear.cron = 0 0 0 1 1 ? 2027
org.quartz.job.broken.cron = 0 0 0 1 1
""",
}
for name, body in CRONTABS.items():
    write(f"crontabs/{name}", body)
for name, loc in [("web01.crontab", "en_US"), ("web01.crontab", "de_DE"), ("k8s-cronjobs.txt", "en_US"),
                  ("k8s-cronjobs.txt", "ja_JP"), ("quartz.properties", "en_US"), ("quartz.properties", "es_MX"),
                  ("missing.crontab", "en_US")]:
    jobs.append(["crontab", f"data/crontabs/{name}", loc])

with open(os.path.join(DATA, "jobs.jsonl"), "w", encoding="utf-8", newline="\n") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(jobs), "jobs")
