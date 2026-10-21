# Writes data/: the jobs (data/jobs.jsonl), a webhook outbox with the
# replies its endpoints give (data/outbox.jsonl, data/endpoints.csv) and
# a backup set with the upload replies (data/backup.csv). Each job runs
# on its own fake clock, starting at its "clock", with random seeded
# with its "seed".
import json
import os

jobs = []


def job(name, script, config=None, mode="call", fn=("billing.client", "Client.fetch"),
        seed=1, clock=1000.0, log_level=10, **kw):
    d = {"name": name, "seed": seed, "clock": clock, "log_level": log_level,
         "mode": mode, "fn": {"module": fn[0], "qualname": fn[1]},
         "script": script, "config": config or {}}
    d.update(kw)
    jobs.append(d)


def boom(cls, msg=None, cost=0.25, **kw):
    d = {"raise": cls, "cost": cost}
    if msg is not None:
        d["msg"] = msg
    d.update(kw)
    return d


def ret(v, cost=0.25, **kw):
    d = {"return": v, "cost": cost}
    d.update(kw)
    return d


def log(name, level, **kw):
    d = {"log": [name, level]}
    d.update(kw)
    return d


TRACE = "trace"
STATS = "stats"


def attempts(n):
    return {"after_attempt": n}


def delay(x):
    return {"after_delay": x}


def before_delay(x):
    return {"before_delay": x}


def fixed(x):
    return {"fixed": x}


def exc(*types):
    return {"exc_type": list(types)}


# --- the controller -----------------------------------------------------

job("default retries until it works", [
    boom("ConnectionError", "connection refused"),
    boom("TimeoutError", "read timed out", cost=1.5),
    ret({"id": 7, "total": 12.5}),
])

job("stop after three attempts", [
    boom("ConnectionError", "connection refused"),
], {"stop": attempts(3), "wait": fixed(2),
    "before": log("billing", 20), "after": log("billing", 30),
    "before_sleep": log("billing", 30)})

job("reraise the last exception", [
    boom("ConnectionResetError", "Connection reset by peer", errno=104),
    boom("ConnectionRefusedError", "Connection refused", errno=111),
], {"stop": attempts(2), "reraise": True, "before_sleep": log("net", 30)})

job("a non-retryable exception goes straight out", [
    boom("ConnectionError", "refused"),
    boom("ValueError", "bad invoice id 'x9'"),
    ret("never reached"),
], {"retry": exc("ConnectionError", "TimeoutError"), "wait": fixed(0.5),
    "before_sleep": log("billing", 20)})

job("KeyboardInterrupt is not an Exception", [
    boom("ConnectionError", "refused"),
    boom("KeyboardInterrupt"),
], {"before_sleep": log("billing", 20)})

job("KeyError's str is its repr", [
    boom("KeyError", "user:41"),
    boom("KeyError"),
    ret(None),
], {"before_sleep": log("cache", 20), "after": TRACE})

job("retry on a result", [
    ret(None), ret([]), ret(0), ret({"rows": 3}),
], {"retry": {"result": {"falsy": 1}}, "wait": fixed(1),
    "before_sleep": log("poller", 20), "after": log("poller", 10)})

job("give up on a result: RetryError", [
    ret("pending"),
], {"retry": {"result": {"eq": "pending"}}, "stop": attempts(3),
    "wait": {"incrementing": [1, 2, 10]}})

job("give up on a result with reraise", [
    ret(503),
], {"retry": {"result": {"ge": 500}}, "stop": attempts(2), "reraise": True})

job("TryAgain retries without asking retry", [
    boom("TryAgain"), boom("TryAgain", "busy"), boom("ValueError", "nope"),
], {"retry": {"never": 1}, "before_sleep": log("jobs", 20), "after": TRACE})

