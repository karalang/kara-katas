# Runs data/jobs.jsonl through limits itself (the copy in limits/,
# unchanged) and prints what mini_limits prints. The clock is set by the
# jobs: time.time is replaced by one that returns the job's time, and the
# memory storage's background expiry timer by one that never fires, so
# expired entries go only when a job sweeps them. limits imports the
# `deprecated` package for its version notes; the decorators it uses are
# stood in for here, since they only add to docstrings.
import json
import math
import os
import sys
import threading
import time
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
DATA = os.path.join(HERE, "data")

_dep = types.ModuleType("deprecated")
_sphinx = types.ModuleType("deprecated.sphinx")


def _note(*args, **kwargs):
    return lambda thing: thing


_sphinx.versionadded = _sphinx.versionchanged = _sphinx.deprecated = _note
_dep.sphinx = _sphinx
sys.modules["deprecated"] = _dep
sys.modules["deprecated.sphinx"] = _sphinx

CLOCK = [0.0]
time.time = lambda: CLOCK[0]


class Timer:
    def __init__(self, interval, function):
        self.function = function

    def start(self):
        pass

    def is_alive(self):
        return False


threading.Timer = Timer

import limits  # noqa: E402
from limits import parse_many  # noqa: E402
from limits._storage_scheme import parse_storage_uri  # noqa: E402
from limits.limits import GRANULARITIES  # noqa: E402
from limits.storage import MemoryStorage, storage_from_string  # noqa: E402
from limits.strategies import STRATEGIES  # noqa: E402
from limits.util import granularity_from_string  # noqa: E402


def failure(e):
    return f"! {type(e).__name__}: {e}"


def items_repr(items):
    return "[" + ", ".join(repr(i) for i in items) + "]"


def op_parse(op):
    text = op["text"]
    try:
        items = parse_many(text)
    except Exception as e:
        print(f"{text!r}: {failure(e)}")
        return
    print(f"{text!r}: {items_repr(items)}")
    for i in items:
        print(f"  {type(i).__name__} expiry={i.get_expiry()} key={i.key_for('203.0.113.5')!r}")


def op_parse_bytes(op):
    b = bytes.fromhex(op["hex"])
    try:
        print(f"{b!r}: {items_repr(parse_many(b))}")
    except Exception as e:
        print(f"{b!r}: {failure(e)}")


def item_class(name):
    return GRANULARITIES[name]


def op_item(op):
    cls = item_class(op["cls"])
    item = cls(op["amount"], op["multiples"], namespace=op["namespace"])
    print(f"{cls.__name__}({op['amount']!r}, {op['multiples']!r}, namespace={op['namespace']!r}): {item!r}"
          f" expiry={item.get_expiry()}")
    print(f"  key {item.key_for(*op['ids'])!r}")


def op_key_for(op):
    item = limits.parse(op["limit"])
    print(f"key_for{tuple(op['ids'])!r} of {item!r}: {item.key_for(*op['ids'])!r}")


def op_key_for_bytes(op):
    item = limits.parse(op["limit"])
    b = bytes.fromhex(op["hex"])
    print(f"key_for({b!r}) of {item!r}: {item.key_for(b)!r}")


def op_compare(op):
    a, b = limits.parse(op["a"]), limits.parse(op["b"])
    print(f"{a!r} vs {b!r}: == {a == b}, < {a < b}, <= {a <= b}, > {a > b}, >= {a >= b}")


def op_compare_ns(op):
    a = limits.parse(op["a"])
    a.namespace = op["na"]
    b = limits.parse(op["b"])
    b.namespace = op["nb"]
    print(f"{a!r} in {a.namespace!r} vs {b!r} in {b.namespace!r}: == {a == b}"
          f", keys {a.key_for('x')!r} {b.key_for('x')!r}")


def op_sort(op):
    items = [limits.parse(s) for s in op["limits"]]
    print(f"sorted {items_repr(items)}")
    print(f"  -> {items_repr(sorted(items))}")
    print(f"  min {min(items)!r}, max {max(items)!r}")


