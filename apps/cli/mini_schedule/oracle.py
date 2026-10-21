# Runs data/jobs.jsonl through schedule 1.2.2 itself (the copy in
# schedule/, unchanged) and prints what mini_schedule.kara must print.
# The clock is fake: datetime.datetime.now() reads it, time.sleep()
# moves it on, and so does each tick of a job.
import datetime as _dt
import functools
import importlib.abc
import json
import logging
import os
import random
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


class NoPytz(importlib.abc.MetaPathFinder):
    # As on a machine without pytz.
    def find_spec(self, name, path, target=None):
        if name == "pytz" or name.startswith("pytz."):
            raise ModuleNotFoundError("No module named %r" % name, name=name)
        return None


sys.meta_path.insert(0, NoPytz())

import schedule  # noqa: E402

NOW = [None]


class FakeDT(_dt.datetime):
    @classmethod
    def now(cls, tz=None):
        n = NOW[0]
        return cls(n.year, n.month, n.day, n.hour, n.minute, n.second, n.microsecond)


def to_fake(d):
    return FakeDT(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)


def advance(seconds):
    NOW[0] = to_fake(NOW[0] + _dt.timedelta(seconds=seconds))


schedule.datetime = types.SimpleNamespace(
    datetime=FakeDT, timedelta=_dt.timedelta, time=_dt.time)
schedule.time = types.SimpleNamespace(sleep=advance)

OUT = []


def out(s=""):
    OUT.append(s)


class Capture(logging.Handler):
    def emit(self, record):
        out("  log: " + record.getMessage())


log = logging.getLogger("schedule")
log.setLevel(logging.DEBUG)
log.addHandler(Capture())
log.propagate = False


def fail(e):
    return "%s: %s" % (type(e).__name__, e)


def parse_dt(s):
    return to_fake(_dt.datetime.fromisoformat(s))


