# Runs data/jobs.jsonl through cachetools 7.2.3 (the package here) and
# prints what mini_cachetools prints. Run mk.py first.
#
# LFUCache keeps the keys of each use count in a Python set and evicts
# whichever comes first in it, so the run pins PYTHONHASHSEED=0 to make
# str hashes, and so that order, the same on every run.
#
# The caches get a clock of the job's own (it starts at "start" and moves
# on by "step" every time it is read, and "tick" moves it on), and
# RRCache gets a choice function that takes the job's "picks" in turn.
import json
import os
import sys
import warnings

if os.environ.get("PYTHONHASHSEED") != "0":
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cachetools  # noqa: E402
from cachetools import func, keys  # noqa: E402

out = []


def emit(s):
    out.append(s)


def val(x):
    if isinstance(x, list):
        return tuple(val(y) for y in x)
    return x


class Clock:
    def __init__(self, start, step):
        self.t = start
        self.step = step

    def __call__(self):
        v = self.t
        self.t += self.step
        return v


class Picks:
    def __init__(self, picks):
        self.picks = picks
        self.n = 0

    def __call__(self, seq):
        k = self.picks[self.n % len(self.picks)]
        self.n += 1
        return seq[k % len(seq)]


def sizeof(kind):
    if kind == "len":
        return len
    if kind == "checked":
        return lambda v: -1 if isinstance(v, str) and v.startswith("!") else len(v)
    return None


def ttu(spec):
    if spec["kind"] == "fixed":
        n = spec["n"]
        return lambda key, value, time: time + n
    if spec["kind"] == "len":
        return lambda key, value, time: time + len(value)
    table = spec["table"]
    default = spec["default"]
    return lambda key, value, time: time + table.get(key, default)


def make_cache(spec, clock):
    t = spec["type"]
    m = spec["maxsize"]
    g = sizeof(spec.get("getsizeof"))
    if t == "Cache":
        return cachetools.Cache(m, g)
    if t == "FIFOCache":
        return cachetools.FIFOCache(m, g)
    if t == "LFUCache":
        return cachetools.LFUCache(m, g)
    if t == "LRUCache":
        return cachetools.LRUCache(m, g)
    if t == "RRCache":
        return cachetools.RRCache(m, Picks(spec["picks"]), g)
    if t == "TTLCache":
        return cachetools.TTLCache(m, spec["ttl"], clock, g)
    if t == "TLRUCache":
        return cachetools.TLRUCache(m, ttu(spec["ttu"]), clock, g)
    raise ValueError(t)


def do(c, clock, op):
    name = op[0]
    a = [val(x) for x in op[1:]]
    if name == "set":
        c[a[0]] = a[1]
        return None
    if name == "getitem":
        return c[a[0]]
    if name == "get":
        return c.get(*a)
    if name == "del":
        del c[a[0]]
        return None
    if name == "pop":
        return c.pop(*a)
    if name == "popitem":
        return c.popitem()
    if name == "setdefault":
        return c.setdefault(*a)
    if name == "in":
        return a[0] in c
    if name == "len":
        return len(c)
    if name == "currsize":
        return c.currsize
    if name == "maxsize":
        return c.maxsize
    if name == "repr":
        return Raw(repr(c))
    if name == "list":
        return list(c)
    if name == "items":
        return list(c.items())
    if name == "values":
        return list(c.values())
    if name == "update":
        c.update(a[0])
        return None
    if name == "expire":
        return c.expire(*a)
    if name == "clear":
        c.clear()
        return None
    if name == "tick":
        clock.t += a[0]
        return Raw("now %r" % clock.t)
    raise ValueError(name)


class Raw:
    def __init__(self, s):
        self.s = s


def show(r):
    return r.s if isinstance(r, Raw) else repr(r)


def args_text(op):
    return " ".join(repr(val(x)) for x in op[1:])


def run_script(j):
    clock = Clock(j.get("start", 0), j.get("step", 0))
    try:
        c = make_cache(j["cache"], clock)
    except ValueError as e:
        emit("  new -> %r" % e)
        return
    for op in j["ops"]:
        head = ("  %s %s" % (op[0], args_text(op))).rstrip()
        try:
            r = do(c, clock, op)
            emit("%s -> %s" % (head, show(r)))
        except (KeyError, ValueError, TypeError) as e:
            emit("%s -> %r" % (head, e))


# ------------------------------------------------------------ memoizing

PROFILES = {1: "ada", 2: "grace", 3: "linus", 4: "margaret", 5: "ken", 7: "barbara"}
PRICES = {"apple": 30, "pear": 45, "fig": 120, "kiwi": 25}
PAGES = {"home": 40, "about": 12, "docs": 75, "blog": 33}
calls = []


