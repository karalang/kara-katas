# Writes data/jobs.jsonl: scripts of cache operations, written out and
# drawn at random from a fixed seed, memoized function runs, and cache
# keys.
import json
import os
import random

os.makedirs("data", exist_ok=True)
jobs = []


def script(cache, ops, start=0, step=0):
    j = {"kind": "script", "cache": cache, "ops": ops}
    if start:
        j["start"] = start
    if step:
        j["step"] = step
    jobs.append(j)


# ------------------------------------------------------------ by hand

basic = [
    ["set", "a", 1], ["set", "b", 2], ["set", "c", 3], ["repr"], ["getitem", "a"],
    ["set", "d", 4], ["repr"], ["get", "b"], ["get", "zz"], ["get", "zz", "none"],
    ["in", "a"], ["in", "b"], ["len"], ["currsize"], ["maxsize"], ["set", "a", 10],
    ["repr"], ["pop", "c"], ["pop", "c"], ["pop", "c", 0], ["setdefault", "e", 5],
    ["setdefault", "e", 6], ["setdefault", "f"], ["repr"], ["del", "nope"], ["popitem"],
    ["repr"], ["list"], ["items"], ["values"], ["repr"], ["update", [["x", 7], ["y", 8]]],
    ["repr"], ["clear"], ["repr"], ["popitem"], ["len"],
]
for t in ["Cache", "FIFOCache", "LRUCache", "LFUCache"]:
    script({"type": t, "maxsize": 3}, basic)
script({"type": "RRCache", "maxsize": 3, "picks": [0, 2, 1, 5]}, basic)
script({"type": "TTLCache", "maxsize": 3, "ttl": 10}, basic)
script({"type": "TLRUCache", "maxsize": 3, "ttu": {"kind": "fixed", "n": 10}}, basic)

script({"type": "LRUCache", "maxsize": -1}, [["repr"]])
script({"type": "LRUCache", "maxsize": 0}, [["set", "a", 1], ["repr"], ["popitem"]])
script({"type": "Cache", "maxsize": 2}, [
    ["set", ["user", 1], "ada"], ["set", ["user", 2], "grace"], ["set", ["user", 3], "linus"],
    ["repr"], ["popitem"], ["popitem"], ["popitem"], ["set", None, None], ["repr"],
    ["getitem", None], ["set", 7, [1, [2, 3]]], ["repr"], ["set", -3, []], ["repr"],
])

# Sizes: a byte budget for rendered pages.
sized = [
    ["set", "home", "<html>home</html>"], ["set", "about", "about us"], ["repr"],
    ["set", "docs", "documentation index page"], ["repr"], ["currsize"],
    ["set", "about", "about us, longer now"], ["repr"],
    ["set", "huge", "x" * 41], ["repr"], ["set", "empty", ""], ["repr"],
    ["set", "home", "h"], ["set", "blog", "a blog post body"], ["repr"],
    ["set", "bad", "!bad"], ["repr"], ["set", "edge", "y" * 40], ["repr"],
    ["pop", "edge"], ["currsize"], ["update", [["a", "aa"], ["b", "bbb"], ["c", "c"]]],
    ["repr"], ["del", "a"], ["del", "a"], ["repr"],
]
for t in ["Cache", "FIFOCache", "LRUCache", "LFUCache"]:
    script({"type": t, "maxsize": 40, "getsizeof": "checked"}, sized)
script({"type": "RRCache", "maxsize": 40, "getsizeof": "checked", "picks": [1, 0, 3]}, sized)
script({"type": "TTLCache", "maxsize": 40, "ttl": 100, "getsizeof": "checked"}, sized)
script({"type": "TLRUCache", "maxsize": 40, "getsizeof": "checked", "ttu": {"kind": "len"}}, sized)

# LRU order: reads move keys to the end, and so do values() and items().
script({"type": "LRUCache", "maxsize": 4}, [
    ["set", "a", 1], ["set", "b", 2], ["set", "c", 3], ["set", "d", 4], ["getitem", "a"],
    ["set", "e", 5], ["repr"], ["get", "c"], ["set", "f", 6], ["repr"], ["in", "d"],
    ["set", "g", 7], ["repr"], ["values"], ["set", "h", 8], ["repr"], ["items"],
    ["setdefault", "c", 0], ["set", "i", 9], ["repr"], ["pop", "nope", "x"], ["popitem"],
    ["popitem"], ["repr"],
])

# LFU counts, with ties broken by the order of the key set.
lfu = [["set", k, n] for n, k in enumerate(["alpha", "beta", "gamma", "delta", "eps"])]
lfu += [["getitem", "alpha"], ["getitem", "alpha"], ["getitem", "beta"], ["get", "gamma"],
        ["set", "zeta", 6], ["repr"], ["set", "eta", 7], ["repr"], ["set", "theta", 8],
        ["repr"], ["getitem", "zeta"], ["set", "beta", 22], ["getitem", "beta"],
        ["set", "iota", 9], ["repr"], ["popitem"], ["popitem"], ["popitem"], ["repr"],
        ["values"], ["values"], ["set", "kappa", 10], ["set", "lambda", 11], ["repr"]]