def op_granularity(op):
    for text in op["texts"]:
        try:
            print(f"granularity {text!r}: {granularity_from_string(text).__name__}")
        except ValueError as e:
            print(f"granularity {text!r}: {failure(e)}")


# ------------------------------------------------------------ storage


def storage_state(st):
    counters = ", ".join(f"{k}={st.storage[k]}@{st.expirations.get(k)!r}" for k in sorted(st.storage))
    events = ", ".join(f"{k}:{len(v)}" for k, v in sorted(st.events.items()))
    return f"counters [{counters}] events [{events}] expirations {len(st.expirations)}"


def op_storage(op, st):
    kind = op["op"]
    if kind == "at":
        CLOCK[0] = op["t"]
        print(f"at {CLOCK[0]!r}")
    elif kind == "advance":
        CLOCK[0] += op["dt"]
        print(f"at {CLOCK[0]!r}")
    elif kind == "check":
        print(f"check -> {st.check()}")
    elif kind == "incr":
        print(f"incr {op['key']} {op['expiry']} +{op['amount']} -> {st.incr(op['key'], op['expiry'], amount=op['amount'])}")
    elif kind == "decr":
        print(f"decr {op['key']} -{op['amount']} -> {st.decr(op['key'], amount=op['amount'])}")
    elif kind == "get":
        print(f"get {op['key']} -> {st.get(op['key'])}")
    elif kind == "get_expiry":
        print(f"get_expiry {op['key']} -> {st.get_expiry(op['key'])!r}")
    elif kind == "clear":
        st.clear(op["key"])
        print(f"clear {op['key']}")
    elif kind == "acquire":
        r = st.acquire_entry(op["key"], op["limit"], op["expiry"], amount=op["amount"])
        print(f"acquire_entry {op['key']} limit={op['limit']} expiry={op['expiry']} amount={op['amount']} -> {r}")
    elif kind == "window":
        print(f"get_moving_window {op['key']} -> {st.get_moving_window(op['key'], op['limit'], op['expiry'])!r}")
    elif kind == "acquire_sliding":
        r = st.acquire_sliding_window_entry(op["key"], op["limit"], op["expiry"], op["amount"])
        print(f"acquire_sliding_window_entry {op['key']} limit={op['limit']} expiry={op['expiry']} "
              f"amount={op['amount']} -> {r}")
    elif kind == "sliding":
        print(f"get_sliding_window {op['key']} -> {st.get_sliding_window(op['key'], op['expiry'])!r}")
    elif kind == "clear_sliding":
        st.clear_sliding_window(op["key"], op["expiry"])
        print(f"clear_sliding_window {op['key']}")
    elif kind == "reset":
        print(f"reset -> {st.reset()!r}")
    elif kind == "state":
        print("state " + storage_state(st))
    elif kind == "sweep":
        st._MemoryStorage__expire_events()
        print("sweep")


def op_strategy_step(op, limiter):
    kind = op["op"]
    if kind == "at":
        CLOCK[0] = op["t"]
        return
    item = limits.parse(op["limit"])
    ids = op["ids"]
    head = f"{CLOCK[0]!r} {kind} {item!r} {'/'.join(ids)}"
    if kind == "hit":
        print(f"{head} cost={op['cost']} -> {limiter.hit(item, *ids, cost=op['cost'])}")
    elif kind == "test":
        print(f"{head} cost={op['cost']} -> {limiter.test(item, *ids, cost=op['cost'])}")
    elif kind == "stats":
        print(f"{head} -> {limiter.get_window_stats(item, *ids)!r}")
    elif kind == "clear":
        limiter.clear(item, *ids)
        print(head)


# ------------------------------------------------------------ storage URIs


def op_uri(op):
    text = op["text"]
    try:
        o = parse_storage_uri(text)
        print(f"{text!r}: {o!r} empty={o.empty}")
    except Exception as e:
        print(f"{text!r}: {failure(e)}")


