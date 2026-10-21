# Writes data/: the jobs mini_limits runs (data/jobs.jsonl) and the files
# its programs read: an API gateway's routes and access log, a login
# log and a data-export log. Times are seconds since the epoch, as
# time.time() gives them; the runs set the clock themselves.
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

T0 = 1700000000.0
jobs = []


def job(name, ops):
    jobs.append({"name": name, "ops": ops})


# ------------------------------------------------------------ strings

STRINGS = [
    "10/minute", "10 per minute", "10 per 1 minute", "10/2 minutes", "1/second", "1 per seconds",
    "100/hour", "1000/day", "5/month", "2/year", "30 per 5 minute", "7 PER HOUR", "7 Per Hours",
    "10 / Minutes", "  3/second  ", "3 /second", "3/ second", "3per second", "3 persecond",
    "1/second; 5/minute", "1/second,5/minute", "1/second|5/minute", "1/second ; 5 / minute ; 100/day",
    "5 per 2 hours; 1/second", "100/day;10/hour;1/minute", "1/second:,2/day", "1/second:;2/day",
    "1/second::2/day", "1/second;;2/day", "1/second;", ";1/second", "1 per 0 minute", "0/second",
    "007/minute", "1/007 minute", "9223372036854775807/second", "1/second\n", "\n1/second",
    "1/second\n\n", "1/\tsecond", "1 per minute", "1/sec", "1/min", "1/hr", "3/fortnight",
    "1/ſecond", "1/Kelvin", "１０/minute", "1/MINUTE", "1/Minutess", "1/2/3", "", " ",
    "per minute", "10", "10/", "/minute", "10 minute", "10/minute/5", "-1/second", "1.5/second",
    "1/1.5 second", "ten/minute", "1/secondly", "1/days", "1/years", "1/months", "1/hours",
    "1/seconds;1/minutes;1/hours;1/days;1/months;1/years",
]
job("rate limit strings", [{"op": "parse", "text": s} for s in STRINGS]
    + [{"op": "parse_bytes", "hex": b"1/second".hex()}, {"op": "parse_bytes", "hex": b"x".hex()}])

ITEMS = [
    ("minute", 10, 1, "LIMITER"), ("minute", 10, 2, "LIMITER"), ("second", 5, None, "api"),
    ("hour", 100, 0, "api"), ("day", 1000, 1, "uploads"), ("month", 5, 3, "billing"),
    ("year", 2, 1, "LIMITER"), ("second", "7", "2", "LIMITER"), ("minute", 2.9, 1.9, "LIMITER"),
    ("hour", 1, -1, "neg"), ("day", 0, 1, "zero"), ("second", True, 1, "LIMITER"),
]
item_ops = []
for cls, amount, multiples, ns in ITEMS:
    item_ops.append({"op": "item", "cls": cls, "amount": amount, "multiples": multiples, "namespace": ns,
                     "ids": ["203.0.113.5", 42, 1.5, "GET /api/v1/orders"]})
item_ops.append({"op": "key_for", "limit": "10/minute", "ids": []})
item_ops.append({"op": "key_for", "limit": "10/minute", "ids": ["user", 7, -2, 3.25, 1e20, "a/b"]})
item_ops.append({"op": "key_for_bytes", "limit": "10/minute", "hex": "café".encode().hex()})
PAIRS = [("10/minute", "10 per 1 minute"), ("10/minute", "10/2 minutes"), ("10/minute", "10/hour"),
         ("10/minute", "5/minute"), ("1/day", "24/hour"), ("60/minute", "1/second"), ("1/second", "1/second")]
for a, b in PAIRS:
    item_ops.append({"op": "compare", "a": a, "b": b})
item_ops.append({"op": "compare_ns", "a": "10/minute", "na": "api", "b": "10/minute", "nb": "web"})
item_ops.append({"op": "sort", "limits": ["1/day", "10/minute", "5/second", "100/hour", "3/minute", "2/second",
                                          "1/year", "7/month", "4/2 minutes", "9/hour"]})
item_ops.append({"op": "granularity", "texts": ["second", "seconds", "SECOND", "Minutes", "minutess", "sec",
                                                "", "hour", "hours", "day", "month", "year", "years", "week"]})
job("rate limit items", item_ops)

# ------------------------------------------------------------ memory storage

