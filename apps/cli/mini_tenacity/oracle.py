# Runs data/jobs.jsonl through tenacity 9.0.0 itself (the copy in
# tenacity/, unchanged) and prints what mini_tenacity.kara must print.
# The clock is fake: time.monotonic() reads it, and time.sleep() and
# each call of a job's function move it on.
import json
import logging
import os
import random
import re
import sys
import threading
import time
from datetime import timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tenacity  # noqa: E402
from tenacity import (  # noqa: E402
    RetryError, Retrying, TryAgain, after_log, before_log, before_sleep_log,
    retry, retry_all, retry_always, retry_any, retry_if_exception,
    retry_if_exception_cause_type, retry_if_exception_message,
    retry_if_exception_type, retry_if_not_exception_message,
    retry_if_not_exception_type, retry_if_not_result, retry_if_result,
    retry_never, retry_unless_exception_type, stop_after_attempt,
    stop_after_delay, stop_all, stop_any, stop_before_delay, stop_never,
    stop_when_event_set, wait_chain, wait_combine, wait_exponential,
    wait_exponential_jitter, wait_fixed, wait_incrementing, wait_random,
    wait_random_exponential)

CLOCK = [0.0]


def monotonic():
    return CLOCK[0]


def fake_sleep(seconds):
    out("  [%r] sleep %r" % (CLOCK[0], seconds))
    CLOCK[0] += seconds


time.monotonic = monotonic
time.sleep = fake_sleep

OUT = []
SINK = [OUT]


def out(s=""):
    SINK[0].append(s)


class Capture(logging.Handler):
    def emit(self, record):
        out("  %s:%s:%s" % (record.levelname, record.name, record.getMessage()))


class FileCapture(logging.Handler):
    def __init__(self, lines):
        super().__init__()
        self.lines = lines

    def emit(self, record):
        self.lines.append("[%.3f] %s %s: %s" % (CLOCK[0], record.levelname, record.name,
                                               record.getMessage()))


ROOT = logging.getLogger()
CAPTURE = Capture()
ROOT.addHandler(CAPTURE)
USED_LOGGERS = set()


def logger(name):
    USED_LOGGERS.add(name)
    return logging.getLogger(name)


class TransientError(Exception):
    pass


class RateLimited(TransientError):
    pass


class FatalError(Exception):
    pass


class ServerError(TransientError):
    pass


CLASSES = {c.__name__: c for c in [
    KeyboardInterrupt, Exception, OSError, ConnectionError, ConnectionResetError,
    ConnectionRefusedError, TimeoutError, PermissionError, ValueError, LookupError,
    KeyError, RuntimeError, TryAgain, TransientError, RateLimited, FatalError,
    ServerError]}


def sanitize(s):
    s = re.sub(r"0x[0-9a-f]+", "0x?", s)
    return re.sub(r"<RetryCallState \d+:", "<RetryCallState ?:", s)


def fail(e):
    return "%s: %s" % (type(e).__name__, sanitize(str(e)))


def make_exc(step):
    cls = CLASSES[step["raise"]]
    if "errno" in step:
        e = cls(step["errno"], step["msg"])
    elif "msg" in step:
        e = cls(step["msg"])
    else:
        e = cls()
    if "cause" in step:
        e.__cause__ = make_exc(step["cause"])
    return e


EVENT = threading.Event()


def seconds(v):
    if isinstance(v, dict):
        return timedelta(**v["td"])
    return v


def build_wait(w):
    (k, v), = w.items()
    if k == "fixed":
        return wait_fixed(seconds(v))
    if k == "none":
        return tenacity.wait_none()
    if k == "random":
        return wait_random(*v)
    if k == "incrementing":
        return wait_incrementing(*v)
    if k == "exponential":
        return wait_exponential(**v)
    if k == "random_exponential":
        return wait_random_exponential(**v)
    if k == "exp_jitter":
        return wait_exponential_jitter(**v)
    if k == "chain":
        return wait_chain(*[build_wait(x) for x in v])
    if k == "combine":
        return wait_combine(*[build_wait(x) for x in v])
    if k == "plus":
        return build_wait(v[0]) + build_wait(v[1])
    if k == "sum":
        return sum([build_wait(x) for x in v])
    if k == "radd":
        return v[0] + build_wait(v[1])
    raise AssertionError(k)


def build_stop(s):
    (k, v), = s.items()
    if k == "after_attempt":
        return stop_after_attempt(v)
    if k == "after_delay":
        return stop_after_delay(seconds(v))
    if k == "before_delay":
        return stop_before_delay(seconds(v))
    if k == "never":
        return stop_never
    if k == "event_set":
        return stop_when_event_set(EVENT)
    if k == "or":
        return build_stop(v[0]) | build_stop(v[1])
    if k == "and":
        return build_stop(v[0]) & build_stop(v[1])
    if k == "any":
        return stop_any(*[build_stop(x) for x in v])
    if k == "all":
        return stop_all(*[build_stop(x) for x in v])
    raise AssertionError(k)