def op_from_string(op):
    text = op["text"]
    try:
        st = storage_from_string(text)
        cls = type(st)
        print(f"storage_from_string({text!r}): {cls.__module__}.{cls.__qualname__}")
    except Exception as e:
        print(f"storage_from_string({text!r}): {failure(e)}")


# ------------------------------------------------------------ the gateway


def read_lines(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip() and not line.startswith("#")]


def stats_text(item, stats):
    return f"limit={item!r} remaining={stats.remaining} reset={stats.reset_time!r}"


def op_gateway():
    storage = MemoryStorage()
    limiters = {name: cls(storage) for name, cls in STRATEGIES.items()}
    default = []
    exempt = set()
    routes = {}
    for line in read_lines("routes.conf"):
        words = line.split()
        if words[0] == "default":
            default = parse_many(" ".join(words[1:]))
        elif words[0] == "exempt":
            exempt.add(words[1])
        elif words[0] == "route":
            method, path, strategy = words[1], words[2], words[3]
            rest = words[4:]
            cost = None
            if rest[-1].startswith("cost="):
                cost = rest.pop()[5:]
            key = rest.pop()
            text = " ".join(rest)
            items = default if text == "-" else parse_many(text)
            routes[(method, path)] = (strategy, items, key, cost)
            print(f"route {method} {path}: {strategy} {items_repr(items)} by {key}" + (f" cost={cost}" if cost else ""))
    paths = {p for (_, p) in routes}
    counts = {}
    refused = {}
    for line in read_lines("access.log"):
        t, ip, user, api_key, method, path, rows = line.split()
        now = float(t)
        CLOCK[0] = now
        head = f"{now!r} {ip} {method} {path}"
        route = routes.get((method, path))
        if route is None:
            status = 405 if path in paths else 404
            print(f"{head} -> {status}")
            counts[(f"{method} {path}", status)] = counts.get((f"{method} {path}", status), 0) + 1
            continue
        strategy, items, key_kind, cost_kind = route
        scope = f"{method} {path}"
        if ip in exempt:
            print(f"{head} -> 200 exempt")
            counts[(scope, 200)] = counts.get((scope, 200), 0) + 1
            continue
        key = {"ip": ip, "user": user, "key": api_key}[key_kind]
        if key == "-":
            key = ip
        cost = max(1, int(rows)) if cost_kind == "rows" else 1
        limiter = limiters[strategy]
        breached = None
        for item in items:
            if not limiter.hit(item, scope, key, cost=cost):
                breached = item
                break
        if breached is not None:
            stats = limiter.get_window_stats(breached, scope, key)
            retry = math.ceil(stats.reset_time - now)
            print(f"{head} as {key} cost={cost} -> 429 {stats_text(breached, stats)} retry-after={retry}")
            counts[(scope, 429)] = counts.get((scope, 429), 0) + 1
            refused[key] = refused.get(key, 0) + 1
            continue
        current, stats = None, None
        for item in items:
            s = limiter.get_window_stats(item, scope, key)
            if stats is None or s.remaining < stats.remaining:
                current, stats = item, s
        print(f"{head} as {key} cost={cost} -> 200 {stats_text(current, stats)}")
        counts[(scope, 200)] = counts.get((scope, 200), 0) + 1
    print("responses:")
    for (scope, status) in sorted(counts):
        print(f"  {scope} {status}: {counts[(scope, status)]}")
    print("refused clients:")
    for key in sorted(refused, key=lambda k: (-refused[k], k)):
        print(f"  {key}: {refused[key]}")
    print(f"storage: {len(storage.storage)} counters, {len(storage.events)} moving windows")


