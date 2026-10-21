# Runs data/jobs.jsonl and the two programs through structlog 24.4.0
# itself (the copy in structlog/, unchanged) and prints what
# mini_structlog.kara must print.
#
# The clock is fake: each time a TimeStamper asks for the time it gets
# the clock and moves it on a quarter of a second. Local time is UTC+2.
# rich, colorama and better_exceptions are kept out, so exceptions print
# as plain tracebacks. Exceptions carry no traceback frames: the ones a
# job raises have theirs taken off, so a traceback is the exception's own
# lines and its chain.
import csv
import json
import os
import sys
from datetime import datetime as real_datetime
from datetime import timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ["NO_COLOR"] = "1"
os.environ.pop("FORCE_COLOR", None)
for blocked in ("rich", "colorama", "better_exceptions"):
    sys.modules[blocked] = None
sys.stdout.reconfigure(write_through=True)

import structlog  # noqa: E402
import structlog.processors  # noqa: E402
from structlog.contextvars import (  # noqa: E402
    bind_contextvars, bound_contextvars, clear_contextvars, get_contextvars,
    get_merged_contextvars, merge_contextvars, unbind_contextvars)
from structlog.dev import ConsoleRenderer, set_exc_info  # noqa: E402
from structlog.exceptions import DropEvent  # noqa: E402
from structlog.processors import (  # noqa: E402
    EventRenamer, JSONRenderer, KeyValueRenderer, LogfmtRenderer,
    MaybeTimeStamper, TimeStamper, UnicodeDecoder, UnicodeEncoder,
    add_log_level, dict_tracebacks, format_exc_info)
from structlog.testing import (  # noqa: E402
    CapturingLogger, CapturingLoggerFactory, LogCapture, ReturnLogger,
    ReturnLoggerFactory, capture_logs)

# --- the fake clock -----------------------------------------------------

CLOCK = [0]
STEP = 250000
EPOCH = real_datetime(1970, 1, 1, tzinfo=timezone.utc)
LOCAL = timedelta(hours=2)


def tick():
    us = CLOCK[0]
    CLOCK[0] += STEP
    return us


class FakeDatetime:
    @staticmethod
    def now(tz=None):
        t = EPOCH + timedelta(microseconds=tick())
        if tz is None:
            return (t + LOCAL).replace(tzinfo=None)
        return t.astimezone(tz)


class FakeDatetimeModule:
    datetime = FakeDatetime
    timezone = timezone


class FakeTime:
    @staticmethod
    def time():
        return tick() / 1000000


structlog.processors.datetime = FakeDatetimeModule
structlog.processors.time = FakeTime


def out(s=""):
    print(s)


def fail(e):
    return "!! %s: %s" % (type(e).__name__, e)


# --- values -------------------------------------------------------------

class Obj:
    def __init__(self, d):
        self._repr = d["repr"]
        self._str = d.get("str")
        if "structlog" in d:
            sl = decode(d["structlog"])
            self.__structlog__ = lambda: sl

    def __repr__(self):
        return self._repr

    def __str__(self):
        return self._str if self._str is not None else self._repr


BUILTIN_EXC = {c.__name__: c for c in [
    Exception, ValueError, KeyError, RuntimeError, TypeError, OSError,
    ConnectionError, TimeoutError, PermissionError, ZeroDivisionError]}
CUSTOM_EXC = {}


def exc_class(name, module):
    if module is None and name in BUILTIN_EXC:
        return BUILTIN_EXC[name]
    key = (name, module)
    if key not in CUSTOM_EXC:
        CUSTOM_EXC[key] = type(name, (Exception,), {"__module__": module or "app"})
    return CUSTOM_EXC[key]


def make_exc(d):
    e = exc_class(d["type"], d.get("module"))(*[decode(a) for a in d["args"]])
    if "cause" in d:
        e.__cause__ = make_exc(d["cause"])
    if "context" in d:
        e.__context__ = make_exc(d["context"])
    if "suppress" in d:
        e.__suppress_context__ = d["suppress"]
    for n in d.get("notes", []):
        e.add_note(n)
    return e