S = []
S += [{"op": "at", "t": T0}, {"op": "check"}]
S += [{"op": "incr", "key": "k1", "expiry": 60, "amount": 1}] * 3
S += [{"op": "get", "key": "k1"}, {"op": "get_expiry", "key": "k1"}, {"op": "get", "key": "nope"},
      {"op": "get_expiry", "key": "nope"}]
S += [{"op": "at", "t": T0 + 30.5}, {"op": "incr", "key": "k1", "expiry": 60, "amount": 2},
      {"op": "get_expiry", "key": "k1"}, {"op": "decr", "key": "k1", "amount": 1}, {"op": "get", "key": "k1"},
      {"op": "decr", "key": "k1", "amount": 10}, {"op": "get", "key": "k1"},
      {"op": "incr", "key": "k1", "expiry": 60, "amount": 0}, {"op": "get_expiry", "key": "k1"}]
S += [{"op": "decr", "key": "fresh", "amount": 1}, {"op": "get", "key": "fresh"},
      {"op": "incr", "key": "k2", "expiry": 10, "amount": 5}, {"op": "get_expiry", "key": "k2"}]
S += [{"op": "at", "t": T0 + 40.5}, {"op": "get", "key": "k2"}, {"op": "at", "t": T0 + 40.499}]
S += [{"op": "get", "key": "k2"}, {"op": "at", "t": T0 + 90.5}, {"op": "get", "key": "k1"},
      {"op": "incr", "key": "k1", "expiry": 60, "amount": 1}, {"op": "get_expiry", "key": "k1"}]
# moving window entries
S += [{"op": "at", "t": T0 + 100}]
for k in range(4):
    S += [{"op": "acquire", "key": "mw", "limit": 3, "expiry": 10, "amount": 1}, {"op": "advance", "dt": 1.25}]
S += [{"op": "window", "key": "mw", "limit": 3, "expiry": 10},
      {"op": "acquire", "key": "mw", "limit": 3, "expiry": 10, "amount": 4},
      {"op": "acquire", "key": "mw2", "limit": 5, "expiry": 10, "amount": 3},
      {"op": "acquire", "key": "mw2", "limit": 5, "expiry": 10, "amount": 3},
      {"op": "acquire", "key": "mw2", "limit": 5, "expiry": 10, "amount": 2},
      {"op": "window", "key": "mw2", "limit": 5, "expiry": 10}, {"op": "window", "key": "none", "limit": 5, "expiry": 10},
      {"op": "advance", "dt": 7.5}, {"op": "window", "key": "mw", "limit": 3, "expiry": 10},
      {"op": "acquire", "key": "mw", "limit": 3, "expiry": 10, "amount": 1},
      {"op": "advance", "dt": 30}, {"op": "window", "key": "mw", "limit": 3, "expiry": 10},
      {"op": "state"}, {"op": "sweep"}, {"op": "state"}, {"op": "window", "key": "mw", "limit": 3, "expiry": 10}]
# sliding window counters
S += [{"op": "at", "t": T0 + 7}, {"op": "sliding", "key": "sw", "expiry": 60}]
for k in range(6):
    S += [{"op": "acquire_sliding", "key": "sw", "limit": 5, "expiry": 60, "amount": 1}]
S += [{"op": "sliding", "key": "sw", "expiry": 60}, {"op": "advance", "dt": 50.75},
      {"op": "sliding", "key": "sw", "expiry": 60}]
for k in range(4):
    S += [{"op": "acquire_sliding", "key": "sw", "limit": 5, "expiry": 60, "amount": 1},
          {"op": "advance", "dt": 6.5}, {"op": "sliding", "key": "sw", "expiry": 60}]
S += [{"op": "acquire_sliding", "key": "sw", "limit": 5, "expiry": 60, "amount": 9},
      {"op": "acquire_sliding", "key": "sw", "limit": 5, "expiry": 60, "amount": 2},
      {"op": "state"}, {"op": "clear_sliding", "key": "sw", "expiry": 60}, {"op": "sliding", "key": "sw", "expiry": 60},
      {"op": "clear", "key": "mw2"}, {"op": "state"}, {"op": "reset"}, {"op": "reset"}, {"op": "state"}]
job("memory storage", S)

# ------------------------------------------------------------ strategies


def strategy_ops(limit, times, ids=("alice",), cost=1):
    ops = []
    for t, what in times:
        ops.append({"op": "at", "t": T0 + t})
        ops.append({"op": what, "limit": limit, "ids": list(ids), "cost": cost})
    return ops


