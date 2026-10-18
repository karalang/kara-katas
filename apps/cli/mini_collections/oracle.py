#!/usr/bin/env python3
"""Runs data/jobs.tsv with Python's collections and functools.lru_cache
and prints expected.out."""
import functools
from collections import ChainMap, Counter, OrderedDict, defaultdict, deque


def words(args):
    if len(args) == 1 and args[0].startswith("@"):
        with open("data/" + args[0][1:]) as f:
            return f.read().split()
    return args


def show(op, fn, state):
    try:
        r = fn()
    except (IndexError, ValueError, KeyError) as e:
        print(f"  {op}: {type(e).__name__}: {e}")
        return
    if r is None:
        print(f"  {op} -> {state()!r}")
    else:
        print(f"  {op} = {r!r} -> {state()!r}")


def counter_job(ops):
    c = Counter()
    for op in ops.split("|"):
        p = op.split(" ")
        cmd, args = p[0], [a for a in p[1:] if a]
        if cmd == "new":
            c = Counter(words(args))
            print(f"  {op} -> {c!r}")
        elif cmd == "repr":
            print(f"  {c!r}")
        elif cmd == "most":
            print(f"  {op} = {c.most_common(int(args[0])) if args else c.most_common()!r}")
        elif cmd == "total":
            print(f"  total = {c.total()}")
        elif cmd == "get":
            print(f"  {op} = {c[args[0]]}")
        elif cmd == "elements":
            print(f"  elements = {list(c.elements())!r}")
        elif cmd == "update":
            c.update(args)
            print(f"  {op} -> {c!r}")
        elif cmd == "subtract":
            c.subtract(args)
            print(f"  {op} -> {c!r}")
        elif cmd == "del":
            del c[args[0]]
            print(f"  {op} -> {c!r}")
        elif cmd == "pos":
            print(f"  +c = {+c!r}")
        elif cmd == "neg":
            print(f"  -c = {-c!r}")
        else:
            other = Counter(args)
            r = {"add": lambda: c + other, "sub": lambda: c - other, "and": lambda: c & other,
                 "or": lambda: c | other, "le": lambda: c <= other, "ge": lambda: c >= other,
                 "eq": lambda: c == other, "ne": lambda: c != other}[cmd]()
            print(f"  {op} = {r!r}")


def deque_job(maxlen, ops):
    d = deque(maxlen=None if maxlen == "-" else int(maxlen))
    for op in ops.split("|"):
        p = op.split(" ")
        cmd, a = p[0], [int(x) for x in p[1:]]
        fns = {
            "append": lambda: d.append(a[0]),
            "appendleft": lambda: d.appendleft(a[0]),
            "extend": lambda: d.extend(a),
            "extendleft": lambda: d.extendleft(a),
            "pop": lambda: d.pop(),
            "popleft": lambda: d.popleft(),
            "len": lambda: len(d),
            "get": lambda: d[a[0]],
            "set": lambda: d.__setitem__(a[0], a[1]),
            "rotate": lambda: d.rotate(a[0]),
            "count": lambda: d.count(a[0]),
            "index": lambda: d.index(a[0]),
            "remove": lambda: d.remove(a[0]),
            "reverse": lambda: d.reverse(),
            "insert": lambda: d.insert(a[0], a[1]),
            "clear": lambda: d.clear(),
            "maxlen": lambda: d.maxlen if d.maxlen is not None else "None",
        }
        show(op, fns[cmd], lambda: d)


def odict_job(ops):
    d = OrderedDict()
    for op in ops.split("|"):
        p = op.split(" ")
        cmd, a = p[0], p[1:]
        fns = {
            "set": lambda: d.__setitem__(a[0], int(a[1])),
            "repr": lambda: None,
            "get": lambda: d[a[0]],
            "del": lambda: d.__delitem__(a[0]),
            "move": lambda: d.move_to_end(a[0], last=a[1] == "last"),
            "popitem": lambda: d.popitem(last=a[0] == "last"),
            "keys": lambda: list(d),
        }
        show(op, fns[cmd], lambda: d)


def lru_job(maxsize, path):
    with open("data/" + path[1:]) as f:
        keys = f.read().split()

    @functools.lru_cache(maxsize=maxsize)
    def fetch(k):
        return k.upper()

    marks = []
    for k in keys:
        before = fetch.cache_info().hits
        fetch(k)
        marks.append(k + ("+" if fetch.cache_info().hits > before else "-"))
    print("  " + " ".join(marks))
    print(f"  {fetch.cache_info()}")
    # The same policy over an OrderedDict, for the evictions and the order.
    cache = OrderedDict()
    evicted = []
    for k in keys:
        if maxsize == 0:
            continue
        if k in cache:
            cache.move_to_end(k)
            continue
        if len(cache) >= maxsize:
            old, _ = cache.popitem(last=False)
            evicted.append(old)
        cache[k] = k.upper()
    print(f"  evicted: {' '.join(evicted) if evicted else '-'}")
    print(f"  cached, oldest first: {' '.join(cache) if cache else '-'}")


def num_or_str(v):
    try:
        return int(v)
    except ValueError:
        return v


def parse_map(spec):
    if spec == "-":
        return {}
    out = {}
    for part in spec.split(","):
        k, v = part.split("=")
        out[k] = num_or_str(v)
    return out


def chain_job(specs, ops):
    cm = ChainMap(*[parse_map(s) for s in specs])
    for op in ops.split("|"):
        p = op.split(" ")
        cmd, a = p[0], p[1:]

        def child():
            nonlocal cm
            cm = cm.new_child()

        def parents():
            nonlocal cm
            cm = cm.parents

        fns = {
            "get": lambda: cm[a[0]],
            "in": lambda: a[0] in cm,
            "len": lambda: len(cm),
            "keys": lambda: list(cm),
            "repr": lambda: None,
            "set": lambda: cm.__setitem__(a[0], num_or_str(a[1])),
            "del": lambda: cm.__delitem__(a[0]),
            "pop": lambda: cm.pop(a[0]),
            "child": child,
            "parents": parents,
        }
        show(op, fns[cmd], lambda: cm)


def read_log(path):
    with open("data/" + path[1:]) as f:
        return [line.rstrip("\n") for line in f]


def run(f):
    kind = f[0]
    if kind == "counter":
        counter_job(f[1])
    elif kind == "deque":
        deque_job(f[1], f[2])
    elif kind == "odict":
        odict_job(f[1])
    elif kind == "lru":
        lru_job(int(f[1]), f[2])
    elif kind == "chain":
        chain_job(f[1:-1], f[-1])
    elif kind == "group":
        by_status = defaultdict(list)
        by_ip = Counter()
        for line in read_log(f[1]):
            ip, method, path, status = line.split(" ")
            by_status[status].append(path)
            by_ip[ip] += 1
        for status, paths in by_status.items():
            print(f"  {status}: {paths!r}")
        print(f"  {by_ip.most_common(3)!r}")
    elif kind == "tail":
        lines = deque(read_log(f[2]), maxlen=int(f[1]))
        for line in lines:
            print(f"  {line}")
        print(f"({len(lines)} lines)")


with open("data/jobs.tsv") as fh:
    for raw in fh:
        fields = raw.rstrip("\n").split("\t")
        print("== " + " | ".join(fields))
        run(fields)