job("retry_if_not_result and the unless type", [
    ret("queued"), ret("running"), boom("RuntimeError", "worker died"),
    ret("done"),
], {"retry": {"or": [{"not_result": {"eq": "done"}},
                     {"exc_type": ["RuntimeError"]}]},
    "before_sleep": log("jobs", 20)})

job("retry_unless_exception_type retries on results", [
    ret(1), ret(2), boom("FatalError", "disk full"),
], {"retry": {"unless_exc_type": ["FatalError"]}, "stop": attempts(5),
    "before_sleep": log("jobs", 20)})

job("retry_if_not_exception_type", [
    boom("TransientError", "flaky"), boom("RateLimited", "slow down"),
    boom("FatalError", "no such bucket"),
], {"retry": {"not_exc_type": ["FatalError"]}, "stop": attempts(9),
    "before_sleep": log("s3", 20)})

job("the cause chain", [
    boom("RuntimeError", "query failed", cause={"raise": "ConnectionResetError", "msg": "reset", "errno": 104}),
    boom("RuntimeError", "query failed", cause={"raise": "ValueError", "msg": "x",
                                                "cause": {"raise": "TimeoutError", "msg": "slow"}}),
    boom("RuntimeError", "query failed", cause={"raise": "ValueError", "msg": "bad sql"}),
], {"retry": {"exc_cause_type": ["ConnectionError", "TimeoutError"]},
    "before_sleep": log("db", 20)})

job("exception messages", [
    boom("RuntimeError", "lock busy"), boom("RuntimeError", "lock busy"),
    boom("RuntimeError", "lock busy: owner 7"), ret("ok"),
], {"retry": {"exc_message": {"message": "lock busy"}},
    "before_sleep": log("lock", 20)})

job("exception message prefixes", [
    boom("RuntimeError", "lock busy: owner 7"), boom("RuntimeError", "lock timeout"),
    boom("RuntimeError", "lock busy"),
], {"retry": {"exc_message": {"match": "lock busy"}},
    "before_sleep": log("lock", 20)})

job("not exception message retries on results too", [
    ret("ok"), boom("RuntimeError", "retry me"), boom("RuntimeError", "fatal"),
], {"retry": {"not_exc_message": {"message": "fatal"}}, "stop": attempts(5),
    "before_sleep": log("lock", 20)})

job("message and match together", [ret(1)],
    {"retry": {"exc_message": {"message": "a", "match": "b"}}})
job("neither message nor match", [ret(1)],
    {"retry": {"not_exc_message": {}}})
job("an empty message is no message", [ret(1)],
    {"retry": {"exc_message": {"message": "", "match": "busy"}}})

job("retry_all and retry_any, short-circuited", [
    boom("ConnectionError", "x"), ret(-1), ret(5), ret(42),
], {"retry": {"and": [{"or": [{"exc_type": None}, {"result": {"lt": 10}}]},
                      {"not_result": {"eq": 5}}]},
    "before_sleep": log("calc", 20)})

job("retry_always and stop_never with a stop", [ret("x")],
    {"retry": {"always": 1}, "stop": {"any": [{"never": 1}, attempts(4)]},
     "before_sleep": log("calc", 20)})

# --- stops --------------------------------------------------------------

job("stop after a delay", [
    boom("TimeoutError", "slow", cost=4),
], {"stop": delay(10), "wait": fixed(1.5), "before_sleep": log("api", 20),
    "after": log("api", 20, fmt="%.1f")})

job("stop before a delay", [
    boom("TimeoutError", "slow", cost=4),
], {"stop": before_delay(10), "wait": fixed(1.5), "before_sleep": log("api", 20),
    "after": log("api", 20, fmt="%d")})

job("stop delays as timedeltas", [
    boom("TimeoutError", "slow", cost=0.75),
], {"stop": {"or": [delay({"td": {"seconds": 2, "milliseconds": 500}}), attempts(10)]},
    "wait": fixed({"td": {"milliseconds": 250}}), "after": log("api", 20, fmt="%s"),
    "before_sleep": log("api", 20)})

