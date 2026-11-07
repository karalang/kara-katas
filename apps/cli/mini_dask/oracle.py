"""Reference for mini_dask: plays data/script.txt on one thread, running
every run in order, and prints what the program must print.

Run from this directory: python3 -I -B oracle.py"""
import re

WORKERS = 4
LO, HI = -(1 << 63), (1 << 63) - 1
RANGE_MAX = 100000
PRIMES_MAX = 2000000

NAME = re.compile(r"[a-z][a-z0-9_]{0,31}\Z")
NUMBER = re.compile(r"-?[0-9]{1,9}\Z")

USAGE = {
    "inc": "inc <x>", "neg": "neg <x>", "add": "add <x> <y>...", "mul": "mul <x> <y>",
    "div": "div <x> <y>", "range": "range <n>", "sum": "sum <list>", "len": "len <list>",
    "concat": "concat <list>...", "primes": "primes <n>", "boom": "boom",
}
ARITY = {
    "inc": (1, 1), "neg": (1, 1), "add": (2, None), "mul": (2, 2), "div": (2, 2),
    "range": (1, 1), "sum": (1, 1), "len": (1, 1), "concat": (1, None), "primes": (1, 1),
    "boom": (0, 0),
}


class Fail(Exception):
    pass


def show(v):
    if isinstance(v, int):
        return str(v)
    if len(v) <= 8:
        return "[" + ", ".join(map(str, v)) + "]"
    return "[" + ", ".join(map(str, v[:3])) + ", ..., " + ", ".join(map(str, v[-2:])) + f"] ({len(v)} items)"


def fits(f, n):
    if n < LO or n > HI:
        raise Fail(f"OverflowError: {f} result does not fit in 64 bits")
    return n


def want_int(f, v):
    if not isinstance(v, int):
        raise Fail(f"TypeError: {f} expects an int, got a list")
    return v


def want_list(f, v):
    if isinstance(v, int):
        raise Fail(f"TypeError: {f} expects a list, got an int")
    return v


def primes_below(n):
    if n < 3:
        return 0
    sieve = [True] * n
    found = 0
    for i in range(2, n):
        if sieve[i]:
            found += 1
            for k in range(i * i, n, i):
                sieve[k] = False
    return found