for strat in ["fixed-window", "moving-window", "sliding-window-counter"]:
    ops = []
    plan = [(0, "hit"), (0, "stats"), (1.5, "hit"), (2, "hit"), (2, "test"), (2.5, "hit"), (2.5, "stats"),
            (3, "hit"), (3, "test"), (59.5, "hit"), (59.5, "stats"), (60.25, "test"), (60.25, "hit"),
            (60.25, "stats"), (75, "hit"), (75, "stats"), (119.75, "hit"), (130, "stats"), (200, "test"),
            (200, "stats"), (200, "hit"), (200, "clear"), (200, "stats"), (200, "hit")]
    ops += strategy_ops("4/minute", plan)
    ops += strategy_ops("4/minute", [(300, "hit"), (300, "stats")], ids=("bob", "GET /orders"), cost=3)
    ops += strategy_ops("4/minute", [(301, "test"), (301, "hit"), (301, "stats")], ids=("bob", "GET /orders"), cost=2)
    ops += strategy_ops("4/minute", [(302, "hit"), (302, "stats")], ids=("bob", "GET /orders"), cost=1)
    ops += strategy_ops("4/minute", [(303, "hit"), (303, "test")], ids=("carol",), cost=5)
    ops += strategy_ops("4/minute", [(304, "hit"), (304, "test"), (304, "stats")], ids=("dave",), cost=0)
    ops += strategy_ops("2/second", [(400.1, "hit"), (400.2, "hit"), (400.3, "hit"), (400.9, "stats"),
                                     (401.05, "hit"), (401.15, "stats"), (401.95, "hit"), (402.5, "stats")])
    ops += strategy_ops("3/2 seconds", [(500, "hit"), (500.5, "hit"), (501, "hit"), (501.5, "hit"),
                                        (502.25, "hit"), (502.25, "stats"), (503, "hit"), (504.75, "stats")])
    job(f"strategy {strat}", [{"op": "strategy", "name": strat}] + ops)

# ------------------------------------------------------------ storage URIs

URIS = [
    "redis://localhost:6379", "redis://user:pw@localhost:6379/0?ssl=true&x=1&x=2", "redis://:secret@cache:6380/2",
    "memcached://a:11211, b:11212,c:11213", "memcached:///var/run/memcached.sock", "redis://localhost",
    "redis://h:99999", "redis://h:abc", "redis://h:", "redis+unix:///tmp/r.sock?db=1", "redis://[::1]:6379",
    "redis://[2001:db8::7]:6379,[2001:db8::8]:6380", "redis://[::1", "redis+cluster://a:7000,b:7001",
    "redis+sentinel://s1:26379,s2:26379/mymaster", "memory://", "memory:///", "MEMORY://", "mongodb://u:p@db:27017/limits?authSource=admin",
    "redis://h:1?a=1&b&c=&d=%20x+y", "redis://u%40x:p%3A@h:1", "redis://h:0", "redis://h:65535", "redis://h:65536",
    "redis://h: 1", "redis://h:1,,", "redis://,h:1", "redis://@h:1", "redis://u@", "x:y",
]
uri_ops = [{"op": "uri", "text": u} for u in URIS]
FROM = [
    "memory://", "Memory://", "memory://?x=1", "async+memory://", "redis://localhost:6379", "rediss://localhost:6380",
    "redis+unix:///tmp/redis.sock", "valkey://localhost:6379", "Valkey://localhost:6379", "valkeys://h:1",
    "valkey+unix:///tmp/v.sock", "redis+cluster://a:7000,b:7001", "redis+cluster://a", "valkey+cluster://a:7000",
    "redis+sentinel://s1:26379,s2:26379/mymaster", "redis+sentinel://s1:26379", "redis+sentinel://s1:26379/",
    "valkey+sentinel://s1:26379/primary", "memcached://localhost:11211", "memcached://localhost",
    "memcached:///var/run/memcached.sock", "etcd://localhost:2379", "", "localhost:6379", "redis",
    "https://cache.example.com", "redis+cluster://[::1", "redis+sentinel://h:abc/x",
]
uri_ops += [{"op": "from_string", "text": u} for u in FROM]
job("storage URIs", uri_ops)

# ------------------------------------------------------------ programs

rng = random.Random(191)

