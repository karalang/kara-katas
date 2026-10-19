# Writes data/jobs.tsv, the operations oracle.py and mini_isodate.kara
# run, and the two files the reports read: data/subscriptions.tsv and
# data/incidents.tsv.
#
# A line of jobs.tsv is an operation and its arguments, separated by tabs;
# "== name" starts a job. A value argument is "d:" (a date), "t:" (a
# time), "dt:" (a datetime) or "p:" (a duration, as parse_duration gives
# it) or "P:" (a duration that stays a Duration) before an ISO string.
# \t, \n and \\ are escaped.
import os
import random

rng = random.Random(126)
lines = []


def job(name):
    lines.append("== " + name)


def esc(s):
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


def op(*args):
    lines.append("\t".join(esc(str(a)) for a in args))


# ---------------------------------------------------------------- dates
job("dates")
for s in ["2024-02-29", "20240229", "2023-02-29", "2024-13-01", "2024-00-10",
          "1985-W15-5", "1985W155", "2009-W01-1", "2009-W53-7", "2010-W01",
          "2010W01", "2008-W52-0", "2004-W53-9", "1985-102", "1985102",
          "2024-366", "2023-366", "1985-04", "198504", "1985", "19", "20",
          "2000-02", "0000-01-01", "0001-01-01", "9999-12-31", "10000",
          "+1985-04-12", "1985-4-12", "1985-04-12 ", " 1985-04-12",
          "1985-04-12\n", "", "abcd", "2024-02-30", "2024-W60-1", "2024-000"]:
    op("date", s)
for s, yd, ex in [("+001985-04-12", 6, 1), ("+0019850412", 6, 1),
                  ("-001985-04-12", 6, 1), ("+1985-04-12", 4, 1),
                  ("-1985-04-12", 4, 1), ("1985-04-12", 4, 1),
                  ("+001985-W15-5", 6, 1), ("+001985102", 6, 1),
                  ("+0019", 6, 1), ("+19", 4, 1), ("+001985", 6, 1),
                  ("+012345-06-07", 6, 0), ("+12345-06-07", 5, 0),
                  ("+0000-01-01", 4, 1)]:
    op("date", s, yd, ex)
for s, m, d in [("1985", 6, 15), ("19", 12, 31), ("1985-04", 1, 30),
                ("2023", 2, 29), ("1985-04", 4, 31)]:
    op("date", s, 4, 0, m, d)
for d in ["2024-02-29", "1985-04-12", "2009-12-31", "2010-01-03", "0001-01-01",
          "2008-12-29", "1999-01-01"]:
    for fmt in ["%Y-%m-%d", "%Y%m%d", "%Y-W%W-%w", "%YW%W%w", "%Y-%j", "%Y%j",
                "%Y-W%W", "%Y-%m", "%Y", "%C", "%d.%m.%Y %%", "%H"]:
        op("date_fmt", d, fmt)
    op("date_fmt", d, "%Y-%m-%d", 6)
    op("date_fmt", d, "%C", 6)

# ---------------------------------------------------------------- times
job("times")
for s in ["23:20:50", "232050", "23:20", "2320", "23", "23:20:50.5",
          "23:20:50,5", "232050.5", "23:20.5", "2320,8", "23.3", "23,3",
          "12.33333333", "00:00:00.1234567", "15:27:46.123456789",
          "10:00:00.000001", "11:59:59.9999999", "T23:20:50", "T2320",
          "23:20:50Z", "23:20:50+01:00", "232050+0100", "23:20:50-05",
          "23:20:50-05:30", "23:20:50+00:00", "23:20:50-00:00", "152746+0100",
          "23:20:50.5+01:00", "23:20.25-0800", "24:00:00", "23:60:00",
          "23:59:60", "25", "1:2:3", "23:20:50 ", "23:20:50+1", "23:20:50+01:",
          "23:20:50+99:00", "23:20:50z", "", "T", "07:15.123456789012"]:
    op("time", s)
for t in ["23:20:50.5+01:00", "08:05:09Z", "12:00", "152746-0530", "00:00:00.000123"]:
    for fmt in ["%H:%M:%S", "%H%M%S", "%H:%M", "%H%M", "%H", "%H:%M:%S%Z",
                "%H%M%S%z", "%H%h", "%H:%M:%S.%f", "%Y"]:
        op("time_fmt", t, fmt)

# ---------------------------------------------------------------- zones
job("zones")
for s in ["Z", "+01:00", "+0100", "+01", "-05:30", "-0530", "-00:30",
          "+00:00", "-00", "", "+1", "x", "+01:00x", "z", "+14:00"]:
    op("tz", s)