def decode(v):
    if isinstance(v, list):
        return [decode(x) for x in v]
    if isinstance(v, dict):
        if "$bytes" in v:
            return bytes.fromhex(v["$bytes"])
        if "$tuple" in v:
            return tuple(decode(x) for x in v["$tuple"])
        if "$float" in v:
            return float(v["$float"])
        if "$dict" in v:
            return {decode(k): decode(x) for k, x in v["$dict"]}
        if "$obj" in v:
            return Obj(v["$obj"])
        if "$exc" in v:
            return make_exc(v["$exc"])
        return {k: decode(x) for k, x in v.items()}
    return v


# --- processors the jobs make -------------------------------------------

def method_proc(logger, name, ed):
    ed["method"] = name
    return ed


def add_proc(kw):
    def add(logger, name, ed):
        ed.update(kw)
        return ed
    return add


def as_tuple(logger, name, ed):
    return (ed.pop("event"),), ed


def return_proc(value):
    def ret(logger, name, ed):
        return value
    return ret


def drop_if(key, value):
    def drop(logger, name, ed):
        if key in ed and ed[key] == value:
            raise DropEvent
        return ed
    return drop


class Sampler:
    def __init__(self, event, every):
        self.event = event
        self.every = every
        self.seen = 0
        self.dropped = 0

    def __call__(self, logger, name, ed):
        if ed.get("event") == self.event:
            self.seen += 1
            if (self.seen - 1) % self.every:
                self.dropped += 1
                raise DropEvent
        return ed


def raise_proc(d):
    def boom(logger, name, ed):
        raise make_exc(d)
    return boom


def encode_proc(logger, name, ed):
    return ed.encode("utf-8")


def redact(keys):
    def proc(logger, name, ed):
        for k in keys:
            if k in ed:
                ed[k] = "[redacted]"
        return ed
    return proc


class World:
    def __init__(self):
        self.vars = {}
        self.captures = {}
        self.capturing = {}
        self.styles = {}


W = World()

NAMED = {"add_log_level": add_log_level, "format_exc_info": format_exc_info,
         "dict_tracebacks": dict_tracebacks, "set_exc_info": set_exc_info,
         "merge_contextvars": merge_contextvars}


def processor(spec):
    if isinstance(spec, str):
        return NAMED[spec]
    p = spec["p"]
    kw = {k: decode(v) for k, v in spec.items() if k != "p"}
    if p == "KeyValueRenderer":
        return KeyValueRenderer(**kw)
    if p == "LogfmtRenderer":
        return LogfmtRenderer(**kw)
    if p == "JSONRenderer":
        if "separators" in kw:
            kw["separators"] = tuple(kw["separators"])
        return JSONRenderer(**kw)
    if p == "TimeStamper":
        return TimeStamper(**kw)
    if p == "MaybeTimeStamper":
        return MaybeTimeStamper(**kw)
    if p == "EventRenamer":
        return EventRenamer(**kw)
    if p == "UnicodeEncoder":
        return UnicodeEncoder(**kw)
    if p == "UnicodeDecoder":
        return UnicodeDecoder(**kw)
    if p == "ConsoleRenderer":
        if "level_styles" in kw:
            kw["level_styles"] = W.styles[kw["level_styles"]]
        return ConsoleRenderer(**kw)
    if p == "LogCapture":
        cap = LogCapture()
        W.captures[kw["name"]] = cap
        return cap
    if p == "method":
        return method_proc
    if p == "add":
        return add_proc(kw["kw"])
    if p == "as_tuple":
        return as_tuple
    if p == "return":
        return return_proc(kw["value"])
    if p == "drop_if":
        return drop_if(kw["key"], kw["value"])
    if p == "sample":
        return Sampler(kw["event"], kw["every"])
    if p == "raise":
        return raise_proc(spec["exc"]["$exc"])
    if p == "encode":
        return encode_proc
    raise SystemExit("unknown processor %r" % p)