def fib_impl(n):
    calls.append("fib(%d)" % n)
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def user_impl(uid):
    calls.append("user(%r)" % (uid,))
    if uid in PROFILES:
        return "%s#%d" % (PROFILES[uid], uid)
    return None


def price_impl(sku, qty=1, currency="EUR"):
    calls.append("price(%r, qty=%r, currency=%r)" % (sku, qty, currency))
    return (sku, PRICES.get(sku, 0) * qty, currency)


def render_impl(page, lang="en"):
    calls.append("render(%r, %r)" % (page, lang))
    n = PAGES.get(page, 5)
    return ("<%s:%s>" % (lang, page)).ljust(n, "~")


IMPLS = {"fib": fib_impl, "user": user_impl, "price": price_impl, "render": render_impl}
fib = None


def make_wrapper(j, clock):
    impl = IMPLS[j["func"]]
    d = j["decorator"]
    if d == "cached":
        spec = j.get("cache")
        cache = None if spec is None else ({} if spec == "dict" else make_cache(spec, clock))
        key = keys.typedkey if j.get("typed") else keys.hashkey
        lock = None
        if j.get("lock"):
            import threading
            lock = threading.RLock()
        return cachetools.cached(cache, key=key, lock=lock, info=j.get("info", False))(impl)
    m = j.get("maxsize", 128)
    typed = j.get("typed", False)
    if d == "lru_cache":
        return func.lru_cache(maxsize=m, typed=typed)(impl)
    if d == "fifo_cache":
        return func.fifo_cache(maxsize=m, typed=typed)(impl)
    if d == "lfu_cache":
        return func.lfu_cache(maxsize=m, typed=typed)(impl)
    if d == "rr_cache":
        return func.rr_cache(maxsize=m, choice=Picks(j["picks"]), typed=typed)(impl)
    if d == "ttl_cache":
        return func.ttl_cache(maxsize=m, ttl=j["ttl"], timer=clock, typed=typed)(impl)
    raise ValueError(d)


def run_memo(j):
    global fib
    clock = Clock(j.get("start", 0), j.get("step", 0))
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        w = make_wrapper(j, clock)
        for x in rec:
            emit("  warning: %s: %s" % (x.category.__name__, x.message))
    if j["func"] == "fib":
        fib = w
    for call in j["calls"]:
        if call[0] == "info":
            emit("  cache_info -> %r" % (w.cache_info(),))
            continue
        if call[0] == "params":
            emit("  cache_parameters -> %r" % (w.cache_parameters(),))
            continue
        if call[0] == "clear":
            w.cache_clear()
            emit("  cache_clear")
            continue
        if call[0] == "cache":
            emit("  cache -> %r" % (w.cache,))
            continue
        if call[0] == "tick":
            clock.t += call[1]
            emit("  now %r" % clock.t)
            continue
        args = [val(x) for x in call[1]]
        kw = call[2] if len(call) > 2 else {}
        del calls[:]
        r = w(*args, **kw)
        parts = [repr(x) for x in args] + ["%s=%r" % kv for kv in kw.items()]
        emit("  %s(%s) -> %r" % (j["func"], ", ".join(parts), r))
        if calls:
            emit("    ran " + " ".join(calls))


def run_key(j):
    for call in j["calls"]:
        args = [val(x) for x in call[0]]
        kw = call[1] if len(call) > 1 else {}
        f = keys.typedkey if j["typed"] else keys.hashkey
        k = f(*args, **kw)
        emit("  %r" % (k,))


RUN = {"script": run_script, "memo": run_memo, "key": run_key}


def describe(j):
    if j["kind"] == "script":
        s = j["cache"]
        parts = ["%s=%r" % (k, s[k]) for k in s if k != "type"]
        return "%s(%s)" % (s["type"], ", ".join(parts))
    if j["kind"] == "memo":
        parts = ["%s=%r" % (k, j[k]) for k in j if k not in ("kind", "calls", "func", "decorator")]
        return "%s %s(%s)" % (j["func"], j["decorator"], ", ".join(parts))
    return "typedkey" if j["typed"] else "hashkey"


def main():
    emit("cachetools %s" % cachetools.__version__)
    with open("data/jobs.jsonl", encoding="utf-8") as f:
        jobs = [json.loads(l) for l in f if l.strip()]
    for k, j in enumerate(jobs):
        emit("job %d: %s %s" % (k + 1, j["kind"], describe(j)))
        RUN[j["kind"]](j)
    sys.stdout.write("\n".join(out) + "\n")


main()