job("stop when an event is set", [
    boom("ConnectionError", "down"), boom("ConnectionError", "down"),
    boom("ConnectionError", "down", set_event=True), boom("ConnectionError", "down"),
], {"stop": {"or": [{"event_set": 1}, attempts(9)]}, "wait": fixed(3),
    "before_sleep": log("svc", 20)})

job("stop_all needs every stop", [
    boom("ConnectionError", "down", cost=2),
], {"stop": {"and": [attempts(2), delay(9)]}, "wait": fixed(1),
    "before_sleep": log("svc", 20)})

job("stop_all of nested stops", [
    boom("ConnectionError", "down", cost=1),
], {"stop": {"all": [{"or": [attempts(6), delay(100)]}, {"any": [delay(4)]}]},
    "wait": fixed(0.5), "before_sleep": log("svc", 20)})

# --- waits --------------------------------------------------------------

job("wait_exponential with its defaults", [boom("ConnectionError", "down")],
    {"stop": attempts(6), "wait": {"exponential": {}}, "before_sleep": log("svc", 20),
     "after": STATS})

job("wait_exponential with a multiplier and limits", [boom("ConnectionError", "down")],
    {"stop": attempts(8),
     "wait": {"exponential": {"multiplier": 0.5, "min": 1, "max": 10}},
     "before_sleep": log("svc", 20)})

job("wait_exponential with a float base", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(7),
     "wait": {"exponential": {"multiplier": 3, "exp_base": 1.5, "max": 20.25}},
     "before_sleep": log("svc", 20)})

job("an exponent that overflows", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(34),
     "wait": {"exponential": {"multiplier": 1e-300, "exp_base": 1e10}},
     "after": STATS})

job("wait_incrementing", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(7), "wait": {"incrementing": [-3, 2, 4.5]},
     "before_sleep": log("svc", 20), "after": STATS})

job("wait_incrementing from zero", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(3), "wait": {"incrementing": [0, 0.1]}, "after": STATS})

job("wait_random", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(5), "wait": {"random": [1, 3]},
     "before_sleep": log("svc", 20)}, seed=42)

job("wait_random_exponential", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(7), "wait": {"random_exponential": {"multiplier": 0.5, "max": 8}},
     "before_sleep": log("svc", 20)}, seed=7)

job("wait_exponential_jitter", [boom("ConnectionError", "down", cost=0.125)],
    {"stop": attempts(7), "wait": {"exp_jitter": {"initial": 1, "max": 20, "jitter": 2}},
     "before_sleep": log("svc", 20), "after": STATS}, seed=2026)

job("wait_exponential_jitter with float settings", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(5), "wait": {"exp_jitter": {"initial": 0.1, "exp_base": 3, "jitter": 0.5}},
     "before_sleep": log("svc", 20)}, seed=3)

job("wait_chain", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(8), "wait": {"chain": [fixed(1), fixed(1), fixed(2), {"exponential": {"multiplier": 5}}]},
     "before_sleep": log("svc", 20)})

job("waits added together", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(5), "wait": {"plus": [fixed(3), {"random": [0, 2]}]},
     "before_sleep": log("svc", 20), "after": STATS}, seed=11)

job("sum() of waits", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(5),
     "wait": {"sum": [fixed(0.1), {"exponential": {}}, fixed(0.2), {"random": [0, 0.3]}]},
     "before_sleep": log("svc", 20), "after": STATS}, seed=5)

job("sum() of one wait is that wait", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(3), "wait": {"sum": [{"exponential": {}}]}, "after": STATS})

job("compensated sums of floats", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(4),
     "wait": {"combine": [fixed(0.1), fixed(0.2), fixed(0.3), fixed(1e16), fixed(1), fixed(-1e16)]},
     "before_sleep": log("svc", 20)})

job("an int added to a wait", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(3), "wait": {"radd": [5, fixed(1)]},
     "before_sleep": log("svc", 20)})