def wrapped_logger(spec):
    t = spec["t"]
    if t == "return":
        return ReturnLogger()
    if t == "print":
        return structlog.PrintLogger()
    if t == "write":
        return structlog.WriteLogger()
    if t == "bytes":
        return structlog.BytesLogger()
    if t == "capturing":
        if spec["name"] not in W.capturing:
            W.capturing[spec["name"]] = CapturingLogger()
        return W.capturing[spec["name"]]
    raise SystemExit("unknown logger %r" % t)


def logger_factory(spec):
    t = spec["t"]
    if t == "return":
        return ReturnLoggerFactory()
    if t == "print":
        return structlog.PrintLoggerFactory()
    if t == "capturing":
        f = CapturingLoggerFactory()
        W.capturing[spec["name"]] = f.logger
        return f
    raise SystemExit("unknown factory %r" % t)


def wrapper_class(spec):
    if spec == "generic":
        return structlog.BoundLogger
    return structlog.make_filtering_bound_logger(int(spec.split(":")[1]))


def kwargs(d):
    return {k: decode(v) for k, v in d.items()}


def show_styles(d):
    return repr(d)


def run_steps(steps):
    for st in steps:
        try:
            run_step(st)
        except Exception as e:  # noqa: BLE001
            out(fail(e))


def run_step(st):
    op = st["op"]
    V = W.vars
    if op == "get":
        V[st["as"]] = structlog.get_logger(*decode(st["args"]), **kwargs(st["init"]))
    elif op == "wrap":
        procs = [processor(p) for p in st["procs"]] if "procs" in st else None
        wc = wrapper_class(st["wrapper"]) if "wrapper" in st else None
        V[st["as"]] = structlog.wrap_logger(
            wrapped_logger(st["wrapped"]), processors=procs, wrapper_class=wc,
            cache_logger_on_first_use=st.get("cache"), **kwargs(st["init"]))
    elif op == "configure":
        procs = [processor(p) for p in st["procs"]] if "procs" in st else None
        wc = wrapper_class(st["wrapper"]) if "wrapper" in st else None
        fac = logger_factory(st["factory"]) if "factory" in st else None
        structlog.configure(processors=procs, wrapper_class=wc, logger_factory=fac,
                            cache_logger_on_first_use=st.get("cache"))
    elif op == "reset":
        structlog.reset_defaults()
    elif op == "call":
        ret = getattr(V[st["log"]], st["m"])(*decode(st["args"]), **kwargs(st["kw"]))
        if ret is not None:
            out("-> " + repr(ret))
    elif op == "bind":
        V[st["as"]] = V[st["log"]].bind(**kwargs(st["kw"]))
    elif op == "new":
        V[st["as"]] = V[st["log"]].new(**kwargs(st["kw"]))
    elif op == "unbind":
        V[st["as"]] = V[st["log"]].unbind(*st["keys"])
    elif op == "try_unbind":
        V[st["as"]] = V[st["log"]].try_unbind(*st["keys"])
    elif op == "context":
        out("context %s: %r" % (st["log"], structlog.get_context(V[st["log"]])))
    elif op == "eq":
        out("%s == %s: %r" % (st["a"], st["b"], V[st["a"]] == V[st["b"]]))
    elif op == "print":
        out(st["text"])
    elif op == "clock":
        CLOCK[0] = st["us"]
    elif op == "try":
        e = make_exc(st["exc"])
        try:
            raise e
        except Exception as caught:  # noqa: BLE001
            caught.__traceback__ = None
            run_steps(st["body"])
    elif op == "capture":
        with capture_logs() as cap:
            run_steps(st["body"])
        out("captured: %r" % (cap,))
    elif op == "calls":
        c = W.capturing[st["name"]]
        out("%s: %d call(s)" % (st["name"], len(c.calls)))
        for call in c.calls:
            out("  " + repr(call))
        c.calls.clear()
    elif op == "entries":
        out("%s: %r" % (st["name"], W.captures[st["name"]].entries))
    elif op == "ctx_bind":
        bind_contextvars(**kwargs(st["kw"]))
    elif op == "ctx_unbind":
        unbind_contextvars(*st["keys"])
    elif op == "ctx_clear":
        clear_contextvars()
    elif op == "ctx_get":
        out("contextvars: %r" % (sorted(get_contextvars().items()),))
    elif op == "ctx_bound":
        with bound_contextvars(**kwargs(st["kw"])):
            run_steps(st["body"])
    elif op == "merged":
        out("merged %s: %r" % (st["log"], sorted(get_merged_contextvars(V[st["log"]]).items())))
    elif op == "styles":
        if "map" in st:
            W.styles[st["name"]] = dict(st["map"])
        else:
            W.styles[st["name"]] = ConsoleRenderer.get_default_level_styles(st["colors"])
    elif op == "show":
        out("%s: %s" % (st["name"], show_styles(W.styles[st["name"]])))
    else:
        raise SystemExit("unknown op %r" % op)