def apply(f, args):
    if f in ("inc", "neg", "mul", "div", "add", "range", "primes"):
        xs = [want_int(f, a) for a in args]
    else:
        xs = [want_list(f, a) for a in args]
    if f == "inc":
        return fits(f, xs[0] + 1)
    if f == "neg":
        return fits(f, -xs[0])
    if f == "add":
        t = xs[0]
        for x in xs[1:]:
            t = fits(f, t + x)
        return t
    if f == "mul":
        return fits(f, xs[0] * xs[1])
    if f == "div":
        if xs[1] == 0:
            raise Fail("ZeroDivisionError: integer division or modulo by zero")
        return fits(f, xs[0] // xs[1])
    if f == "range":
        if xs[0] > RANGE_MAX:
            raise Fail(f"ValueError: range({xs[0]}) is too long")
        return list(range(xs[0]))
    if f == "primes":
        if xs[0] > PRIMES_MAX:
            raise Fail(f"ValueError: primes below {xs[0]} is too many")
        return primes_below(xs[0])
    if f == "sum":
        t = 0
        for x in xs[0]:
            t = fits(f, t + x)
        return t
    if f == "len":
        return len(xs[0])
    if f == "concat":
        out = []
        for x in xs:
            out += x
        return out
    if f == "boom":
        raise Fail("ZeroDivisionError: division by zero")
    raise AssertionError(f)


class Err(Exception):
    pass


class Dask:
    def __init__(self):
        self.keys = {}          # key -> ("value", v) | ("call", f, args); args are ("num", n) | ("key", k)
        self.stats = {"runs": 0, "tasks": 0, "failed": 0, "by": {}}

    def key_deps(self, k):
        t = self.keys[k]
        if t[0] == "value":
            return []
        out = []
        for a in t[2]:
            if a[0] == "key" and a[1] not in out:
                out.append(a[1])
        return out

    def value(self, w):
        if len(w) != 3:
            raise Err("usage: value <key> <number>")
        k, n = w[1], w[2]
        if not NAME.match(k):
            raise Err(f"bad key '{k}'")
        if k in self.keys:
            raise Err(f"key {k} already exists")
        if not NUMBER.match(n):
            raise Err(f"bad number '{n}'")
        self.keys[k] = ("value", int(n))

    def task(self, w):
        if len(w) < 3:
            raise Err("usage: task <key> <func> [args]")
        k, f = w[1], w[2]
        if not NAME.match(k):
            raise Err(f"bad key '{k}'")
        if k in self.keys:
            raise Err(f"key {k} already exists")
        if f not in USAGE:
            raise Err(f"unknown function '{f}'")
        args = []
        for a in w[3:]:
            if NUMBER.match(a):
                args.append(("num", int(a)))
            elif NAME.match(a):
                args.append(("key", a))
            else:
                raise Err(f"bad argument '{a}'")
        lo, hi = ARITY[f]
        if len(args) < lo or (hi is not None and len(args) > hi):
            raise Err(f"bad arguments for {f}: {USAGE[f]}")
        self.keys[k] = ("call", f, args)

    def drop(self, w):
        if len(w) != 2:
            raise Err("usage: drop <key>")
        if w[1] not in self.keys:
            raise Err(f"no key '{w[1]}'")
        del self.keys[w[1]]
        print(f"  dropped {w[1]}")

    def compute(self, w, persist):
        cmd = "persist" if persist else "compute"
        fuse = True
        want = []
        for x in w[1:]:
            if x == "--nofuse":
                fuse = False
            elif x.startswith("--"):
                raise Err(f"unknown option '{x}'")
            else:
                want.append(x)
        if not want:
            raise Err(f"usage: {cmd} [--nofuse] <key>...")
        for i, k in enumerate(want):
            if k not in self.keys:
                raise Err(f"no key '{k}'")
            if k in want[:i]:
                raise Err(f"duplicate key {k}")
        # 1. cull and order
        order = []
        state = {}
        stack = []

        def walk(k):
            state[k] = 1
            stack.append(k)
            for d in self.key_deps(k):
                if d not in self.keys:
                    raise Err(f"missing dependency {d} of {k}")
                if state.get(d) == 1:
                    path = stack[stack.index(d):] + [d]
                    raise Err("cycle " + " -> ".join(path))
                if d not in state:
                    walk(d)
            stack.pop()
            state[k] = 2
            order.append(k)

        for k in want:
            if k not in state:
                walk(k)
        kept = set(order)
        print(f"  cull: {len(order)} of {len(self.keys)} keys")
        pos = {k: i for i, k in enumerate(order)}
        users = {k: [] for k in order}
        for k in order:
            for d in self.key_deps(k):
                users[d].append(k)
        # 2. fuse
        into = {}
        if fuse:
            for k in order:
                if self.keys[k][0] != "call" or k in want or len(users[k]) != 1:
                    continue
                p = users[k][0]
                if self.keys[p][0] == "call" and self.key_deps(p) == [k]:
                    into[k] = p
        heads = {}
        tail_of = {}
        for k in order:
            if self.keys[k][0] != "call" or k in into:
                continue
            chain = [k]
            while True:
                prev = [d for d in self.key_deps(chain[0]) if into.get(d) == chain[0]]
                if not prev:
                    break
                chain.insert(0, prev[0])
            heads[k] = chain
            for m in chain:
                tail_of[m] = k
            if len(chain) > 1:
                print("  fuse: " + " + ".join(chain))
        runs = [k for k in order if k in heads]
        print("  order: " + (", ".join(runs) if runs else "none"))
        # 4. run, one at a time in order: a run's inputs come first in the order
        result = {}
        for k in order:
            if self.keys[k][0] == "value":
                result[k] = ("ok", self.keys[k][1])
        nfail = nskip = 0
        for k in runs:
            chain = heads[k]
            inputs = self.key_deps(chain[0])
            bad = [d for d in inputs if result[d][0] != "ok"]
            if bad:
                r = result[bad[0]]
                origin = bad[0] if r[0] == "failed" else r[2]
                result[k] = ("skipped", r[1], origin)
                nskip += 1
                continue
            self.stats["runs"] += 1
            prev = None
            out = None
            try:
                for i, m in enumerate(chain):
                    f, args = self.keys[m][1], self.keys[m][2]
                    vals = []
                    for a in args:
                        if a[0] == "num":
                            vals.append(a[1])
                        elif i > 0 and a[1] == chain[i - 1]:
                            vals.append(prev)
                        else:
                            vals.append(result[a[1]][1])
                    self.stats["tasks"] += 1
                    self.stats["by"][f] = self.stats["by"].get(f, 0) + 1
                    prev = apply(f, vals)
                out = ("ok", prev)
            except Fail as e:
                out = ("failed", str(e))
                self.stats["failed"] += 1
                nfail += 1
            result[k] = out
        for k in want:
            r = result[k]
            if r[0] == "ok":
                print(f"  {k} = {show(r[1])}")
            elif r[0] == "failed":
                print(f"  {k} ! {r[1]}")
            else:
                print(f"  {k} ! {r[1]} (from {r[2]})")
        print(f"  runs {len(runs) - nskip}, failed {nfail}, skipped {nskip}")
        if persist:
            n = 0
            for k in want:
                if self.keys[k][0] == "call" and result[k][0] == "ok":
                    self.keys[k] = ("value", result[k][1])
                    n += 1
            print(f"  persisted {n}")

    def deps_of(self, k):
        seen = set()
        missing = set()

        def go(k):
            for d in self.key_deps(k):
                if d not in self.keys:
                    missing.add(d)
                elif d not in seen:
                    seen.add(d)
                    go(d)

        go(k)
        return sorted([(d, d) for d in seen] + [(d, f"{d} (missing)") for d in missing])

    def inspect(self, w):
        if len(w) == 1:
            raise Err("missing command")
        c = w[1]
        if c == "graph":
            if len(w) != 2:
                raise Err("usage: @ graph")
            if not self.keys:
                print("  empty")
            for k, t in self.keys.items():
                if t[0] == "value":
                    print(f"  {k}: {show(t[1])}")
                else:
                    args = ", ".join(str(a[1]) for a in t[2])
                    print(f"  {k}: {t[1]}({args})")
        elif c in ("deps", "dependents"):
            if len(w) != 3:
                raise Err(f"usage: @ {c} <key>")
            k = w[2]
            if k not in self.keys:
                raise Err(f"no key '{k}'")
            if c == "deps":
                ds = [s for _, s in self.deps_of(k)]
                print(f"  {k} needs " + (", ".join(ds) if ds else "nothing"))
            else:
                us = [u for u in self.keys if k in self.key_deps(u)]
                print(f"  {k} is used by " + (", ".join(us) if us else "nothing"))
        else:
            raise Err(f"unknown command '@ {c}'")

    def command(self, w):
        c = w[0]
        if c == "@":
            self.inspect(w)
        elif c == "value":
            self.value(w)
        elif c == "task":
            self.task(w)
        elif c == "drop":
            self.drop(w)
        elif c == "compute":
            self.compute(w, False)
        elif c == "persist":
            self.compute(w, True)
        else:
            raise Err(f"unknown command '{c}'")


def main():
    with open("data/script.txt", encoding="utf-8", newline="") as fh:
        text = fh.read()
    d = Dask()
    print(f"== script ({WORKERS} workers)")
    for i, line in enumerate(text.split("\n")):
        w = line.split("#", 1)[0].split()
        if not w:
            continue
        print("> " + " ".join(w))
        try:
            d.command(w)
        except Err as e:
            print(f"  error: script.txt:{i + 1}: {e}")
    print("== end")
    print(f"  {len(d.keys)} keys")
    s = d.stats
    print(f"  {WORKERS} workers: {s['runs']} runs, {s['tasks']} tasks, {s['failed']} failed")
    by = ", ".join(f"{f} {n}" for f, n in sorted(s["by"].items()))
    print(f"  by function: {by if by else 'none'}")


main()
