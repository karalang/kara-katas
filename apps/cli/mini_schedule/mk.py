# Writes data/: the jobs (data/jobs.jsonl), the daemon's config
# (data/daemon.conf) and a service's health over an afternoon
# (data/health.csv). Each job starts its own Scheduler with the clock at
# its "start" and random seeded with its "seed".
import json
import os

jobs = []


def job(name, ops, start="2026-10-21 09:15:27.250000", seed=1):
    jobs.append({"name": name, "start": start, "seed": seed, "ops": ops})


def every(label, chain, n=None, **kw):
    op = {"op": "every", "job": label, "chain": chain}
    if n is not None:
        op["n"] = n
    op.update(kw)
    return op


def do(fname, *args, **kwargs):
    d = {"do": fname}
    if args:
        d["args"] = list(args)
    if kwargs:
        d["kwargs"] = kwargs
    return d


def tick(s):
    return {"op": "tick", "s": s}


def at_clock(t):
    return {"op": "clock", "t": t}


JOBS = {"op": "jobs"}
IDLE = {"op": "idle"}

# 2026-10-21 is a Wednesday.
job("units", [
    every("j1", ["seconds", do("ping")], n=10),
    every("j2", ["minute", do("sync", "inbox")]),
    every("j3", ["hours", do("report", "hourly", fmt="csv")], n=2),
    every("j4", ["day", {"at": "10:30"}, do("backup", "db")]),
    every("j5", ["days", {"at": "08:00:15"}, do("vacuum")], n=3),
    every("j6", ["week", do("digest")]),
    every("j7", ["monday", do("standup")]),
    every("j8", ["wednesday", {"at": "09:00"}, do("review")]),
    every("j9", ["wednesday", {"at": "13:45"}, do("demo")]),
    every("j10", ["sunday", {"at": "23:59:59"}, do("rollover")]),
    every("j11", ["weeks", do("audit")], n=2),
    JOBS,
    {"op": "next_run"},
    IDLE,
    tick(9.75),
    tick(0.25),
    tick(50),
    tick(10),
    IDLE,
    at_clock("2026-10-21 10:30:00"),
    at_clock("2026-10-21 11:15:27.25"),
    at_clock("2026-10-21 13:45:00"),
    JOBS,
])

job("intervals", [
    every("a", ["minute", do("x")], n=2),
    every("b", ["second", do("x")], n=5),
    every("c", ["hour", do("x")], n=0.5),
    every("d", ["day", do("x")], n=7),
    every("e", ["week", do("x")], n=3),
    every("f", ["monday", do("x")], n=2),
    every("g", ["sunday", {"at": "10:00"}], n=4),
    every("h", ["minute", do("one_float")], n=1.0),
    every("i", ["hour", do("one_bool")], n=True),
    every("k", ["minutes", do("ninety_s")], n=1.5),
    every("l", ["seconds", do("quarter")], n=0.25),
    every("m", ["hours", do("tiny")], n=0.0001),
    every("n", ["minutes", do("text")], n="5"),
    every("o", ["minute"], n="5"),
    every("p", [do("nounit")], n=3),
    every("q", [], n=3),
    every("r", []),
    every("s", ["minutes"], n=2),
    {"op": "str", "job": "q"},
    {"op": "str", "job": "r"},
    {"op": "str", "job": "s"},
    {"op": "str", "job": "n"},
    {"op": "should_run", "job": "q"},
    {"op": "should_run", "job": "h"},
    JOBS,
    tick(0.25),
    tick(0.5),
    tick(59.25),
    tick(30),
    JOBS,
])