def build_pred(p):
    (k, v), = p.items()
    if k == "falsy":
        return lambda r: not r
    if k == "eq":
        return lambda r: r == v
    if k == "ge":
        return lambda r: r >= v
    if k == "lt":
        return lambda r: r < v
    if k == "is_none":
        return lambda r: r is None
    raise AssertionError(k)


def types_of(v):
    if v is None:
        return Exception
    return tuple(CLASSES[n] for n in v)


def build_retry(r):
    (k, v), = r.items()
    if k == "exc_type":
        return retry_if_exception_type(types_of(v))
    if k == "not_exc_type":
        return retry_if_not_exception_type(types_of(v))
    if k == "unless_exc_type":
        return retry_unless_exception_type(types_of(v))
    if k == "exc_cause_type":
        return retry_if_exception_cause_type(types_of(v))
    if k == "result":
        return retry_if_result(build_pred(v))
    if k == "not_result":
        return retry_if_not_result(build_pred(v))
    if k == "exc_message":
        return retry_if_exception_message(**v)
    if k == "not_exc_message":
        return retry_if_not_exception_message(**v)
    if k == "always":
        return retry_always
    if k == "never":
        return retry_never
    if k == "or":
        return build_retry(v[0]) | build_retry(v[1])
    if k == "and":
        return build_retry(v[0]) & build_retry(v[1])
    if k == "any":
        return retry_any(*[build_retry(x) for x in v])
    if k == "all":
        return retry_all(*[build_retry(x) for x in v])
    raise AssertionError(k)


def trace(rs):
    out("  trace: %s; next_action=%r; upcoming_sleep=%r" % (
        sanitize(repr(rs)), rs.next_action, rs.upcoming_sleep))


def stats(rs):
    out("  stats: %r" % (rs.retry_object.statistics,))


def build_cb(c, kind):
    if c == "trace":
        return trace
    if c == "stats":
        return stats
    name, level = c["log"]
    lg = logger(name)
    if kind == "before":
        return before_log(lg, level)
    if kind == "after":
        if "fmt" in c:
            return after_log(lg, level, sec_format=c["fmt"])
        return after_log(lg, level)
    return before_sleep_log(lg, level)


def build_error_callback(c):
    if c == "attempts":
        return lambda rs: rs.attempt_number
    if c == "last_result":
        return lambda rs: rs.outcome.result()
    v = c["fallback"]
    return lambda rs: v


def build_config(cfg):
    kw = {}
    if "stop" in cfg:
        kw["stop"] = build_stop(cfg["stop"])
    if "wait" in cfg:
        kw["wait"] = build_wait(cfg["wait"])
    if "retry" in cfg:
        kw["retry"] = build_retry(cfg["retry"])
    for k in ("before", "after", "before_sleep"):
        if k in cfg:
            kw[k] = build_cb(cfg[k], k)
    if "reraise" in cfg:
        kw["reraise"] = cfg["reraise"]
    if "error_callback" in cfg:
        kw["retry_error_callback"] = build_error_callback(cfg["error_callback"])
    return kw


def make_fn(spec):
    script = spec["script"]
    n = [0]

    def call():
        i = n[0]
        n[0] += 1
        step = script[min(i, len(script) - 1)]
        CLOCK[0] += step["cost"]
        if step.get("set_event"):
            EVENT.set()
        if "raise" in step:
            e = make_exc(step)
            out("  [%r] call %d: raise %s" % (CLOCK[0], i + 1, fail(e)))
            raise e
        v = step["return"]
        out("  [%r] call %d: return %r" % (CLOCK[0], i + 1, v))
        return v

    call.__module__ = spec["fn"]["module"]
    call.__qualname__ = spec["fn"]["qualname"]
    return call


def show_raised(e):
    out("  -> raised " + fail(e))
    if isinstance(e, RetryError):
        la = e.last_attempt
        if la.failed:
            what = "raised " + fail(la.exception())
        else:
            what = "returned %r" % (la.result(),)
        out("  last attempt: #%d %s" % (la.attempt_number, what))
        c = e.__cause__
        out("  cause: " + (fail(c) if c is not None else "None"))


def show_call(f):
    try:
        v = f()
    except BaseException as e:  # noqa: B902
        show_raised(e)
    else:
        out("  -> returned %r" % (v,))