ROUTES = """\
# the gateway's routes: method path strategy limits key [cost=n]
# the default limits apply to a route that names none ("-")
default 200/day;60/hour
exempt 10.0.0.1
route GET /api/v1/orders fixed-window 5/minute;20/hour ip
route POST /api/v1/orders moving-window 2/minute;10/hour user
route GET /api/v1/search sliding-window-counter 10/minute key
route GET /api/v1/export sliding-window-counter 1000/hour key cost=rows
route POST /api/v1/login moving-window 3/minute;10/hour ip
route GET /healthz fixed-window - ip
route GET /api/v1/reports fixed-window 2 per 30 seconds user
"""
with open(os.path.join(DATA, "routes.conf"), "w") as f:
    f.write(ROUTES)

clients = [("198.51.100.7", "ana", "k-ana"), ("198.51.100.8", "ben", "k-ben"), ("203.0.113.9", "chen", "k-chen"),
           ("203.0.113.9", "dee", "k-dee"), ("10.0.0.1", "ops", "k-ops"), ("192.0.2.44", "-", "-")]
paths = [("GET", "/api/v1/orders"), ("POST", "/api/v1/orders"), ("GET", "/api/v1/search"),
         ("GET", "/api/v1/export"), ("POST", "/api/v1/login"), ("GET", "/healthz"), ("GET", "/api/v1/reports"),
         ("DELETE", "/api/v1/orders"), ("GET", "/api/v1/unknown")]
weights = [6, 3, 6, 2, 2, 2, 2, 1, 1]
lines = ["# time ip user api-key method path rows"]
t = T0 + 3.0
for k in range(260):
    t += rng.choice([0.25, 0.5, 1.0, 1.5, 2.0, 3.75, 7.5, 0.125]) * (1 if k % 40 < 30 else 12)
    ip, user, key = rng.choice(clients)
    method, path = rng.choices(paths, weights)[0]
    rows = rng.choice([10, 50, 200, 400, 900, 1500]) if path == "/api/v1/export" else 0
    lines.append(f"{t!r} {ip} {user} {key} {method} {path} {rows}")
# a burst from one client at a fixed-window boundary
for k in range(8):
    lines.append(f"{t + 60 + k * 0.5!r} 198.51.100.66 eve k-eve GET /api/v1/orders 0")
with open(os.path.join(DATA, "access.log"), "w") as f:
    f.write("\n".join(lines) + "\n")
job("api gateway", [{"op": "gateway"}])

LOG = ["# time ip user outcome"]
t = T0 + 1000.0
attacker = "45.33.12.9"
for k in range(30):
    t += rng.choice([0.5, 1.0, 2.0, 4.0, 9.0])
    if k % 3 == 0:
        LOG.append(f"{t!r} 198.51.100.7 ana " + ("ok" if k % 9 == 0 else "fail"))
    else:
        LOG.append(f"{t!r} {attacker} " + rng.choice(["root", "admin", "ana", "ben"]) + " fail")
t += 70
for user, outcome in [("ana", "fail"), ("ana", "fail"), ("ana", "ok"), ("ana", "fail"), ("ben", "ok")]:
    t += 1.5
    LOG.append(f"{t!r} 198.51.100.7 {user} {outcome}")
t += 3700
LOG.append(f"{t!r} {attacker} root fail")
LOG.append(f"{t + 1!r} {attacker} admin fail")
with open(os.path.join(DATA, "logins.log"), "w") as f:
    f.write("\n".join(LOG) + "\n")
job("login guard", [{"op": "logins"}])

EXP = ["# time tenant rows"]
t = T0 + 5000.0
for k in range(40):
    t += rng.choice([30.0, 60.0, 90.0, 240.0, 600.0])
    EXP.append(f"{t!r} " + rng.choice(["acme", "globex", "initech"]) + f" {rng.choice([50, 120, 300, 450, 700])}")
with open(os.path.join(DATA, "exports.log"), "w") as f:
    f.write("\n".join(EXP) + "\n")
job("export quotas", [{"op": "exports"}])

burst = [55.0, 56.0, 57.0, 58.0, 59.0, 59.5, 60.0, 60.5, 61.0, 62.0, 90.0, 110.0, 115.5, 119.0, 121.0, 150.0, 175.0]
job("window boundary", [{"op": "boundary", "limit": "5/minute", "times": [T0 + 1200 + x for x in burst]}])

with open(os.path.join(DATA, "jobs.jsonl"), "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(jobs), "jobs,", sum(len(j["ops"]) for j in jobs), "operations")