class Run:
    def __init__(self, spec):
        self.sched = schedule.Scheduler()
        self.labels = {}
        self.children = 0
        NOW[0] = parse_dt(spec["start"])
        random.seed(spec["seed"])

    def label(self, job):
        for k, v in self.labels.items():
            if v is job:
                return k
        return "?"

    def show(self, job):
        try:
            return repr(job)
        except Exception as e:
            return "<repr raised %s>" % fail(e)

    # The job functions: what each one does is chosen by its name.
    def func(self, name):
        run = self
        state = {"count": 0}

        def f(*args, **kwargs):
            state["count"] += 1
            now = FakeDT.now()
            parts = [repr(a) for a in args] + ["%s=%r" % kv for kv in kwargs.items()]
            out("  run %s(%s) at %s" % (name, ", ".join(parts), now))
            if name == "once":
                return schedule.CancelJob
            if name == "once_obj":
                return schedule.CancelJob()
            if name == "limited":
                if state["count"] >= kwargs["times"]:
                    return schedule.CancelJob
                return None
            if name == "returns":
                return args[0]
            if name == "slow":
                advance(args[0])
                return None
            if name == "boom":
                raise RuntimeError(args[0])
            if name == "boom_type":
                raise TypeError("unsupported operand type(s) for +: 'int' and 'str'")
            if name == "clear_all":
                run.sched.clear()
                return None
            if name == "clear_tag":
                run.sched.clear(args[0])
                return None
            if name == "spawn":
                run.children += 1
                lab = "%s%d" % (args[1], run.children)
                child = run.sched.every(args[0]).seconds.do(run.func(lab))
                run.labels[lab] = child
                out("  spawned %s = %s" % (lab, run.show(child)))
                return None
            return None

        f.__name__ = name
        f.__qualname__ = name
        return f

    def until_arg(self, v):
        if isinstance(v, dict):
            if "dt" in v:
                return parse_dt(v["dt"])
            if "td" in v:
                return _dt.timedelta(seconds=v["td"])
            if "time" in v:
                return _dt.time.fromisoformat(v["time"])
        return v

    def chain(self, job, items):
        for item in items:
            if isinstance(item, str):
                job = getattr(job, item)
            elif "at" in item:
                if "tz" in item:
                    job = job.at(item["at"], item["tz"])
                else:
                    job = job.at(item["at"])
            elif "to" in item:
                job = job.to(item["to"])
            elif "tag" in item:
                job = job.tag(*item["tag"])
            elif "until" in item:
                job = job.until(self.until_arg(item["until"]))
            elif "do" in item:
                job = job.do(self.func(item["do"]), *item.get("args", []),
                             **item.get("kwargs", {}))
        return job

    def op_every(self, op, detached):
        lab = op["job"]
        if detached:
            job = schedule.Job(op["n"]) if "n" in op else schedule.Job(1)
        elif "n" in op:
            job = self.sched.every(op["n"])
        else:
            job = self.sched.every()
        self.labels[lab] = job
        try:
            self.chain(job, op["chain"])
        except Exception as e:
            out("%s: %s" % (lab, fail(e)))
            return
        out("%s = %s" % (lab, self.show(job)))

    def pending(self):
        try:
            self.sched.run_pending()
        except Exception as e:
            out("  error: " + fail(e))

    def op(self, op):
        kind = op["op"]
        if kind == "every":
            self.op_every(op, False)
        elif kind == "detached":
            self.op_every(op, True)
        elif kind == "tick":
            advance(op["s"])
            out("@ %s" % NOW[0])
            self.pending()
        elif kind == "clock":
            NOW[0] = parse_dt(op["t"])
            out("@ %s" % NOW[0])
            self.pending()
        elif kind == "jobs":
            out("jobs at %s:" % NOW[0])
            for j in self.sched.jobs:
                out("  %s: %s" % (self.label(j), self.show(j)))
        elif kind == "str":
            out("str %s: %s" % (op["job"], self.labels[op["job"]]))
        elif kind == "tags":
            j = self.labels[op["job"]]
            out("tags %s: [%s]" % (op["job"], ", ".join(sorted(repr(t) for t in j.tags))))
        elif kind == "should_run":
            try:
                v = self.labels[op["job"]].should_run
                out("should_run %s: %s" % (op["job"], v))
            except Exception as e:
                out("should_run %s: %s" % (op["job"], fail(e)))
        elif kind == "last_run":
            out("last_run %s: %s" % (op["job"], self.labels[op["job"]].last_run))
        elif kind == "get_jobs":
            if "tag" in op:
                js = self.sched.get_jobs(op["tag"])
                what = repr(op["tag"])
            else:
                js = self.sched.get_jobs()
                what = "(all)"
            out("get_jobs %s: [%s]" % (what, ", ".join(self.label(j) for j in js)))
        elif kind == "next_run":
            if "tag" in op:
                out("next_run %r: %s" % (op["tag"], self.sched.get_next_run(op["tag"])))
            else:
                out("next_run: %s" % self.sched.next_run)
        elif kind == "idle":
            out("idle_seconds: %r" % self.sched.idle_seconds)
        elif kind == "clear":
            if "tag" in op:
                out("clear %r" % op["tag"])
                self.sched.clear(op["tag"])
            else:
                out("clear")
                self.sched.clear()
        elif kind == "cancel":
            out("cancel %s" % op["job"])
            self.sched.cancel_job(self.labels[op["job"]])
        elif kind == "run_all":
            if "delay" in op:
                out("run_all delay=%r" % op["delay"])
                try:
                    self.sched.run_all(op["delay"])
                except Exception as e:
                    out("  error: " + fail(e))
            else:
                out("run_all")
                try:
                    self.sched.run_all()
                except Exception as e:
                    out("  error: " + fail(e))
            out("  now %s" % NOW[0])
        elif kind == "daemon":
            # The programs log at INFO, so the scheduler's DEBUG lines
            # are not shown.
            log.setLevel(logging.INFO)
            daemon(self, op)
            log.setLevel(logging.DEBUG)
        elif kind == "monitor":
            log.setLevel(logging.INFO)
            monitor(self, op)
            log.setLevel(logging.DEBUG)


# ------------------------------------------------------------ the daemon
#
# An ops daemon that reads its tasks from a config file and runs them the
# way the schedule docs suggest: run_pending(), then sleep for
# idle_seconds(). Failures go through the docs' catch_exceptions
# decorator. It logs to data/out/daemon.log and summarizes that log.