def run_job(spec):
    CLOCK[0] = spec["clock"]
    random.seed(spec["seed"])
    EVENT.clear()
    for name in USED_LOGGERS:
        logging.getLogger(name).setLevel(logging.NOTSET)
    ROOT.setLevel(spec["log_level"])
    for name, level in spec.get("loggers", {}).items():
        logger(name).setLevel(level)
    try:
        kw = build_config(spec["config"])
    except BaseException as e:  # noqa: B902
        out("  config: " + fail(e))
        return
    fn = make_fn(spec)
    mode = spec["mode"]
    calls = spec.get("calls", 1)
    if mode == "call":
        r = Retrying(**kw)
        for i in range(calls):
            out("  call #%d" % (i + 1))
            show_call(lambda: r(fn))
            out("  statistics: %r" % (r.statistics,))
    elif mode in ("decorated", "bare"):
        f = retry(fn) if mode == "bare" else retry(**kw)(fn)
        out("  statistics before: %r" % (f.statistics,))
        for i in range(calls):
            out("  call #%d" % (i + 1))
            show_call(f)
            out("  statistics: %r" % (f.statistics,))
        if "retry_with" in spec:
            g = f.retry_with(**build_config(spec["retry_with"]))
            out("  retry_with")
            show_call(g)
            out("  statistics: %r" % (g.statistics,))
            out("  original statistics: %r" % (f.statistics,))
    else:
        r = Retrying(**kw)

        def loop():
            n = 0
            for attempt in r:
                n += 1
                out("  attempt #%d" % attempt.retry_state.attempt_number)
                with attempt:
                    fn()
            return "loop ended after %d attempts" % n

        show_call(loop)
        out("  statistics: %r" % (r.statistics,))


# ------------------------------------------------------------- programs

def read_csv(path):
    with open(path) as f:
        lines = f.read().splitlines()
    head = lines[0].split(",")
    return [dict(zip(head, line.split(","))) for line in lines[1:]]


def replies(text):
    rs = []
    for item in text.split():
        what, secs = item.split(":")
        rs.append((what, float(secs)))
    return rs


class Status:
    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return "<Status %d>" % self.code


def webhooks(spec):
    lines = []
    handler = FileCapture(lines)
    ROOT.removeHandler(CAPTURE)
    ROOT.addHandler(handler)
    ROOT.setLevel(logging.DEBUG)
    lg = logger("webhooks")
    eps = {}
    for row in read_csv("data/endpoints.csv"):
        eps[row["name"]] = {"url": row["url"], "replies": replies(row["replies"]), "n": 0}
    with open("data/outbox.jsonl") as f:
        outbox = [json.loads(line) for line in f.read().splitlines()]

    def post(hook):
        ep = eps[hook["endpoint"]]
        i = ep["n"]
        ep["n"] += 1
        what, secs = ep["replies"][min(i, len(ep["replies"]) - 1)]
        CLOCK[0] += secs
        if what == "reset":
            raise ConnectionResetError(104, "Connection reset by peer")
        if what == "refused":
            raise ConnectionRefusedError(111, "Connection refused")
        if what == "timeout":
            raise TimeoutError("POST %s timed out after %rs" % (ep["url"], secs))
        return int(what)

    post.__module__ = "webhooks.delivery"
    post.__qualname__ = "post"
    send = retry(
        stop=stop_after_attempt(5) | stop_after_delay(20),
        wait=wait_exponential_jitter(initial=0.5, max=8, jitter=0.25),
        retry=(retry_if_exception_type((ConnectionError, TimeoutError))
               | retry_if_result(lambda st: st >= 500 or st == 429)),
        before_sleep=before_sleep_log(lg, logging.WARNING),
        after=after_log(lg, logging.DEBUG),
        reraise=True)(post)
    dead = []
    counts = {"delivered": 0, "rejected": 0, "dead": 0}
    total_attempts = 0
    total_idle = 0
    for hook in outbox:
        start = CLOCK[0]
        try:
            st = send(hook)
        except RetryError as e:
            status, why = "dead", "gave up on status %d" % e.last_attempt.result()
        except (ConnectionError, TimeoutError) as e:
            status, why = "dead", fail(e)
        else:
            if 200 <= st < 300:
                status, why = "delivered", "status %d" % st
            else:
                status, why = "rejected", "status %d" % st
        s = send.statistics
        total_attempts += s["attempt_number"]
        total_idle += s["idle_for"]
        counts[status] += 1
        out("  %s %s %s -> %s (%s) after %d attempt(s), idle %.3fs, took %.3fs" % (
            hook["id"], hook["type"], hook["endpoint"], status, why,
            s["attempt_number"], s["idle_for"], CLOCK[0] - start))
        if status == "dead":
            dead.append("%s,%s,%s,%d,%s" % (hook["id"], hook["endpoint"], hook["type"],
                                            s["attempt_number"], why))
            lg.error("dead-lettered %s for tenant %d", hook["id"], hook["tenant"])
    out("  delivered %d, rejected %d, dead %d; %d attempts, idle %r" % (
        counts["delivered"], counts["rejected"], counts["dead"], total_attempts, total_idle))
    os.makedirs("data/out", exist_ok=True)
    with open("data/out/dead_letter.csv", "w") as f:
        f.write("id,endpoint,type,attempts,reason\n")
        for d in dead:
            f.write(d + "\n")
    with open("data/out/delivery.log", "w") as f:
        for line in lines:
            f.write(line + "\n")
    ROOT.removeHandler(handler)
    ROOT.addHandler(CAPTURE)
    for path in ("data/out/dead_letter.csv", "data/out/delivery.log"):
        out("  == " + path)
        with open(path) as f:
            for line in f.read().splitlines():
                out("  " + line)


