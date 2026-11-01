"""Writes data/ for mini_symtable: the Python modules the jobs analyse, the
one-line programs, the builtin names the lint job knows, and the job list.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def write(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# A small web service: a route registry built from closures, class-based
# views that call super(), a request counter behind `global`, async
# handlers and a template filter table.
write("webapp.py", '''\
"""Order service: routes, views and filters."""
import json
import logging.handlers as handlers
from dataclasses import dataclass, field
from functools import wraps

log = logging.getLogger(__name__)
ROUTES = {}
request_count = 0


def route(path, *, methods=("GET",)):
    def register(fn):
        @wraps(fn)
        def wrapper(request, *args, **kwargs):
            global request_count
            request_count += 1
            if request.method not in methods:
                return {"status": 405, "allow": list(methods)}
            return fn(request, *args, **kwargs)
        ROUTES[path] = wrapper
        return wrapper
    return register


@dataclass
class Order:
    id: int
    lines: list = field(default_factory=list)
    status: str = "new"

    def total(self):
        return sum(line.price * line.qty for line in self.lines)


class View:
    template = "base.html"

    def __init__(self, request):
        self.request = request

    def render(self, **context):
        context.setdefault("template", self.template)
        return context


class OrderView(View):
    template = "order.html"

    def __init__(self, request, store):
        super().__init__(request)
        self.store = store

    def render(self, **context):
        order = self.store.get(self.request.args["id"])
        if (missing := order is None):
            log.warning("order %s not found", self.request.args["id"])
        return super().render(order=order, missing=missing, **context)


@route("/orders", methods=("GET", "POST"))
def orders(request, store):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
        except ValueError as exc:
            return {"status": 400, "error": str(exc)}
        order = Order(id=len(store) + 1, lines=payload.get("lines", []))
        store[order.id] = order
        return {"status": 201, "id": order.id}
    open_orders = [o for o in store.values() if o.status != "shipped"]
    by_status = {o.status: [p.id for p in store.values() if p.status == o.status]
                 for o in open_orders}
    return {"status": 200, "count": len(open_orders), "by_status": by_status}


async def fetch_rates(client, currencies):
    rates = {}
    async with client.session() as session:
        async for cur, rate in session.stream(currencies):
            rates[cur] = rate
    return {c: await client.adjust(r) for c, r in rates.items()}


FILTERS = {
    "money": lambda v, places=2: f"{v:.{places}f}",
    "upper": str.upper,
    "plural": lambda n, word: f"{n} {word}{'s' if n != 1 else ''}",
}


def make_app(store):
    handlers_by_path = {path: fn for path, fn in ROUTES.items()}

    def app(environ, start_response):
        handler = handlers_by_path.get(environ["PATH_INFO"])
        if handler is None:
            start_response("404 Not Found", [])
            return [b"not found"]
        result = handler(environ["request"], store)
        start_response(f"{result['status']} OK", [])
        return [json.dumps(result).encode()]
    return app
''')

# A command-line tool: nested functions with `nonlocal` counters, a
# generator pipeline, `match` with class, mapping and sequence patterns,
# star unpacking, `del`, and a lambda sort key over a closure.
write("cli.py", '''\
import sys
import os.path
from collections import Counter as Tally


def scan(paths, *, follow=False, ignore=()):
    seen = 0
    skipped = []

    def visit(path, depth=0):
        nonlocal seen
        if any(path.endswith(ext) for ext in ignore):
            skipped.append(path)
            return
        seen += 1
        if follow and os.path.isdir(path):
            for child in sorted(os.listdir(path)):
                visit(os.path.join(path, child), depth + 1)

    for p in paths:
        visit(p)
    return seen, skipped


def read_records(lines):
    for lineno, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        yield lineno, key.strip(), value.strip()


def describe(event):
    match event:
        case {"type": "click", "pos": (x, y)}:
            return f"click at {x},{y}"
        case {"type": "key", "key": str(k), **rest} if rest:
            return f"key {k} with {sorted(rest)}"
        case [first, *others]:
            return f"batch of {1 + len(others)} starting {first!r}"
        case Point(x=0, y=0) | Point(x=0, y=None):
            return "origin"
        case Point(x=px, y=py) as pt:
            return f"point {px},{py} ({pt})"
        case _:
            return "unknown"


def top_words(text, n=3, *, stop=frozenset({"a", "the"})):
    counts = Tally(w for w in text.lower().split() if w not in stop)
    order = lambda item: (-item[1], item[0])
    head, *tail = sorted(counts.items(), key=order)
    del tail[n - 1:]
    return [head, *tail]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    total, skipped = scan(argv, follow="-r" in argv, ignore=(".pyc", ".o"))
    for i, (lineno, key, value) in enumerate(read_records(sys.stdin)):
        print(i, lineno, key, value, sep="\\t")
    print(f"{total} files, {len(skipped)} skipped", file=sys.stderr)
    return 0 if total else 1


if __name__ == "__main__":
    raise SystemExit(main())
''')

# A data pipeline on 3.12+ syntax: generic classes and functions,
# `type` aliases, private names that get mangled, walrus inside a
# comprehension (it binds in the function), a class body comprehension
# that reads a class variable, and a nested class.
write("pipeline.py", '''\
from typing import Callable, Iterable

type Row = dict[str, object]
type Pair[K, V] = tuple[K, V]


class Stage[T, *Ts, **P]:
    __registry = []

    def __init__(self, fn: Callable[P, T], name: str = "") -> None:
        self.__fn = fn
        self.name = name or fn.__name__
        Stage.__registry.append(self)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.__fn(*args, **kwargs)

    @classmethod
    def registered(cls) -> list[str]:
        return [s.name for s in cls.__registry]

    class Error(Exception):
        def __init__(self, stage, cause):
            super().__init__(f"{stage.name}: {cause}")
            self.__cause = cause


def first[T: (int, str)](items: Iterable[T], default: T | None = None) -> T | None:
    for item in items:
        return item
    return default


def window[T](rows: list[T], size: int = 2) -> list[list[T]]:
    return [rows[i:i + size] for i in range(0, len(rows) - size + 1)]


def summarize(rows: list[Row]) -> dict[str, float]:
    totals = {}
    big = [r for r in rows if (amount := float(r["amount"])) > 100]
    totals["big"] = len(big)
    totals["last_amount"] = amount
    totals["by_region"] = {
        region: sum(float(r["amount"]) for r in rows if r["region"] == region)
        for region in {r["region"] for r in rows}
    }
    return totals


class Units:
    factors = {"k": 1e3, "M": 1e6, "G": 1e9}
    names = [name for name in factors]
    scaled = [f * 2 for f in factors.values()]

    def parse(self, text):
        unit = text[-1]
        return float(text[:-1]) * self.factors.get(unit, 1)


def compose[**P, R](*stages: Callable[..., R]) -> Callable[P, R]:
    def run(*args: P.args, **kwargs: P.kwargs) -> R:
        value = stages[0](*args, **kwargs)
        for stage in stages[1:]:
            value = stage(value)
        return value
    return run
''')

# Annotations postponed by the future import: the symbol table puts them
# in annotation blocks that never appear among the children.
write("models.py", '''\
from __future__ import annotations

import datetime as dt
from typing import Optional


class Customer:
    email: str
    since: dt.date
    referrer: Optional[Customer] = None

    def tenure(self, today: dt.date | None = None) -> dt.timedelta:
        today = today or dt.date.today()
        return today - self.since


def lookup(customers: dict[str, Customer], email: Unknown) -> Customer | None:
    return customers.get(email)
''')

# A file full of the mistakes a symbol-table checker is for.
write("smells.py", '''\
import os
import re as regex

DEBUG = False
cache = {}


def load(path, list=None):
    data = open(path).read()
    lines = data.splitlines()
    result = []
    for line in lines:
        result.append(line)
    return result


def configure(verbose):
    global DEBUG, LEVEL
    DEBUG = verbose
    print(LEVEL)


class Config:
    timeout = 30
    retries = 3

    def connect(self, host):
        for attempt in range(retries):
            if self.try_once(host, timeout):
                return True
        return False

    def try_once(self, host, wait):
        id = hash(host)
        return id % 2 == 0


def handlers():
    out = []
    for name in ("a", "b"):
        out.append(lambda: name)
    def flush():
        pending = len(out)
    return out


def report(rows):
    total = 0
    for r in rows:
        total += r.amount
    print(f"{len(rows)} rows, {totl:.2f}")
''')

BUILTINS = sorted(n for n in dir(__builtins__) if not n.startswith("_")) + [
    "__name__", "__file__", "__doc__", "__debug__"]
write("builtins.txt", "\n".join(BUILTINS) + "\n")

# One-line programs. `\\n` stands for a newline and `\\t` for a tab.
SNIPS = r"""
tables x = 1\ndef f(): return x
tables def f(x):\n    return lambda: x
tables def outer():\n    a = 1\n    def mid():\n        def inner():\n            return a\n        return inner\n    return mid
tables def counter():\n    n = 0\n    def inc():\n        nonlocal n\n        n += 1\n        return n\n    return inc
tables class A:\n    x = 1\n    def m(self):\n        return x
tables class A(B):\n    def m(self):\n        return super().m()
tables class C:\n    def f(self):\n        def g():\n            return __class__\n        return g
tables def f():\n    return [y for y in range(3)]
tables def f(xs):\n    return [(last := x) for x in xs], last
tables [(x := i) for i in range(3)]
tables def f(xs):\n    return (x for x in xs)
tables def f(xs):\n    return {k: v for k, v in xs}, {s for s in xs}
tables def f(rows):\n    return [[c for c in r] for r in rows]
tables def f(n):\n    return [lambda: i for i in range(n)]
tables class K:\n    items = [1, 2]\n    double = [i * 2 for i in items]
tables class K:\n    n = 3\n    sq = [n * i for i in range(n)]
tables import a.b.c as d, e.f\nfrom g import h as i, j
tables from g import *
tables try:\n    pass\nexcept E as err:\n    print(err)
tables with open(p) as (f, g), lock:\n    del f
tables for i, (a, *b) in pairs:\n    pass
tables def f(a, /, b, *c, d, e=1, **f):\n    pass
tables def f(a=x, *, b=y): return lambda c=z: c
tables @deco(arg)\ndef f(): pass
tables async def f(s):\n    async with s as t:\n        await t.go()\n    return [x async for x in s]
tables def g():\n    yield 1\n    yield from h()
tables def f(x: int, *a: str, **k: T) -> R:\n    v: list = []\n    w: int\n    return v
tables x: int\ny: str = "s"\nz.attr: int = 1
tables def f[T](x: T) -> T:\n    return x
tables def f[T](*, a=1): pass
tables class C[T](Base[T]):\n    def m(self) -> T: pass
tables class C[__T]:\n    def m(self, x: __T): return __T
tables type Alias[K, V] = dict[K, V]
tables class C:\n    type A = int\n    type B[T] = list[T]
tables def f[T: int, *Ts, **P](): pass
tables class C:\n    def f[T: C](self): pass
tables class C:\n    __x = 1\n    def __m(self):\n        return self.__x + __y
tables class _:\n    __x = 1
tables class C:\n    __dunder__ = 1\n    def m(self):\n        import __mod.sub\n        return __q
tables match p:\n    case {"k": v, **rest}:\n        pass\n    case [a, *b] | (a, b):\n        pass\n    case P(x=xx) as whole:\n        pass
tables f"{a!r:{width}.{prec}} {b}"
tables def f():\n    global g\n    g = 1\n    def h():\n        return g
tables def f():\n    x = 1\n    class C:\n        y = x\n        def m(self): return x
tables def f():\n    x = 1\n    class C:\n        x = 2\n        def m(self): return x
tables def f():\n    del x
tables def f():\n    x += 1
tables lambda: (yield)
tables def f():\n    return [(yield x) for x in y]
tables class A:\n    def m(self):\n        global super\n        return super
tables def f(): return super
tables x = super
tables def a():\n    def b():\n        def c():\n            nonlocal q\n        q = 1\n    q = 2
tables def f():\n    print(x)\n    [x := 1 for _ in ()]
tables def f[T](x=T): pass
dump def f(a):\n    return lambda: a
dump class C:\n    x: int = 1\n    def m(self): return super()
dump def f():\n    global g\n    g = 1
dump import os, sys as system\nfrom . import x
dump def f():\n    x = 1\n    return [x for _ in range(2)]
dump def f[T](a: T): return a
lint def f():\n    x = 1\n    y = 2\n    return y
lint def f(list, dict):\n    str = 1\n    return list
lint class C:\n    n = 1\n    def m(self):\n        return n
lint def f():\n    global G\n    return 1
lint print(undefined_name)\nimport os
error def f(a, a): pass
error def f(x):\n    global x
error def f(x):\n    nonlocal x
error def f():\n    x = 1\n    global x
error def f():\n    print(x)\n    global x
error def f():\n    global x\n    x: int = 1
error def g():\n    y = 1\n    def f():\n        nonlocal y\n        y: int
error def f():\n    x: int\n    global x
error def f():\n    y = 1\n    nonlocal y
error def f():\n    print(y)\n    nonlocal y
error nonlocal x
error def f():\n    nonlocal q
error def f():\n    x = 1\n    def g():\n        nonlocal x\n        global x
error class C:\n    nonlocal x
error def f():\n    from g import *
error class C:\n    from g import *
error class C:\n    [(x := i) for i in y]
error def f():\n    [x for x in y if (x := 1)]
error [i for i in (j := y)]
error [i for i in [k for k in (j := y)]]
error def f():\n    [[(j := 1) for j in range(2)] for i in range(3)]
error def f():\n    [i := 0 for i, j in y]
error def f():\n    yield\n    [(yield x) for x in y]
error def f():\n    {(yield k): v for k, v in y}
error def f():\n    {(yield from x) for x in y}
error def f():\n    list((yield x) for x in y)
error def f[T, T](): pass
error class C[T, *T]: pass
error def f[T](): nonlocal T
error def outer():\n    x = 1\n    def f[T]():\n        nonlocal T
error type A[T: (x := 1)] = T
error type A[T: (yield)] = T
error type A[T = (await x)] = T
error type A[*Ts = (x := 1)] = Ts
error type A[**P = (yield)] = P
error type A[T: (int, (x := 1))] = T
error type A = (x := 1)
error class C[T]((x := 1)): pass
error def f[T](x: (yield)): pass
error def f[__classdict__](): pass
error class C[T: (yield)]: pass
error def f():\n    def g(a, b, a): pass
error lambda a, a: 0
error def f(*, k, k): pass
error def f(a, **a): pass
"""

FILES = ["webapp.py", "cli.py", "pipeline.py", "models.py", "smells.py"]
jobs = []
for name in FILES:
    for mode in ("tables", "dump", "lint"):
        jobs.append(f"{mode} {name}")
for line in SNIPS.strip("\n").split("\n"):
    mode, src = line.split(" ", 1)
    jobs.append(f"snip {mode} {src}")
write("jobs.txt", "\n".join(jobs) + "\n")
print(len(jobs), "jobs")