def catch_exceptions(logline, stats, cancel_on_failure):
    def deco(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except Exception as e:
                stats[job_func.__name__][1] += 1
                logline("%s FAILED: %s" % (job_func.__name__, fail(e)))
                if cancel_on_failure:
                    logline("%s cancelled" % job_func.__name__)
                    return schedule.CancelJob
        return wrapper
    return deco


TASKS = ["rotate_logs", "backup", "poll_feed", "weekly_report", "healthcheck",
         "refresh_certs", "heartbeat", "compact_db", "send_digest"]

UNITS = ["second", "seconds", "minute", "minutes", "hour", "hours", "day", "days",
         "week", "weeks", "monday", "tuesday", "wednesday", "thursday", "friday",
         "saturday", "sunday"]


def conf_value(s):
    if s.isdigit():
        return int(s)
    return s


def daemon(run, op):
    lines = []
    stats = {}

    def logline(msg):
        lines.append("%s %s" % (FakeDT.now(), msg))

    def task(name):
        def f(*args, **kwargs):
            st = stats[name]
            st[0] += 1
            st[2] = str(FakeDT.now())
            n = st[0]
            detail = " ".join([str(a) for a in args] + ["%s=%s" % kv for kv in kwargs.items()])
            if name == "backup" and args[0] == "media" and n % 2 == 0:
                raise OSError("No space left on device: '/backup/media'")
            if name == "backup" and args[0] == "db" and n == 3:
                raise OSError("connection refused")
            if name == "poll_feed" and n % 4 == 0:
                raise TimeoutError("timed out after 10s")
            if name == "heartbeat" and n == 40:
                raise ConnectionError("collector gone")
            logline("%s %s" % (name, detail) if detail else name)
            return None
        f.__name__ = name
        f.__qualname__ = name
        return f

    sched = run.sched
    end = parse_dt(op["until"])
    text = open(os.path.join("data", op["conf"])).read()
    out("daemon: %s" % op["conf"])
    for no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            words = line.split()
            if words[0] != "every":
                raise ValueError("a task starts with 'every'")
            i = 1
            job = None
            if i < len(words) and words[i] not in UNITS:
                n = int(words[i])
                i += 1
                job = sched.every(n)
                if i < len(words) and words[i] == "to":
                    job.to(int(words[i + 1]))
                    i += 2
            else:
                job = sched.every()
            if i >= len(words):
                raise ValueError("no unit")
            if words[i] not in UNITS:
                raise ValueError("unknown unit %r" % words[i])
            job = getattr(job, words[i])
            i += 1
            if i < len(words) and words[i] == "at":
                job.at(words[i + 1])
                i += 2
            if i < len(words) and words[i] == "until":
                job.until(words[i + 1].replace("_", " "))
                i += 2
            if i >= len(words) or words[i] != "do":
                raise ValueError("no 'do'")
            name = words[i + 1]
            if name not in TASKS:
                raise ValueError("no task named %r" % name)
            args = []
            kwargs = {}
            tags = []
            cancel = False
            for w in words[i + 2:]:
                if w.startswith("#"):
                    tags.append(w[1:])
                elif w == "!cancel":
                    cancel = True
                elif w == "until":
                    raise ValueError("'until' goes before 'do'")
                elif "=" in w:
                    k, v = w.split("=", 1)
                    kwargs[k] = conf_value(v)
                else:
                    args.append(conf_value(w))
            if tags:
                job.tag(*tags)
            stats.setdefault(name, [0, 0, "never"])
            f = catch_exceptions(logline, stats, cancel)(task(name))
            job.do(f, *args, **kwargs)
            out("  line %d: %s" % (no, run.show(job)))
        except (schedule.ScheduleError, ValueError, TypeError, IndexError) as e:
            out("  line %d: %s" % (no, fail(e)))
    out("  %d tasks scheduled at %s" % (len(sched.jobs), NOW[0]))
    wakeups = 0
    while True:
        sched.run_pending()
        idle = sched.idle_seconds
        if idle is None:
            break
        if NOW[0] + _dt.timedelta(seconds=max(idle, 0)) > end:
            break
        if idle > 0:
            schedule.time.sleep(idle)
        wakeups += 1
    out("  stopped at %s after %d wakeups" % (NOW[0], wakeups))
    os.makedirs("data/out", exist_ok=True)
    with open("data/out/daemon.log", "w") as fh:
        fh.write("".join(l + "\n" for l in lines))
    back = open("data/out/daemon.log").read().splitlines()
    out("  daemon.log: %d lines" % len(back))
    for l in back[:12]:
        out("    " + l)
    out("    ...")
    for l in back[-6:]:
        out("    " + l)
    failed = [l for l in back if " FAILED: " in l or l.endswith(" cancelled")]
    out("  failures:")
    for l in failed:
        out("    " + l)
    out("  by task:")
    for name in sorted(stats):
        runs, fails, last = stats[name]
        out("    %-14s runs=%-4d failed=%-2d last=%s" % (name, runs, fails, last))
    out("  still scheduled:")
    for j in sched.jobs:
        out("    %s" % run.show(j))
    out("  next: %s; nightly: %s" % (sched.next_run, sched.get_next_run("nightly")))


# ----------------------------------------------------------- the monitor
#
# A health monitor: a check every 30 seconds reads the service's state
# (data/health.csv gives it by seconds since the start). When it goes
# down, a one-off retry job is scheduled with exponential backoff from
# 10 s up to 120 s, each retry cancelling itself and scheduling the
# next; recovery clears the retries by tag. Alerts go to
# data/out/alerts.txt.

def monitor(run, op):
    sched = run.sched
    start = NOW[0]
    end = parse_dt(op["until"])
    rows = []
    for line in open(os.path.join("data", op["csv"])).read().splitlines()[1:]:
        s, status = line.split(",")
        rows.append((int(s), status))
    st = {"down_since": None, "delay": 10, "checks": 0, "retries": 0, "outages": 0}
    alerts = []

    def alert(msg):
        alerts.append("%s %s" % (FakeDT.now(), msg))

    def status():
        elapsed = (FakeDT.now() - start).total_seconds()
        cur = rows[0][1]
        for s, v in rows:
            if s <= elapsed:
                cur = v
        return cur

    def schedule_retry():
        job = sched.every(st["delay"]).seconds.do(retry).tag("retry")
        alert("retry in %ds (next run %s)" % (st["delay"], job.next_run))

    def check():
        st["checks"] += 1
        s = status()
        if s == "up":
            if st["down_since"] is not None:
                took = FakeDT.now() - st["down_since"]
                alert("RECOVERED after %s; dropping %d retries" % (
                    took, len(sched.get_jobs("retry"))))
                sched.clear("retry")
                st["down_since"] = None
                st["delay"] = 10
        elif st["down_since"] is None:
            st["down_since"] = FakeDT.now()
            st["outages"] += 1
            alert("DOWN (%s)" % s)
            schedule_retry()

    def retry():
        st["retries"] += 1
        s = status()
        if s == "up":
            alert("retry: up again")
        else:
            st["delay"] = min(st["delay"] * 2, 120)
            alert("retry: still %s" % s)
            schedule_retry()
        return schedule.CancelJob

    sched.every(30).seconds.do(check).tag("health")
    out("monitor: %s from %s" % (op["csv"], NOW[0]))
    while True:
        sched.run_pending()
        nxt = sched.next_run
        if nxt is None or nxt > end:
            break
        NOW[0] = to_fake(nxt)
    os.makedirs("data/out", exist_ok=True)
    with open("data/out/alerts.txt", "w") as fh:
        fh.write("".join(a + "\n" for a in alerts))
    for line in open("data/out/alerts.txt").read().splitlines():
        out("  " + line)
    out("  checks=%d retries=%d outages=%d at %s" % (
        st["checks"], st["retries"], st["outages"], NOW[0]))
    for j in sched.jobs:
        out("  left: %s" % run.show(j))


def main():
    os.chdir(HERE)
    for line in open("data/jobs.jsonl", encoding="utf-8"):
        spec = json.loads(line)
        out("== %s" % spec["name"])
        r = Run(spec)
        for op in spec["ops"]:
            r.op(op)
    sys.stdout.write("".join(l + "\n" for l in OUT))


main()