CHUNK = 4 * 1048576


def is_transient(e):
    return isinstance(e, (TransientError, TimeoutError))


def backup(spec):
    lines = []
    handler = FileCapture(lines)
    ROOT.removeHandler(CAPTURE)
    ROOT.addHandler(handler)
    ROOT.setLevel(logging.INFO)
    lg = logger("backup")
    manifest = []
    sent = 0
    for row in read_csv("data/backup.csv"):
        path = row["path"]
        size = int(row["bytes"])
        script = row["replies"].split()
        n = [0]
        chunks = (size + CHUNK - 1) // CHUNK

        def upload(k, length):
            i = n[0]
            n[0] += 1
            what = script[min(i, len(script) - 1)]
            if what == "ok":
                CLOCK[0] += length / CHUNK * 1.5
                return
            if what == "busy":
                CLOCK[0] += 0.05
                raise TryAgain
            if what == "5xx":
                CLOCK[0] += 0.2
                raise ServerError("503 Slow Down")
            if what == "denied":
                CLOCK[0] += 0.1
                raise PermissionError(13, "Permission denied: %s" % path)
            CLOCK[0] += 20
            raise TimeoutError("upload of %s part %d timed out" % (path, k))

        upload.__module__ = "backup.store"
        upload.__qualname__ = "Bucket.put_part"
        out("  %s (%d bytes, %d chunk(s))" % (path, size, chunks))
        done = 0
        status = "ok"
        try:
            for k in range(1, chunks + 1):
                length = min(CHUNK, size - (k - 1) * CHUNK)
                r = Retrying(
                    stop=stop_before_delay(60),
                    wait=wait_random_exponential(multiplier=0.5, max=10),
                    retry=retry_if_exception(is_transient),
                    before_sleep=before_sleep_log(lg, logging.INFO),
                    retry_error_callback=lambda rs: None)
                for attempt in r:
                    with attempt:
                        upload(k, length)
                rs = attempt.retry_state
                s = r.statistics
                if rs.outcome.failed:
                    out("    chunk %d/%d: skipped after %d attempt(s), idle %.3fs: %s" % (
                        k, chunks, s["attempt_number"], s["idle_for"], fail(rs.outcome.exception())))
                    lg.warning("skipped part %d of %s", k, path)
                    status = "partial"
                else:
                    done += 1
                    sent += length
                    out("    chunk %d/%d: %d bytes after %d attempt(s), idle %.3fs" % (
                        k, chunks, length, s["attempt_number"], s["idle_for"]))
        except BaseException as e:  # noqa: B902
            out("    aborted: " + fail(e))
            lg.error("aborted %s: %s", path, e)
            status = "aborted"
        manifest.append("%s,%d,%d,%d,%s" % (path, size, chunks, done, status))
    out("  sent %d bytes; clock %r" % (sent, CLOCK[0]))
    os.makedirs("data/out", exist_ok=True)
    with open("data/out/manifest.csv", "w") as f:
        f.write("path,bytes,chunks,uploaded,status\n")
        for m in manifest:
            f.write(m + "\n")
    with open("data/out/backup.log", "w") as f:
        for line in lines:
            f.write(line + "\n")
    ROOT.removeHandler(handler)
    ROOT.addHandler(CAPTURE)
    for path in ("data/out/manifest.csv", "data/out/backup.log"):
        out("  == " + path)
        with open(path) as f:
            for line in f.read().splitlines():
                out("  " + line)


def main():
    with open("data/jobs.jsonl") as f:
        specs = [json.loads(line) for line in f.read().splitlines()]
    for spec in specs:
        out("== " + spec["name"])
        if "program" in spec:
            CLOCK[0] = spec["clock"]
            random.seed(spec["seed"])
            {"webhooks": webhooks, "backup": backup}[spec["program"]](spec)
        else:
            run_job(spec)
    sys.stdout.write("\n".join(OUT) + "\n")


main()