script({"type": "LFUCache", "maxsize": 5}, lfu)
script({"type": "LFUCache", "maxsize": 3}, [
    ["set", 1, "one"], ["set", 2, "two"], ["set", 3, "three"], ["set", 4, "four"],
    ["repr"], ["set", 9, "nine"], ["set", 17, "seventeen"], ["repr"], ["getitem", 9],
    ["set", -1, "minus"], ["set", -2, "minus two"], ["repr"],
    ["set", ["k", 1], "t1"], ["set", ["k", 2], "t2"], ["repr"], ["set", "", "empty"],
    ["set", ["k", 3], "t3"], ["repr"],
])

# TTL: items die at insert time + ttl, reads do not renew them.
ttl = [
    ["set", "s1", "alice"], ["tick", 3], ["set", "s2", "bob"], ["tick", 3],
    ["set", "s3", "carol"], ["repr"], ["tick", 4], ["in", "s1"], ["repr"], ["len"],
    ["getitem", "s1"], ["get", "s2"], ["tick", 3], ["getitem", "s2"], ["del", "s2"],
    ["set", "s4", "dave"], ["set", "s5", "erin"], ["set", "s6", "frank"], ["repr"],
    ["getitem", "s4"], ["set", "s7", "grace"], ["repr"], ["tick", 5], ["list"],
    ["items"], ["expire"], ["repr"], ["tick", 20], ["currsize"], ["repr"],
    ["set", "s8", "heidi"], ["tick", 2], ["set", "s8", "heidi2"], ["tick", 9], ["get", "s8"],
    ["expire", 100], ["popitem"],
]
script({"type": "TTLCache", "maxsize": 3, "ttl": 10}, ttl)
script({"type": "TTLCache", "maxsize": 3, "ttl": 10}, ttl, start=1000, step=1)
script({"type": "TTLCache", "maxsize": 2, "ttl": 0}, [["set", "a", 1], ["repr"], ["getitem", "a"],
                                                     ["del", "a"], ["len"]])

tlru_table = {"kind": "table", "table": {"short": 2, "long": 50, "never": -1, "now": 0}, "default": 10}
tlru = [
    ["set", "short", 1], ["set", "long", 2], ["set", "mid", 3], ["repr"], ["list"],
    ["tick", 2], ["repr"], ["set", "never", 4], ["repr"], ["set", "now", 5], ["repr"],
    ["set", "long", 6], ["set", "long", 7], ["set", "long", 8], ["list"], ["repr"],
    ["set", "a", 9], ["set", "b", 10], ["repr"], ["list"], ["getitem", "long"],
    ["tick", 9], ["list"], ["items"], ["set", "long", "x"], ["set", "never", 1],
    ["repr"], ["del", "long"], ["popitem"], ["tick", 60], ["expire"], ["repr"],
]
script({"type": "TLRUCache", "maxsize": 4, "ttu": tlru_table}, tlru)
script({"type": "TLRUCache", "maxsize": 4, "ttu": tlru_table}, tlru, start=5, step=1)

# ------------------------------------------------------------ at random

rng = random.Random(20261019)
KEYS = ["k%d" % i for i in range(7)] + [3, 4, ["t", 1]]


def random_value(sized):
    r = rng.random()
    if r < (0.04 if sized else 0.5):
        return rng.randrange(100)
    if r < 0.9:
        return "v" * rng.randrange(1, 9)
    return [rng.randrange(5), "x"]


def random_ops(n, timed, sized=False):
    ops = []
    for _ in range(n):
        r = rng.random()
        k = rng.choice(KEYS)
        if r < 0.35:
            ops.append(["set", k, random_value(sized)])
        elif r < 0.5:
            ops.append(["getitem", k])
        elif r < 0.58:
            ops.append(["get", k])
        elif r < 0.63:
            ops.append(["del", k])
        elif r < 0.68:
            ops.append(["pop", k, None])
        elif r < 0.72:
            ops.append(["popitem"])
        elif r < 0.76:
            ops.append(["setdefault", k, random_value(sized)])
        elif r < 0.8:
            ops.append(["in", k])
        elif r < 0.84 and timed:
            ops.append(["tick", rng.randrange(1, 6)])
        elif r < 0.86:
            ops.append(["values"])
        elif r < 0.87:
            ops.append(["clear"])
        else:
            ops.append(["repr"])
    ops.append(["repr"])
    return ops


for t in ["Cache", "FIFOCache", "LRUCache", "LFUCache"]:
    script({"type": t, "maxsize": 4}, random_ops(150, False))
    script({"type": t, "maxsize": 12, "getsizeof": "len"}, random_ops(150, False, True))
script({"type": "RRCache", "maxsize": 4, "picks": [rng.randrange(10) for _ in range(30)]},
       random_ops(150, False))