job("at_daily", [
    every("d1", ["day", {"at": "10:30"}, do("t")]),
    every("d2", ["day", {"at": "1030"}, do("t")]),
    every("d3", ["day", {"at": "24:00"}, do("t")]),
    every("d4", ["day", {"at": "29:59:59"}, do("t")]),
    every("d5", ["day", {"at": "10:60"}, do("t")]),
    every("d6", ["day", {"at": "10:30:60"}, do("t")]),
    every("d7", ["day", {"at": "7:30"}, do("t")]),
    every("d8", ["day", {"at": "07:30\n"}, do("newline")]),
    every("d9", ["day", {"at": "09:15:27"}, do("this_second")]),
    every("d10", ["day", {"at": "09:15:28"}, do("next_second")]),
    every("d11", ["day", {"at": "1０:3０"}, do("fullwidth")]),
    every("d12", ["day", {"at": "١٢:٠٥"}, do("arabic_indic")]),
    every("d13", ["day", {"at": "10:30 "}, do("t")]),
    every("d14", ["day", {"at": " 10:30"}, do("t")]),
    every("d15", ["day", {"at": 1030}, do("t")]),
    every("d16", ["day", {"at": "10:30", "tz": "Europe/Berlin"}, do("t")]),
    every("d17", ["day", {"at": "10:30", "tz": 5}, do("t")]),
    every("d18", ["days", {"at": "06:00"}, do("every_other")], n=2),
    every("d19", ["days", {"at": "23:00"}, do("every_other_late")], n=2),
    every("d20", ["day", {"at": "00:00"}, do("midnight")]),
    every("d21", ["day", {"at": "23:59:59"}, do("last_second")]),
    every("d22", ["day", {"at": "10:30"}, {"at": "11:45"}, do("twice_at")]),
    JOBS,
    tick(1),
    at_clock("2026-10-22 00:00:00"),
    at_clock("2026-10-22 09:30:00"),
    JOBS,
])

job("at_hourly_minutely", [
    every("h1", ["hour", {"at": ":30"}, do("half_past")]),
    every("h2", ["hour", {"at": "15:30"}, do("m15s30")]),
    every("h3", ["hour", {"at": "15"}, do("t")]),
    every("h4", ["hour", {"at": "5:30"}, do("t")]),
    every("h5", ["hour", {"at": "60:00"}, do("t")]),
    every("h6", ["hours", {"at": ":00"}, do("on_the_hour")], n=3),
    every("h7", ["hour", {"at": "15:27"}, do("this_minute")]),
    every("m1", ["minute", {"at": ":15"}, do("sec15")]),
    every("m2", ["minute", {"at": "00:15"}, do("t")]),
    every("m3", ["minutes", {"at": ":45"}, do("every5_at45")], n=5),
    every("m4", ["minute", {"at": ":27"}, do("now_second")]),
    every("s1", ["second", {"at": ":15"}, do("t")]),
    every("s2", ["week", {"at": "10:00"}, do("t")]),
    every("s3", ["weeks", {"at": "10:00", "tz": "UTC"}, do("t")], n=2),
    every("s4", ["monday", {"at": "25:00"}, do("t")]),
    every("s5", ["monday", {"at": ":30"}, do("t")]),
    every("s6", [{"at": "10:00"}, do("t")]),
    JOBS,
    tick(32.75),
    tick(60),
    at_clock("2026-10-21 09:30:00"),
    at_clock("2026-10-21 10:15:30"),
    at_clock("2026-10-21 12:00:00"),
    JOBS,
])

job("random_to", [
    every("r1", [{"to": 10}, "minutes", do("jitter")], n=5),
    every("r2", [{"to": 3}, "hours", do("hourly_jitter")], n=1),
    every("r3", ["seconds", {"to": 30}, do("sec_jitter")], n=10),
    every("r4", [{"to": 5}, "minutes", do("t")], n=10),
    every("r5", [{"to": 3}, "minutes", do("t")], n=1.5),
    every("r6", [{"to": 2.5}, "minutes", do("t")], n=2),
    every("r7", [{"to": 4}, "minutes", do("t")], n=2.0),
    every("r8", [{"to": 1}, "minute", do("same")], n=1),
    every("r9", [{"to": 3}, "day", {"at": "12:00"}, do("noonish")], n=1),
    every("r10", [{"to": 3}, "minutes", do("bool_low")], n=True),
    every("r11", [{"to": 2}, "minutes"], n=1),
    {"op": "str", "job": "r11"},
    JOBS,
    tick(300),
    tick(300),
    tick(300),
    tick(600),
    tick(1800),
    JOBS,
], seed=42)

job("random_seeds", [
    every("x", [{"to": 1000}, "seconds", do("wide")], n=1),
    tick(1000), tick(1000), tick(1000), tick(1000),
    JOBS,
], seed=2026)