job("zero added to a wait", [boom("ConnectionError", "down", cost=0)],
    {"stop": attempts(3), "wait": {"radd": [0, fixed(1)]},
     "before_sleep": log("svc", 20)})

# --- callbacks ----------------------------------------------------------

job("retry_error_callback gets the last attempt", [boom("ConnectionError", "down")],
    {"stop": attempts(3), "error_callback": "attempts", "after": TRACE})

job("retry_error_callback with a fallback", [ret(None)],
    {"stop": attempts(2), "retry": {"result": {"is_none": 1}},
     "error_callback": {"fallback": {"cached": True, "rows": []}}})

job("retry_error_callback that re-raises", [boom("TimeoutError", "slow")],
    {"stop": attempts(2), "error_callback": "last_result"})

job("before, after and before_sleep logs", [
    boom("ConnectionError", "down", cost=0.3333),
    ret({"ok": True}, cost=0.0625),
], {"wait": fixed(1.25), "before": log("http", 10), "after": log("http", 10),
    "before_sleep": log("http", 30)}, log_level=10,
    fn=("", "fetch_profile"))

job("logger levels filter", [
    boom("ConnectionError", "down"), boom("ConnectionError", "down"), ret(1),
], {"before": log("quiet", 10), "after": log("loud", 25),
    "before_sleep": log("quiet", 40)}, log_level=30, loggers={"loud": 20},
    fn=("worker.tasks", "sync_inventory"))

job("a function with no module", [
    boom("ConnectionError", "down"), ret(2),
], {"before": log("x", 20), "before_sleep": log("x", 20)},
    fn=(None, "Outer.<locals>.inner"))

job("trace and stats callbacks", [
    boom("ConnectionError", "down", cost=0.1),
    boom("ConnectionError", "down", cost=0.2),
    ret("ok", cost=0.3),
], {"wait": {"random": [0.01, 0.03]}, "before": STATS, "after": TRACE,
    "before_sleep": TRACE}, seed=99)

job("slept rounds to two places", [
    boom("ConnectionError", "down", cost=0),
], {"stop": attempts(6), "wait": {"chain": [fixed(0.125), fixed(0.005), fixed(0.0049),
                                            fixed(1.115), fixed(2.675)]},
    "after": TRACE})

# --- calling it ---------------------------------------------------------

job("one Retrying called twice", [
    boom("ConnectionError", "down"), ret("a"),
    boom("ConnectionError", "down"), boom("ConnectionError", "down"), ret("b"),
], {"wait": fixed(1)}, calls=2)

job("the decorator", [
    boom("ConnectionError", "down"), ret("first"),
    boom("ConnectionError", "down"), ret("second"),
], {"wait": fixed(2), "before_sleep": log("deco", 20)}, mode="decorated", calls=2)

job("the bare decorator", [
    boom("ValueError", "x"), boom("ValueError", "y"), ret(3),
], {}, mode="bare", fn=("reports", "monthly"))

job("retry_with", [
    boom("ConnectionError", "down"),
], {"wait": fixed(2), "stop": attempts(4), "before_sleep": log("deco", 20)},
    mode="decorated", retry_with={"stop": attempts(2), "wait": fixed(0.5)})

job("the iterator", [
    boom("ConnectionError", "down"), boom("TimeoutError", "slow"), ret("ok"),
], {"stop": attempts(5), "wait": fixed(1), "before": log("loop", 20),
    "after": log("loop", 20), "before_sleep": log("loop", 20)}, mode="iter")

job("the iterator gives up", [
    boom("ConnectionError", "down"),
], {"stop": attempts(2), "after": TRACE}, mode="iter")

job("the iterator with reraise", [
    boom("ConnectionError", "down"),
], {"stop": attempts(2), "reraise": True}, mode="iter")

job("the iterator retries a None result", [
    ret("ignored"),
], {"stop": attempts(3), "retry": {"result": {"is_none": 1}}, "after": TRACE}, mode="iter")