def reset():
    structlog.reset_defaults()
    clear_contextvars()


# --- the programs -------------------------------------------------------

class UpstreamError(Exception):
    pass


UpstreamError.__module__ = "orders.upstream"


def api():
    out("== program: an API's access log ==")
    reset()
    os.makedirs("data/out", exist_ok=True)
    f = open("data/out/api.jsonl", "w")
    structlog.configure(
        processors=[merge_contextvars, add_log_level, TimeStamper(fmt="iso"),
                    redact(["authorization"]), format_exc_info,
                    EventRenamer("message"), JSONRenderer(sort_keys=True)],
        wrapper_class=structlog.make_filtering_bound_logger(20),
        logger_factory=structlog.WriteLoggerFactory(file=f),
        cache_logger_on_first_use=True)
    log = structlog.get_logger(service="orders-api", version="2.4.1")
    with open("data/requests.csv", newline="") as rf:
        rows = list(csv.DictReader(rf))
    for row in rows:
        CLOCK[0] = int(row["ts_us"])
        clear_contextvars()
        bind_contextvars(request_id=row["request_id"], client_ip=row["ip"])
        rlog = log.bind(method=row["method"], path=row["path"])
        if row["user"]:
            rlog = rlog.bind(user=row["user"])
        if row["authorization"]:
            rlog = rlog.bind(authorization=row["authorization"])
        rlog.debug("request.received")
        status = int(row["status"])
        ms = int(row["ms"])
        kw = {"status": status, "duration_ms": ms, "bytes": int(row["bytes"])}
        if status >= 500:
            rlog.error("request.failed", exc_info=UpstreamError("upstream returned %d" % status), **kw)
        elif status == 429:
            rlog.warning("request.throttled", retry_after=2 ** (ms % 4), **kw)
        elif status >= 400:
            rlog.warning("request.rejected", **kw)
        else:
            rlog.info("request.completed", **kw)
        if ms >= 1000:
            rlog.warning("request.slow", threshold_ms=1000, duration_ms=ms)
    f.close()
    clear_contextvars()
    with open("data/out/api.jsonl") as rf:
        lines = rf.read().splitlines()
    out("wrote %d lines to data/out/api.jsonl, the first four:" % len(lines))
    for line in lines[:4]:
        out("  " + line)
    recs = [json.loads(line) for line in lines]
    levels = {}
    events = {}
    for r in recs:
        levels[r["level"]] = levels.get(r["level"], 0) + 1
        events[r["message"]] = events.get(r["message"], 0) + 1
    out("by level: " + ", ".join("%s=%d" % kv for kv in sorted(levels.items())))
    out("by message: " + ", ".join("%s=%d" % kv for kv in sorted(events.items())))
    classes = {}
    durations = []
    sent = 0
    users = {}
    redacted = 0
    for r in recs:
        if "status" in r:
            c = "%dxx" % (r["status"] // 100)
            classes[c] = classes.get(c, 0) + 1
            durations.append(r["duration_ms"])
            if r["status"] < 400:
                sent += r["bytes"]
            u = r.get("user", "-")
            users[u] = users.get(u, 0) + 1
        if r.get("authorization") == "[redacted]":
            redacted += 1
    out("by status: " + ", ".join("%s=%d" % kv for kv in sorted(classes.items())))
    durations.sort()
    n = len(durations)
    for p in (50, 90, 99):
        k = (p * n + 99) // 100
        out("p%d: %d ms" % (p, durations[k - 1]))
    out("bytes sent: %d" % sent)
    out("authorization redacted in %d lines" % redacted)
    ranked = sorted(users.items(), key=lambda kv: (-kv[1], kv[0]))
    out("requests by user: " + ", ".join("%s=%d" % kv for kv in ranked))
    slow = sorted((r for r in recs if r["message"] == "request.slow"),
                  key=lambda r: (-r["duration_ms"], r["request_id"]))
    for r in slow[:3]:
        out("slow: %s %s %s %d ms at %s" % (r["request_id"], r["method"], r["path"],
                                          r["duration_ms"], r["timestamp"]))
    failed = [r for r in recs if r["message"] == "request.failed"]
    for r in failed:
        out("failed: %s %s -> %s" % (r["request_id"], r["path"], r["exception"]))


WORKER_EXC = {"TimeoutError": TimeoutError, "ValueError": ValueError,
              "PermissionError": PermissionError}


def worker():
    out("== program: a task worker ==")
    reset()
    CLOCK[0] = 1714579200000000
    f = open("data/out/worker.log", "w")
    sampler = Sampler("heartbeat", 4)
    flog = structlog.wrap_logger(
        structlog.PrintLogger(file=f),
        processors=[add_log_level, TimeStamper(fmt="%Y-%m-%dT%H:%M:%S.%fZ", key="ts"), sampler,
                    redact(["secret"]), format_exc_info,
                    LogfmtRenderer(key_order=["ts", "level", "event", "task"], drop_missing=True)],
        wrapper_class=structlog.make_filtering_bound_logger(10),
        worker="w-1")
    console = structlog.wrap_logger(
        structlog.PrintLogger(),
        processors=[add_log_level, TimeStamper(fmt="%H:%M:%S", utc=False),
                    ConsoleRenderer(colors=False, pad_event=20)],
        wrapper_class=structlog.make_filtering_bound_logger(30))
    with open("data/tasks.jsonl") as tf:
        tasks = [json.loads(line) for line in tf]
    done = failed = retries = 0
    for task in tasks:
        tlog = flog.bind(task=task["id"], kind=task["kind"])
        tlog.debug("task.received", **task["payload"])
        outcomes = task["outcomes"]
        for a, outcome in enumerate(outcomes, 1):
            for hb in range(task["heartbeats"]):
                tlog.debug("heartbeat", attempt=a, beat=hb + 1)
                CLOCK[0] += 1000000
            CLOCK[0] += task["cost_us"]
            if outcome == "ok":
                tlog.info("task.done", attempt=a, elapsed_ms=task["cost_us"] / 1000, retried=a > 1)
                done += 1
                break
            typ, msg = outcome.split(":", 1)
            if a < len(outcomes):
                tlog.warning("task.retry", attempt=a, error=typ, will_retry=True)
                retries += 1
            else:
                tlog.error("task.failed", attempt=a, exc_info=WORKER_EXC[typ](msg), will_retry=False)
                console.error("task failed", task=task["id"], kind=task["kind"], error=typ)
                failed += 1
    f.close()
    with open("data/out/worker.log") as rf:
        lines = rf.read().splitlines()
    out("data/out/worker.log, %d lines:" % len(lines))
    for line in lines:
        out("  " + line)
    out("tasks: %d done, %d failed, %d retries; heartbeats: %d seen, %d dropped"
        % (done, failed, retries, sampler.seen, sampler.dropped))


def main():
    with open("data/jobs.jsonl") as f:
        jobs = [json.loads(line) for line in f]
    for j in jobs:
        reset()
        W.vars.clear()
        W.captures.clear()
        W.capturing.clear()
        W.styles.clear()
        out("== %s ==" % j["name"])
        run_steps(j["steps"])
    api()
    worker()


main()