job("until", [
    every("u1", ["minutes", {"until": "2026-10-21 09:30:00"}, do("t1")], n=5),
    every("u2", ["minutes", {"until": "2026-10-21 09:40"}, do("t2")], n=5),
    every("u3", ["hours", {"until": "2026-10-22"}, do("t3")], n=6),
    every("u4", ["minutes", {"until": "09:31:00"}, do("t4")], n=10),
    every("u5", ["minutes", {"until": "10:00"}, do("t5")], n=10),
    every("u6", ["minutes", {"until": "08:00"}, do("t")], n=10),
    every("u7", ["minutes", {"until": "2026-02-30"}, do("t")], n=10),
    every("u8", ["minutes", {"until": "2026-10-23 18:00:61"}, do("t")], n=10),
    every("u9", ["minutes", {"until": "2026-10-23 18:00:7"}, do("t9")], n=10),
    every("u10", ["minutes", {"until": "tomorrow"}, do("t")], n=10),
    every("u11", ["minutes", {"until": "2026-1-5"}, do("t")], n=10),
    every("u12", ["minutes", {"until": "2026-10-23   18:00"}, do("t12")], n=10),
    every("u13", ["minutes", {"until": "2026-10- 9"}, do("t")], n=10),
    every("u14", ["minutes", {"until": "2026-11- 9 9:5"}, do("t14")], n=10),
    every("u15", ["minutes", {"until": "2026-10-23 18:00 "}, do("t")], n=10),
    every("u16", ["minutes", {"until": "２０２６-10-23"}, do("t16")], n=10),
    every("u17", ["minutes", {"until": {"dt": "2026-10-21 09:45:00"}}, do("t17")], n=10),
    every("u18", ["minutes", {"until": {"td": 1800.5}}, do("t18")], n=10),
    every("u19", ["minutes", {"until": {"time": "09:50:30"}}, do("t19")], n=10),
    every("u20", ["minutes", {"until": {"time": "09:00:00"}}, do("t")], n=10),
    every("u21", ["minutes", {"until": 3600}, do("t")], n=10),
    every("u22", ["minutes", {"until": "2026-10-21 09:15:27"}, do("t")], n=10),
    every("u23", ["minutes", {"until": {"td": 0}}, do("t")], n=10),
    every("u24", ["minutes", {"until": "2026-10-21 9:20"}, do("t24")], n=1),
    every("u25", ["minutes", {"until": "2026-10-21 09:35"}, do("t25")], n=20),
    JOBS,
    tick(300),
    tick(300),
    tick(300),
    tick(300),
    tick(600),
    tick(1200),
    JOBS,
    {"op": "run_all"},
    JOBS,
    at_clock("2026-10-22 12:00:00"),
    JOBS,
])

job("tags", [
    every("t1", ["minutes", {"tag": ["db", "nightly"]}, do("a")], n=5),
    every("t2", ["minutes", {"tag": [1]}, do("b")], n=7),
    every("t3", ["minutes", {"tag": [True, "db"]}, do("c")], n=9),
    every("t4", ["minutes", {"tag": [1.0, "1"]}, do("d")], n=11),
    every("t5", ["minutes", {"tag": [["x"]]}, do("e")], n=13),
    every("t6", ["minutes", {"tag": ["web", {"k": 1}]}, do("f")], n=15),
    every("t7", ["minutes", {"tag": []}, {"tag": ["web"]}, {"tag": ["web", None]}, do("g")], n=17),
    every("t8", [{"tag": ["early"]}, "minutes", do("h")], n=19),
    {"op": "str", "job": "t5"},
    {"op": "tags", "job": "t1"},
    {"op": "tags", "job": "t3"},
    {"op": "tags", "job": "t4"},
    {"op": "tags", "job": "t7"},
    {"op": "get_jobs", "tag": "db"},
    {"op": "get_jobs", "tag": 1},
    {"op": "get_jobs", "tag": True},
    {"op": "get_jobs", "tag": 1.0},
    {"op": "get_jobs", "tag": "1"},
    {"op": "get_jobs", "tag": None},
    {"op": "get_jobs", "tag": "nope"},
    {"op": "get_jobs"},
    {"op": "next_run", "tag": "db"},
    {"op": "next_run", "tag": "web"},
    {"op": "next_run", "tag": "nope"},
    {"op": "clear", "tag": 1.0},
    {"op": "get_jobs"},
    {"op": "clear", "tag": "db"},
    {"op": "get_jobs"},
    {"op": "clear", "tag": "nope"},
    {"op": "clear"},
    {"op": "get_jobs"},
    {"op": "next_run"},
    IDLE,
    tick(60),
])

job("returns", [
    every("o1", ["minute", do("once")]),
    every("o2", ["minute", do("once_obj")]),
    every("l1", ["minutes", do("limited", times=3)], n=2),
    every("v1", ["minute", do("returns", 42)]),
    every("v2", ["minute", do("returns", "CancelJob")]),
    JOBS,
    tick(60),
    JOBS,
    tick(60),
    tick(60),
    tick(60),
    tick(120),
    JOBS,
    {"op": "cancel", "job": "o1"},
    {"op": "cancel", "job": "v1"},
    {"op": "cancel", "job": "v1"},
    JOBS,
])