script({"type": "TTLCache", "maxsize": 4, "ttl": 7}, random_ops(150, True))
script({"type": "TTLCache", "maxsize": 12, "ttl": 9, "getsizeof": "len"}, random_ops(150, True, True), step=1)
script({"type": "TLRUCache", "maxsize": 4, "ttu": {"kind": "table", "table": {"k1": 3, "k2": 1, "k3": 30}, "default": 8}},
       random_ops(150, True))
script({"type": "TLRUCache", "maxsize": 12, "getsizeof": "len", "ttu": {"kind": "len"}},
       random_ops(150, True, True), start=50, step=1)

# ------------------------------------------------------------ memoizing


def memo(func, decorator, calls, **kw):
    j = {"kind": "memo", "func": func, "decorator": decorator}
    j.update(kw)
    j["calls"] = calls
    jobs.append(j)


memo("fib", "lru_cache", [["call", [10]], ["info"], ["call", [12]], ["info"], ["cache"], ["params"]],
     maxsize=4)
memo("fib", "lru_cache", [["call", [15]], ["info"], ["params"]], maxsize=None)
memo("fib", "lfu_cache", [["call", [9]], ["info"], ["cache"], ["call", [3]], ["cache"]], maxsize=3)
memo("fib", "fifo_cache", [["call", [8]], ["info"], ["cache"]], maxsize=3)
memo("fib", "rr_cache", [["call", [8]], ["info"], ["cache"]], maxsize=3, picks=[1, 0, 2, 2, 1])
memo("fib", "cached", [["call", [11]], ["cache"]], cache={"type": "LRUCache", "maxsize": 20})
memo("user", "ttl_cache", [
    ["call", [1]], ["call", [2]], ["call", [1]], ["tick", 30], ["call", [1]], ["call", [9]],
    ["call", [9]], ["info"], ["tick", 31], ["call", [2]], ["call", [1]], ["info"], ["cache"],
    ["clear"], ["info"], ["call", [3]], ["call", [3.0]], ["info"], ["params"],
], maxsize=2, ttl=60)
memo("user", "ttl_cache", [["call", [1]], ["call", [1]], ["tick", 600], ["call", [1]], ["info"],
                           ["cache"], ["params"]], maxsize=None, ttl=600)
memo("user", "lru_cache", [["call", [1]], ["call", [1.0]], ["call", [True]], ["info"], ["cache"]],
     typed=True)
memo("user", "lru_cache", [["call", [1]], ["call", [1.0]], ["call", [True]], ["info"]], typed=False)
memo("price", "cached", [
    ["call", ["apple"]], ["call", ["apple"], {"qty": 1}], ["call", ["apple", 1]],
    ["call", ["pear"], {"qty": 3, "currency": "USD"}], ["call", ["pear"], {"currency": "USD", "qty": 3}],
    ["call", ["fig", 2, "GBP"]], ["call", ["apple"]], ["info"], ["cache"],
], cache={"type": "LRUCache", "maxsize": 8}, info=True)
memo("price", "cached", [["call", ["kiwi"]], ["call", ["kiwi"]], ["cache"]],
     cache={"type": "Cache", "maxsize": 8}, typed=True)
memo("render", "cached", [
    ["call", ["home"]], ["call", ["about"]], ["call", ["docs"]], ["call", ["home"]],
    ["call", ["blog"], {"lang": "fr"}], ["call", ["home"]], ["call", ["huge"]],
    ["call", ["missing"]], ["info"], ["cache"], ["clear"], ["info"], ["cache"],
], cache={"type": "LRUCache", "maxsize": 100, "getsizeof": "len"}, info=True, lock=True)
memo("render", "cached", [["call", ["home"]], ["call", ["home"]], ["info"], ["cache"]],
     cache="dict", info=True)
memo("render", "cached", [["call", ["home"]], ["call", ["home"]], ["info"], ["clear"], ["info"]],
     cache=None, info=True)
memo("user", "cached", [["call", [5]], ["call", [5]], ["cache"]], cache=None)
memo("user", "cached", [
    ["call", [1]], ["call", [2]], ["call", [3]], ["call", [1]], ["call", [4]], ["call", [5]],
    ["call", [1]], ["call", [6]], ["call", [7]], ["info"], ["cache"],
], cache={"type": "TLRUCache", "maxsize": 3, "ttu": {"kind": "fixed", "n": 5}}, info=True, step=1)

# ------------------------------------------------------------ keys
jobs.append({"kind": "key", "typed": False, "calls": [
    [[]], [[1, 2]], [["a"], {"b": 2}], [[], {"z": 1, "a": 2}], [[[1, 2]]], [[None]],
]})
jobs.append({"kind": "key", "typed": True, "calls": [
    [[]], [[1, 2]], [["a"], {"b": 2}], [[], {"z": 1, "a": "x"}], [[[1, 2]]], [[None, 1.5]],
    [[True]],
]})

with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j) + "\n")
print(len(jobs), "jobs")