# ---------------------------------------------------------------- datetimes
job("datetimes")
for s in ["1985-04-12T10:15:30", "19850412T101530", "1985-04-12T10:15:30Z",
          "1985-04-12T10:15:30+04:00", "1985-W15-5T10:15", "1985102T23:50:30",
          "1985-04T10:15", "1985-04-12T10:15:30.5+01:00", "2012-10-30T08:55:22.7-05:00",
          "1985-04-12", "1985-04-12T", "T10:15:30", "1985-04-12T10:15:30T",
          "1985-04-12 10:15:30", "2024-02-30T10:00", "2024-02-29T24:00",
          "2014-11-02T01:30:00-04:00", "1997-07-16T19:20+01:00", "1997-07-16t19:20"]:
    op("datetime", s)
for s in ["1985-04-12T10:15:30Z", "2012-10-30T08:55:22.7-05:00",
          "2009-12-31T23:59:59+05:45", "1985-04-12T10:15:30"]:
    for fmt in ["%Y-%m-%dT%H:%M:%S%Z", "%Y%m%dT%H%M%S%z", "%Y-%jT%H:%M:%S%Z",
                "%Y%jT%H%M%S%z", "%Y-W%W-%wT%H:%M:%S%Z", "%YW%W%wT%H%M%S%z",
                "%Y-%m-%dT%H:%M:%S.%f%h", "%d/%m/%Y %H:%M"]:
        op("datetime_fmt", s, fmt)

# ---------------------------------------------------------------- durations
job("durations")
durs = ["P18Y9M4DT11H9M8S", "P2W", "P3Y6M4DT12H30M5S", "P23DT23H", "P4Y",
        "PT36H", "P1DT12H", "PT0.5S", "PT0,5S", "P0.5Y", "P0,5Y", "P1.5M",
        "P0.5W", "P1.5D", "PT1.5H", "PT1.5M", "P1M", "-P1M", "-P2W", "-PT1S",
        "+P1D", "P0D", "PT0S", "P0Y", "P", "PT", "P1", "1Y", "P1Y2", "P1D2H",
        "P1DT", "PT1H2", "P1W2D", "PT1000000S", "P10000D", "PT0.0000001S",
        "PT0.0000005S", "PT0.0000015S", "PT1.0000005S", "P0.000001D",
        "PT0.1H", "P1.333333333333333D", "P0.00001Y", "P0.0000001Y",
        "P1.50Y", "P007Y0010M", "P0.0M", "-P0.0Y", "P1YT", "P1y",
        "P0003-02-01T04:05:06", "P00030201T040506", "P0000-00-01T00:00:00",
        "P0003-032T04:05:06", "P0001-01-01T00:00:00.5", "P0002-02-30T00:00",
        "P0018-09-04T11:09:08", "P1985-W15-5T10:15", "Pfoo", "", "PT36H1D",
        "P1DT-1H", "p1d", "P1D ", "P1.D", "P.5D", "P1e3D"]
for s in durs:
    op("duration", s)
    op("duration", s, "no")
for s in ["P3Y6M4DT12H30M5S", "PT36H", "-P1M", "P2W", "-PT1.5S", "P0D",
          "PT0.000001S", "P1.5Y", "-P1Y1DT1S", "P0.0000001Y", "P400D", "-P10D"]:
    for fmt in ["P%P", "P%p", "P%Y-%m-%dT%H:%M:%S", "P%Y%m%dT%H%M%S",
                "%d %H %M %S %f", "%W %%", "%C"]:
        op("duration_fmt", s, fmt)
        op("duration_fmt", s, fmt, "no")

# ---------------------------------------------------------------- arithmetic
job("arithmetic")
for d, x in [("P1M", "d:2024-01-31"), ("P1M", "d:2023-01-31"), ("P1Y", "d:2024-02-29"),
             ("P1Y1M", "dt:2024-01-31T10:00:00Z"), ("P13M", "d:2024-12-15"),
             ("-P1M", "d:2024-03-31"), ("P1MT12H", "d:2024-01-31"),
             ("P1MT12H", "dt:2024-01-31T18:00"), ("P0.5M", "d:2024-01-01"),
             ("P1.0M", "d:2024-01-31"), ("PT36H", "d:2024-01-01"),
             ("PT36H", "dt:2024-01-01T00:00+05:30"), ("P1M", "P:P1D"),
             ("P1M", "p:PT1H"), ("P9000Y", "d:2024-01-01"), ("-P2025Y", "d:2024-01-01"),
             ("P2Y", "d:9998-06-01"), ("P1D", "d:9999-12-31"), ("P100Y", "dt:1999-12-31T23:59:59.5")]:
    op("add", "P:" + d, x)
    op("add", x, "P:" + d)
for x, d in [("d:2024-03-31", "P1M"), ("d:2024-03-31", "P1Y1M"), ("d:2024-01-15", "P1M"),
             ("dt:2024-03-31T12:00", "P1MT12H"), ("d:2024-03-01", "PT1H"),
             ("d:2024-03-01", "P1D"), ("p:PT1H", "P1M"), ("P:P1Y", "P1M"),
             ("d:2024-01-31", "P0.5M"), ("d:0001-03-01", "P1Y")]:
    op("sub", x, "P:" + d)