job("failures", [
    every("f1", ["minute", do("ping", "a")]),
    every("f2", ["seconds", do("boom", "disk full")], n=30),
    every("f3", ["minutes", do("ping", "c")], n=2),
    tick(30),
    tick(30),
    JOBS,
    tick(1),
    {"op": "cancel", "job": "f2"},
    tick(60),
    JOBS,
    every("f4", ["minute", do("boom", "")]),
    tick(60),
    every("f5", ["minute", do("boom_type")]),
    {"op": "clear"},
    every("f6", ["minute", do("boom_type")]),
    tick(60),
])

job("slow_jobs", [
    every("w1", ["minute", do("slow", 90)]),
    every("w2", ["minute", do("ping", "after")]),
    every("w3", ["minutes", do("slow", 0.5)], n=3),
    tick(60),
    JOBS,
    IDLE,
    tick(30),
    tick(60),
    JOBS,
    {"op": "run_all", "delay": 5},
    JOBS,
    {"op": "run_all", "delay": 2.5},
    {"op": "last_run", "job": "w1"},
    {"op": "last_run", "job": "w2"},
])

job("run_all", [
    {"op": "run_all", "delay": 3},
    every("a1", ["hour", do("ping", "a1")]),
    every("a2", ["day", {"at": "18:00"}, do("ping", "a2")]),
    every("a3", ["minutes", {"until": "2026-10-21 09:20"}, do("ping", "a3")], n=3),
    every("a4", ["minute", do("once")]),
    {"op": "run_all", "delay": 60},
    JOBS,
    {"op": "run_all"},
    JOBS,
    {"op": "run_all", "delay": 0.75},
    JOBS,
])

job("inside_jobs", [
    every("c1", ["minute", do("ping", "c1")]),
    every("c2", ["minute", do("clear_all")]),
    every("c3", ["minute", do("ping", "c3")]),
    every("c4", ["minute", do("once")]),
    tick(60),
    JOBS,
    every("s1", ["minutes", do("spawn", 15, "child")], n=1),
    every("s2", ["minutes", {"tag": ["keep"]}, do("ping", "s2")], n=2),
    tick(60),
    JOBS,
    tick(15),
    tick(45),
    JOBS,
    every("x1", ["seconds", {"tag": ["spawned"]}, do("clear_tag", "spawned")], n=20),
    tick(20),
    JOBS,
])

job("clock_moves", [
    every("k1", ["day", {"at": "06:00"}, do("daily")]),
    every("k2", ["minutes", do("tick15")], n=15),
    every("k3", ["hours", do("every4h")], n=4),
    at_clock("2026-10-24 12:00:00"),
    JOBS,
    at_clock("2026-10-24 11:00:00"),
    {"op": "should_run", "job": "k2"},
    IDLE,
    at_clock("2026-10-24 12:16:00"),
    JOBS,
    at_clock("2026-10-25 05:59:59.999999"),
    IDLE,
    tick(0.000001),
    JOBS,
    at_clock("2026-12-31 23:59:59"),
    JOBS,
])

job("weekdays", [
    every("w0", ["monday", {"at": "09:00"}, do("mon")]),
    every("w1", ["tuesday", do("tue")]),
    every("w2", ["wednesday", do("wed_now")]),
    every("w3", ["wednesday", {"at": "09:15:27"}, do("wed_this_second")]),
    every("w4", ["thursday", {"at": "00:00"}, do("thu")]),
    every("w5", ["friday", {"at": "17:30:45"}, do("fri")]),
    every("w6", ["saturday", {"at": "10:00"}, do("sat")]),
    every("w7", ["sunday", do("sun")]),
    every("w8", ["monday", "tuesday", do("both_days")]),
    every("w9", ["friday", "day", do("fri_then_day")]),
    every("w10", ["day", "friday", {"at": "08:00"}, do("day_then_fri")]),
    every("w11", ["wednesday", "hours", {"at": ":30"}, do("wed_hours")]),
    JOBS,
    at_clock("2026-10-23 17:30:45"),
    at_clock("2026-10-26 09:00:00"),
    at_clock("2026-11-02 10:00:00"),
    JOBS,
], start="2026-10-21 09:15:27.250000")