job("the iterator lets a ValueError out", [
    boom("ConnectionError", "down"), boom("ValueError", "bad"),
], {"retry": exc("ConnectionError")}, mode="iter")

# --- the programs -------------------------------------------------------

jobs.append({"name": "webhook delivery", "program": "webhooks", "seed": 404, "clock": 5000.0})
jobs.append({"name": "backup upload", "program": "backup", "seed": 77, "clock": 86400.0})

os.makedirs("data", exist_ok=True)
with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j) + "\n")

# The outbox: one webhook per line. endpoints.csv says what each
# endpoint answers, one reply per attempt (the last one repeats):
# a status code, "reset" (ConnectionResetError), "refused"
# (ConnectionRefusedError) or "timeout" (TimeoutError), each with the
# seconds it takes after a colon.
outbox = [
    ("evt_001", "orders", "order.created", 1),
    ("evt_002", "billing", "invoice.paid", 2),
    ("evt_003", "crm", "contact.updated", 3),
    ("evt_004", "orders", "order.shipped", 1),
    ("evt_005", "legacy", "order.created", 4),
    ("evt_006", "slack", "alert.fired", 5),
    ("evt_007", "billing", "invoice.voided", 2),
    ("evt_008", "gone", "contact.deleted", 6),
    ("evt_009", "flaky", "order.created", 1),
    ("evt_010", "slowpoke", "report.ready", 7),
    ("evt_011", "crm", "contact.created", 3),
    ("evt_012", "ratelimited", "alert.fired", 5),
]
with open("data/outbox.jsonl", "w") as f:
    for i, ep, kind, tenant in outbox:
        f.write(json.dumps({"id": i, "endpoint": ep, "type": kind, "tenant": tenant}) + "\n")

endpoints = [
    ("orders", "https://orders.internal/hooks", "200:0.08"),
    ("billing", "https://billing.example.com/webhook", "503:0.2 503:0.2 202:0.1"),
    ("crm", "https://crm.example.org/in", "reset:0.05 timeout:5 200:0.3"),
    ("legacy", "http://10.0.4.7:8080/notify", "refused:0.01"),
    ("slack", "https://hooks.slack.example/T0/B0", "429:0.1 429:0.1 429:0.1 200:0.1"),
    ("gone", "https://old.example.net/hook", "410:0.05"),
    ("flaky", "https://flaky.example.io/h", "500:1 timeout:5 502:1 timeout:5 200:0.5"),
    ("slowpoke", "https://slow.example.com/hook", "timeout:9 timeout:9 timeout:9 timeout:9"),
    ("ratelimited", "https://rl.example.com/h", "429:0.5"),
]
with open("data/endpoints.csv", "w") as f:
    f.write("name,url,replies\n")
    for row in endpoints:
        f.write(",".join(row) + "\n")

# The backup set: each file is cut into 4 MiB chunks; replies are what
# the object store answers to each upload of a chunk, in order, the last
# one repeating: "ok", "busy" (TryAgain), "5xx" (a transient error),
# "denied" (a permanent one) and "slow" (an upload that takes 20 s).
backup = [
    ("db/2026-10-21.sql.gz", 9437184, "ok ok ok"),
    ("media/photos.tar", 16777216, "ok 5xx ok busy busy ok ok"),
    ("logs/app.log.1", 1048576, "5xx 5xx 5xx ok"),
    ("etc/secrets.env", 4096, "denied"),
    ("media/video.mp4", 12582912, "slow slow 5xx slow 5xx 5xx 5xx 5xx 5xx 5xx 5xx"),
    ("home/notes.md", 0, "ok"),
    ("db/2026-10-20.sql.gz", 8388608, "busy busy busy busy ok ok"),
]
with open("data/backup.csv", "w") as f:
    f.write("path,bytes,replies\n")
    for row in backup:
        f.write("%s,%d,%s\n" % row)