op("sub", "P:P1M", "d:2024-01-01")
for d, n in [("P1M", 3), ("P1Y2M3DT4H", 2), ("P1.5Y", 2), ("-P1M", 4), ("P1M", 0), ("PT1S", -3)]:
    op("mul", "P:" + d, n)
for d in ["P1Y2M", "-P1M", "PT1H", "P1.5Y"]:
    op("neg", "P:" + d)
for a, b in [("P:P1Y", "P:P12M"), ("P:P1Y", "P:P365D"), ("P:P1D", "p:PT24H"),
             ("P:P0Y", "p:P1D"), ("P:P0YT1D", "p:P1D"), ("P:P1M", "P:P1M"),
             ("P:P1.5Y", "P:P18M"), ("P:P2W", "P:P14D")]:
    op("eq", a, b)
for d, which, x in [("P1M", "start", "d:2024-01-31"), ("P1M", "start", "d:2024-02-01"),
                    ("P1M", "end", "d:2024-03-31"), ("P1Y", "start", "dt:2024-02-29T00:00"),
                    ("P1Y", "end", "d:2025-02-28"), ("P1M", "none", "d:2024-01-01"),
                    ("P1M", "both", "d:2024-01-01"), ("P0.5Y", "start", "d:2024-01-01")]:
    op("totd", "P:" + d, which, x)
for k in range(30):
    y, m = rng.randrange(1, 4), rng.randrange(0, 14)
    dd = rng.randrange(0, 40)
    sign = rng.choice(["", "-"])
    start = f"d:{rng.randrange(1990, 2030):04d}-{rng.randrange(1, 13):02d}-{rng.randrange(1, 29):02d}"
    op("add", f"P:{sign}P{y}Y{m}M{dd}D", start)

# ---------------------------------------------------------------- reports
job("subscriptions")
op("subscriptions", "subscriptions.tsv")
job("incidents")
op("incidents", "incidents.tsv")

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

SUBS = """# id\tstarts\tperiod\trenewals\tgrace\tplan
acme-pro\t2024-01-31\tP1M\t6\tP3D\tmonthly, billed on the last day the month allows
globex\t2023-11-30T09:00:00Z\tP1M\t4\tPT36H\tmonthly from a datetime
initech\t2024-02-29\tP1Y\t5\tP14D\tyearly from a leap day
hooli\t2024-03-15T12:00:00+05:30\tP3M\t5\tP1W\tquarterly
umbrella\t2024-01-01\tP2W\t6\tP2D\tfortnightly
stark\t2024-05-31\tP1M15D\t4\tP0D\ta month and a half
wayne\t2024-08-31\tP6M\t3\tPT12H\thalf-yearly
tyrell\t2024-01-15\tP1.5M\t2\tP1D\tfractional months are refused
cyberdyne\t2024-12-31T23:30:00-08:00\tP1MT1H\t3\tPT30M\tmonthly plus an hour
soylent\t2024-06-30\tP1Y2M\t3\tP0D\tfourteen months
oscorp\t2025-01-31\tPT720H\t3\tP1D\tthirty days, as hours
nakatomi\t2024-04-31\tP1M\t2\tP1D\tbad start
"""
with open("data/subscriptions.tsv", "w", encoding="utf-8") as f:
    f.write(SUBS)

INC = """# service\tstarted\tresolved\tbudget\tnote
api\t2024-03-10T01:59:30-05:00\t2024-03-10T03:01:15-04:00\tPT45M\tacross the DST change, written with offsets
api\t2024-03-12T14:00:00Z\t2024-03-12T14:07:30.250Z\tPT45M\tshort blip
api\t20240315T220000+0100\t20240316T003000+0100\tPT45M\tbasic format
db\t2024-03-01T23:50:00+00:00\t2024-03-02T00:20:00+00:00\tPT1H\tacross midnight
db\t2024-W10-3T08:00:00Z\t2024-W10-3T09:15:00Z\tPT1H\tweek dates
db\t2024-068T10:00:00Z\t2024-068T10:42:00.5Z\tPT1H\tordinal dates
web\t2024-03-05T10:00\t2024-03-05T10:30\tPT20M\tlocal times
web\t2024-03-05T10:00Z\t2024-03-05T10:30\tPT20M\tnaive and aware
web\t2024-03-07T09:00:00+02:00\t2024-03-07T08:59:00+01:00\tPT20M\tresolved in another zone
web\t2024-03-08T12:00:00Z\t2024-03-08T11:00:00Z\tPT20M\tresolved before it started
queue\t2024-03-20T06:00:00.123456Z\t2024-03-21T07:30:00.654321Z\tP1D\tlong outage
queue\t2024-03-22T06:00Z\tnot-a-time\tP1D\tbad resolved time
queue\t2024-03-23T06:00Z\t2024-03-23T07:00Z\tPT1X\tbad budget
"""
with open("data/incidents.tsv", "w", encoding="utf-8") as f:
    f.write(INC)