job("weekdays_sunday_start", [
    every("w0", ["monday", {"at": "09:00"}, do("mon")]),
    every("w6", ["saturday", {"at": "23:00"}, do("sat")]),
    every("w7", ["sunday", {"at": "07:00"}, do("sun_morning")]),
    every("w8", ["sunday", {"at": "21:00"}, do("sun_evening")]),
    JOBS,
    at_clock("2026-11-01 21:00:00"),
    JOBS,
], start="2026-11-01 08:00:00")

job("detached", [
    {"op": "detached", "job": "d1", "chain": ["minutes", do("lonely")], "n": 5},
    {"op": "str", "job": "d1"},
    {"op": "should_run", "job": "d1"},
    {"op": "detached", "job": "d2", "chain": ["minute"]},
    {"op": "str", "job": "d2"},
    {"op": "should_run", "job": "d2"},
    {"op": "cancel", "job": "d1"},
    JOBS,
])

job("arg_reprs", [
    every("p1", ["minute", do("echo", "it's", 'say "hi"', "both ' and \"", "tab\there", "back\\slash")]),
    every("p2", ["minute", do("echo", 1, -2.5, 1e100, 1e-07, 0.1, True, False, None)]),
    every("p3", ["minute", do("echo", [1, "a", [None]], {"k": [1.5]}, {})]),
    every("p4", ["minute", do("echo", name="café", n=0, flag=None)]),
    every("p5", ["minute", do("echo", "é中\U0001f600", "\x7f\x01", "​", " ")]),
    every("p6", ["minute", do("echo", 12345678901234567890, -0.0, 100.0, 1.5e16)]),
    JOBS,
    {"op": "str", "job": "p1"},
    {"op": "str", "job": "p2"},
    {"op": "str", "job": "p3"},
    {"op": "str", "job": "p4"},
    {"op": "str", "job": "p5"},
    {"op": "str", "job": "p6"},
    tick(60),
])

job("sort_order", [
    every("e1", ["minutes", do("ping", "e1")], n=3),
    every("e2", ["minute", do("ping", "e2")]),
    every("e3", ["minutes", do("ping", "e3")], n=2),
    every("e4", ["seconds", do("ping", "e4")], n=90),
    every("e5", ["minute", do("ping", "e5")]),
    at_clock("2026-10-21 09:25:00"),
    JOBS,
    {"op": "next_run"},
    tick(30),
    tick(30),
])

job("daemon", [
    {"op": "daemon", "conf": "daemon.conf", "until": "2026-10-23 12:00:00"},
], start="2026-10-21 08:59:30")

job("monitor", [
    {"op": "monitor", "csv": "health.csv", "until": "2026-10-21 17:00:00"},
], start="2026-10-21 13:00:00")

DAEMON_CONF = """\
# ops daemon tasks: every [N [to M]] UNIT [at T] [until DATE_TIME] do TASK ARGS...
# key=value args are keyword arguments, #name is a tag, !cancel cancels a
# task when it fails (otherwise a failure is logged and it runs again).

every 15 minutes do rotate_logs /var/log/app.log keep=5 #maint
every day at 02:30 do backup db #maint #nightly
every day at 02:30 do backup media #nightly !cancel
every 10 to 20 minutes do poll_feed https://status.example.com/feed.xml #net
every monday at 09:00 do weekly_report team=ops
every wednesday at 17:00 do weekly_report team=web
every hour at :05 do healthcheck api
every 6 hours until 2026-10-22_06:00 do refresh_certs #maint
every 90 seconds do heartbeat !cancel
every 2 days at 23:45:10 do compact_db shards=4
every hour at 30 do healthcheck web
every 5 fortnights do nothing
every day at 25:00 do backup oops
every minute do no_such_task
every x minutes do heartbeat
every 2 minute do heartbeat
every 3 to 1 hours do poll_feed http://x
every day at 07:00 do backup logs until 2026-10-20_00:00
every 1 to 3 days do send_digest #mail
every
"""

HEALTH = """\
seconds,status
0,up
1200,up
1830,down
2100,down
2400,degraded
2700,down
3000,up
6000,down
6020,up
9000,down
12000,up
"""

os.makedirs("data", exist_ok=True)
with open("data/jobs.jsonl", "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
with open("data/daemon.conf", "w") as f:
    f.write(DAEMON_CONF)
with open("data/health.csv", "w") as f:
    f.write(HEALTH)
print(len(jobs), "jobs,", sum(len(j["ops"]) for j in jobs), "operations")