def op_logins():
    limiter = STRATEGIES["moving-window"](MemoryStorage())
    per_user = limits.parse("3/minute")
    per_ip = limits.parse("10/hour")
    blocked = {}
    for line in read_lines("logins.log"):
        t, ip, user, outcome = line.split()
        now = float(t)
        CLOCK[0] = now
        head = f"{now!r} {ip} {user}"
        stop = None
        for item, ident in ((per_ip, ip), (per_user, user)):
            if not limiter.test(item, "login", ident):
                stop = (item, ident)
                break
        if stop is not None:
            stats = limiter.get_window_stats(stop[0], "login", stop[1])
            print(f"{head}: blocked by {stop[0]!r} for {stop[1]}, retry in {math.ceil(stats.reset_time - now)}s")
            blocked[ip] = blocked.get(ip, 0) + 1
            continue
        limiter.hit(per_ip, "login", ip)
        limiter.hit(per_user, "login", user)
        if outcome == "ok":
            limiter.clear(per_user, "login", user)
            print(f"{head}: signed in, {limiter.get_window_stats(per_ip, 'login', ip).remaining} left for {ip}")
        else:
            stats = limiter.get_window_stats(per_user, "login", user)
            print(f"{head}: wrong password, {stats.remaining} left for {user}"
                  f" (window from {stats.reset_time - per_user.get_expiry()!r})")
    for ip in sorted(blocked):
        print(f"blocked {ip}: {blocked[ip]}")


def op_exports():
    limiter = STRATEGIES["sliding-window-counter"](MemoryStorage())
    quota = limits.parse("1000/hour")
    done = {}
    for line in read_lines("exports.log"):
        t, tenant, rows = line.split()
        now = float(t)
        CLOCK[0] = now
        n = int(rows)
        ok = limiter.hit(quota, "export", tenant, cost=n)
        stats = limiter.get_window_stats(quota, "export", tenant)
        print(f"{now!r} {tenant} {n} rows -> {'accepted' if ok else 'refused'}, remaining={stats.remaining}"
              f" reset={stats.reset_time!r}")
        a, r = done.get(tenant, (0, 0))
        done[tenant] = (a + n, r) if ok else (a, r + n)
    for tenant in sorted(done):
        print(f"{tenant}: {done[tenant][0]} rows exported, {done[tenant][1]} refused")


def op_boundary(op):
    item = limits.parse(op["limit"])
    names = ["fixed-window", "moving-window", "sliding-window-counter"]
    limiters = [STRATEGIES[n](MemoryStorage()) for n in names]
    print(f"{item!r}: " + " | ".join(names))
    taken = [0, 0, 0]
    for t in op["times"]:
        CLOCK[0] = t
        cells = []
        for k, limiter in enumerate(limiters):
            ok = limiter.hit(item, "client")
            taken[k] += ok
            stats = limiter.get_window_stats(item, "client")
            cells.append(f"{'ok ' if ok else '429'} {stats.remaining} {stats.reset_time!r}")
        print(f"{t!r}: " + " | ".join(cells))
    print("served: " + ", ".join(f"{n} {c}" for n, c in zip(names, taken)))


def main():
    with open(os.path.join(DATA, "jobs.jsonl"), encoding="utf-8") as f:
        jobs = [json.loads(line) for line in f]
    for j in jobs:
        print("== " + j["name"])
        storage = None
        limiter = None
        for op in j["ops"]:
            kind = op["op"]
            if kind == "parse":
                op_parse(op)
            elif kind == "parse_bytes":
                op_parse_bytes(op)
            elif kind == "item":
                op_item(op)
            elif kind == "key_for":
                op_key_for(op)
            elif kind == "key_for_bytes":
                op_key_for_bytes(op)
            elif kind == "compare":
                op_compare(op)
            elif kind == "compare_ns":
                op_compare_ns(op)
            elif kind == "sort":
                op_sort(op)
            elif kind == "granularity":
                op_granularity(op)
            elif kind == "strategy":
                limiter = STRATEGIES[op["name"]](MemoryStorage())
            elif kind == "uri":
                op_uri(op)
            elif kind == "from_string":
                op_from_string(op)
            elif kind == "gateway":
                op_gateway()
            elif kind == "logins":
                op_logins()
            elif kind == "exports":
                op_exports()
            elif kind == "boundary":
                op_boundary(op)
            elif limiter is not None:
                op_strategy_step(op, limiter)
            else:
                if storage is None:
                    storage = MemoryStorage()
                op_storage(op, storage)


if __name__ == "__main__":
    main()
