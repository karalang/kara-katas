# Writes data/: the jobs (data/jobs.jsonl), an access log for the API
# program (data/requests.csv) and a task queue for the worker program
# (data/tasks.jsonl).
#
# A job is a list of steps that make loggers, configure structlog, call
# log methods and look at what came out. Values that JSON has no word for
# are tagged: {"$bytes": hex}, {"$tuple": [...]}, {"$float": "nan"},
# {"$dict": [[key, value], ...]} for keys that are not strings,
# {"$obj": {...}} for an object with its own repr, and {"$exc": {...}}
# for an exception.
import json
import os
import random

jobs = []


def job(name, *steps):
    jobs.append({"name": name, "steps": list(steps)})


# --- values -------------------------------------------------------------

def B(s):
    if isinstance(s, str):
        s = s.encode("utf-8")
    return {"$bytes": s.hex()}


def T(*items):
    return {"$tuple": list(items)}


def F(s):
    return {"$float": s}


def D(*pairs):
    return {"$dict": [list(p) for p in pairs]}


def O(r, s=None, sl=None):
    d = {"repr": r}
    if s is not None:
        d["str"] = s
    if sl is not None:
        d["structlog"] = sl
    return {"$obj": d}


def E(cls, *args, module=None, cause=None, context=None, notes=None, suppress=None):
    d = {"type": cls, "args": list(args)}
    if module is not None:
        d["module"] = module
    if cause is not None:
        d["cause"] = cause["$exc"]
    if context is not None:
        d["context"] = context["$exc"]
    if notes is not None:
        d["notes"] = notes
    if suppress is not None:
        d["suppress"] = suppress
    return {"$exc": d}


# --- steps --------------------------------------------------------------

def call(log, m, *args, **kw):
    return {"op": "call", "log": log, "m": m, "args": list(args), "kw": kw}


def callkw(log, m, args, kw):
    return {"op": "call", "log": log, "m": m, "args": list(args), "kw": kw}


def get(name, *factory_args, **init):
    return {"op": "get", "as": name, "args": list(factory_args), "init": init}


def wrap(name, wrapped, procs=None, wrapper=None, cache=None, **init):
    d = {"op": "wrap", "as": name, "wrapped": wrapped, "init": init}
    if procs is not None:
        d["procs"] = procs
    if wrapper is not None:
        d["wrapper"] = wrapper
    if cache is not None:
        d["cache"] = cache
    return d


def configure(procs=None, wrapper=None, factory=None, cache=None):
    d = {"op": "configure"}
    if procs is not None:
        d["procs"] = procs
    if wrapper is not None:
        d["wrapper"] = wrapper
    if factory is not None:
        d["factory"] = factory
    if cache is not None:
        d["cache"] = cache
    return d


def bind(log, name, **kw):
    return {"op": "bind", "log": log, "as": name, "kw": kw}


def new(log, name, **kw):
    return {"op": "new", "log": log, "as": name, "kw": kw}


def unbind(log, name, *keys):
    return {"op": "unbind", "log": log, "as": name, "keys": list(keys)}


def try_unbind(log, name, *keys):
    return {"op": "try_unbind", "log": log, "as": name, "keys": list(keys)}


def context(log):
    return {"op": "context", "log": log}


def eq(a, b):
    return {"op": "eq", "a": a, "b": b}


def note(text):
    return {"op": "print", "text": text}


def clock(us):
    return {"op": "clock", "us": us}


def raising(exc, *body):
    return {"op": "try", "exc": exc["$exc"], "body": list(body)}


def capture(*body):
    return {"op": "capture", "body": list(body)}


def calls(name):
    return {"op": "calls", "name": name}


def entries(name):
    return {"op": "entries", "name": name}


def ctx_bind(**kw):
    return {"op": "ctx_bind", "kw": kw}


def ctx_unbind(*keys):
    return {"op": "ctx_unbind", "keys": list(keys)}


def ctx_bound(kw, *body):
    return {"op": "ctx_bound", "kw": kw, "body": list(body)}


def styles(name, colors=None, mapping=None):
    d = {"op": "styles", "name": name}
    if colors is not None:
        d["colors"] = colors
    if mapping is not None:
        d["map"] = mapping
    return d


def show(name):
    return {"op": "show", "name": name}


CTX_GET = {"op": "ctx_get"}
CTX_CLEAR = {"op": "ctx_clear"}
RESET = {"op": "reset"}


def merged(log):
    return {"op": "merged", "log": log}


# --- processors and wrapped loggers -------------------------------------

def P(_p, **kw):
    d = {"p": _p}
    d.update(kw)
    return d


KV = P("KeyValueRenderer")
KVS = P("KeyValueRenderer", sort_keys=True)
LEVEL = "add_log_level"
RETURN = {"t": "return"}
PRINT = {"t": "print"}
GENERIC = "generic"


def flt(n):
    return "filter:%d" % n


def capturing(name):
    return {"t": "capturing", "name": name}


# --- the jobs -----------------------------------------------------------

job("the default configuration",
    clock(1714564800000000),
    get("log"),
    call("log", "info", "hello", user="alice", n=3),
    call("log", "debug", "details", items=[1, 2.5, None]),
    call("log", "warning", "disk low", pct=91.5, mount="/var"),
    call("log", "error", "write failed", path="/var/log/app.log"),
    call("log", "critical", "out of memory"),
    call("log", "msg", "msg logs at info"),
    call("log", "warn", "warn is warning"),
    call("log", "fatal", "fatal is error, not critical"),
    call("log", "exception", "no exception is being handled"),
    call("log", "info", "a str stays bare", s="two words", q="it's", b=B("raw")),
    call("log", "info", "", empty=""),
    call("log", "info", "stack_info=False is dropped", stack_info=False))

job("log() takes a level number",
    clock(1714564801000000),
    get("log"),
    call("log", "log", 20, "twenty is info"),
    call("log", "log", 50, "%s=%d", "answer", 42),
    call("log", "log", 10, "ten is debug"),
    call("log", "log", 25, "no name for 25"),
    call("log", "log", 0, "notset has no name either"),
    call("log", "log", "info", "a str is not a level"),
    call("log", "log", 40),
    call("log", "log"))

job("positional arguments are %-formatted",
    wrap("log", RETURN, [P("KeyValueRenderer", key_order=["event"])], flt(20)),
    call("log", "info", "user %s logged in from %s", "bob", "10.0.0.7"),
    call("log", "info", "%d%% done", 50),
    call("log", "info", "%5.2f|%-6s|%r|%6s", 3.14159, "ab", "q", "right"),
    call("log", "info", "%05d|%+d|% d|%x|%X|%o|%#x", 42, 7, 3, 255, 255, 8, 255),
    call("log", "info", "%d and %i of floats", 3.99, -2.5),
    call("log", "info", "%.3s|%10.4f|%-8.1f|", "abcdef", 2.0, -0.25),
    call("log", "info", "%s", {"a": 1}),
    call("log", "info", "%s and %r", None, B("x")),
    call("log", "info", "%(a)s", {"a": 1}),
    call("log", "info", "%s %s", 1),
    call("log", "info", "plain", 1),
    call("log", "info", "%d", "x"),
    call("log", "info", "%x", 2.5),
    call("log", "info", "%f", "x"),
    call("log", "info", "%q", 1),
    call("log", "info", "100%", 1),
    call("log", "info", "%s|%d", True, False),
    call("log", "debug", "below the level %s is never formatted %d", "x", "y"),
    call("log", "info", "%-5d|%5s|%.0f|%.1f|%.2f", -3, None, 0.5, 0.25, 2.675))

job("the event argument",
    wrap("log", RETURN, [LEVEL, KV], flt(20)),
    call("log", "info"),
    call("log", "debug"),
    callkw("log", "info", ["a"], {"event": "b"}),
    callkw("log", "info", [], {"event": "given by keyword"}),
    call("log", "exception"),
    call("log", "info", None, a=1),
    call("log", "info", 42),
    call("log", "info", ["a", "list"], n=1))

job("the generic BoundLogger",
    wrap("log", RETURN, [LEVEL, KVS], GENERIC),
    call("log", "info", "info"),
    call("log", "failure", "any method name reaches the processors"),
    call("log", "exception", "exception maps to error"),
    call("log", "warn", "warn maps to warning"),
    call("log", "info"),
    call("log", "info", "one", "two"),
    callkw("log", "info", ["x"], {"event": "y"}),
    callkw("log", "info", [], {"method_name": "m"}),
    call("log", "trace", "ReturnLogger has no trace"),
    call("log", "log", 20, "log is just a name here"),
    call("log", "log", "with one argument"))

job("the generic BoundLogger over a PrintLogger",
    wrap("log", PRINT, [LEVEL, P("KeyValueRenderer", key_order=["level", "event"])], GENERIC),
    call("log", "err", "err"),
    call("log", "failure", "failure"),
    call("log", "notice", "PrintLogger has no notice"),
    call("log", "msg", "msg"),
    call("log", "debug", "the generic logger never filters"))

job("bind, unbind and try_unbind",
    wrap("base", RETURN, [KV], flt(0)),
    bind("base", "log", a=1, b=2),
    bind("log", "l2", c=3, a=10),
    call("l2", "info", "a keeps its place"),
    unbind("l2", "l3", "b"),
    call("l3", "info", "b is gone"),
    unbind("l2", "bad", "zzz"),
    unbind("l2", "bad2", "c", "zzz"),
    try_unbind("l2", "l4", "zzz", "a"),
    call("l4", "info", "zzz was never there"),
    context("log"), context("l2"), context("l3"), context("l4"),
    eq("log", "log"), eq("log", "l2"), eq("l2", "l3"),
    bind("log", "l5"),
    eq("log", "l5"),
    call("l2", "info", "an event keyword wins", a=99, c=None))

job("new() clears the context it is called on",
    wrap("base", RETURN, [KV], flt(0)),
    bind("base", "b", x=1, y=2),
    new("b", "c", z=3),
    call("b", "info", "b lost x and y"),
    call("c", "info", "c has only z"),
    context("b"),
    bind("c", "d", w=4),
    new("d", "e"),
    call("c", "info", "c keeps z"),
    call("e", "info", "e is empty"))

job("a lazy proxy's new() keeps its initial values",
    configure([KVS], flt(0), RETURN),
    get("p", svc="api", region="eu"),
    new("p", "n", req=1),
    call("n", "info", "from new"),
    call("p", "info", "from the proxy"),
    context("p"),
    unbind("p", "u", "region"),
    call("u", "info", "unbound"),
    try_unbind("p", "t", "region", "nope"),
    call("t", "info", "tried"),
    unbind("p", "bad", "nope"),
    bind("p", "b", svc="override"),
    call("b", "info", "rebound"))

job("cache_logger_on_first_use",
    configure([KVS], flt(0), RETURN, cache=True),
    get("p", a=1),
    call("p", "info", "first use fixes the processors"),
    configure([P("JSONRenderer")]),
    call("p", "info", "still the KeyValueRenderer"),
    get("q"),
    call("q", "info", "a new proxy sees the JSONRenderer"),
    bind("p", "b"),
    eq("b", "b"),
    new("b", "c"),
    call("p", "info", "new() on the cached logger cleared the proxy's a"),
    bind("p", "d", k=2),
    call("d", "info", "bind with values copies"),
    call("p", "info", "the proxy is unchanged"))

job("without the cache every use builds a logger",
    configure([KVS], flt(0), RETURN),
    get("p", a=1),
    call("p", "info", "first"),
    configure([P("JSONRenderer")]),
    call("p", "info", "second"),
    bind("p", "b"),
    new("b", "c"),
    call("p", "info", "new() cleared a copy"),
    configure(cache=True),
    wrap("w", RETURN, [KV], cache=False, x=1),
    call("w", "info", "this proxy opts out"),
    configure([KVS]),
    call("w", "info", "and so sees the new processors"))

for lv in (10, 20, 30, 40, 50):
    job("make_filtering_bound_logger(%d)" % lv,
        wrap("log", RETURN, [P("method"), LEVEL, KV], flt(lv)),
        call("log", "debug", "debug"),
        call("log", "info", "info"),
        call("log", "msg", "msg"),
        call("log", "warning", "warning"),
        call("log", "warn", "warn"),
        call("log", "error", "error"),
        call("log", "fatal", "fatal"),
        call("log", "exception", "exception"),
        call("log", "critical", "critical"),
        call("log", "log", 30, "log 30"),
        call("log", "trace", "trace"))

job("make_filtering_bound_logger with no such level",
    configure(wrapper=flt(25)),
    configure(wrapper=flt(0), procs=[P("add", kw={"configured": True}), KV], factory=RETURN),
    get("log"),
    call("log", "info", "the bad level changed nothing"))

job("exception() and exc_info",
    wrap("log", RETURN, [LEVEL, "format_exc_info", P("KeyValueRenderer", key_order=["level", "event"])], flt(0)),
    raising(E("ValueError", "bad input"),
            call("log", "exception", "failed"),
            call("log", "exception", "exc_info=False wins", exc_info=False),
            call("log", "error", "error with exc_info", exc_info=True),
            call("log", "info", "a truthy str", exc_info="yes"),
            call("log", "info", "zero is falsy", exc_info=0)),
    call("log", "exception", "outside an except block"),
    call("log", "error", "an instance", exc_info=E("KeyError", "user_id")),
    call("log", "error", "an empty list is falsy", exc_info=[]),
    call("log", "error", "a list is truthy", exc_info=[0]))

job("exceptions as format_exc_info prints them",
    wrap("log", RETURN, ["format_exc_info", P("KeyValueRenderer", key_order=["event", "exception"], repr_native_str=False)], flt(0)),
    call("log", "error", "no args", exc_info=E("RuntimeError")),
    call("log", "error", "two args", exc_info=E("ValueError", "a", 1)),
    call("log", "error", "KeyError prints its repr", exc_info=E("KeyError", "it's")),
    call("log", "error", "a module", exc_info=E("CardDeclined", "insufficient funds", module="billing.errors")),
    call("log", "error", "__main__ is left out", exc_info=E("AppError", "x", module="__main__")),
    call("log", "error", "raise from", exc_info=E("RuntimeError", "charge failed", cause=E("ConnectionError", "reset by peer"))),
    call("log", "error", "during handling", exc_info=E("TypeError", "cleanup broke", context=E("OSError", "disk full"))),
    call("log", "error", "suppressed", exc_info=E("TypeError", "quiet", context=E("OSError", "hidden"), suppress=True)),
    call("log", "error", "cause beats context", exc_info=E("ValueError", "v", cause=E("KeyError", "k"), context=E("OSError", "o"))),
    call("log", "error", "a chain of three", exc_info=E("RuntimeError", "top", cause=E("ValueError", "middle", context=E("ZeroDivisionError", "division by zero")))),
    call("log", "error", "notes", exc_info=E("ValueError", "bad row", notes=["row 7", "line one\nline two"])),
    call("log", "error", "an empty message", exc_info=E("ValueError", "")),
    call("log", "error", "a non-str arg", exc_info=E("TimeoutError", 30)))

job("dict_tracebacks",
    wrap("log", RETURN, [LEVEL, "dict_tracebacks", P("JSONRenderer", sort_keys=True)], flt(0)),
    raising(E("ValueError", "bad input"),
            call("log", "exception", "inside")),
    call("log", "error", "an instance", exc_info=E("KeyError", "k", cause=E("OSError", "o"))),
    call("log", "error", "two args", exc_info=E("ValueError", "a", B("b"))),
    call("log", "error", "outside", exc_info=True),
    call("log", "error", "falsy", exc_info=None))

job("the ConsoleRenderer without colors",
    clock(1714564802000000),
    wrap("log", RETURN, [LEVEL, P("TimeStamper", fmt="iso"), P("ConsoleRenderer", colors=False)], flt(0)),
    call("log", "info", "values", s="text", n=3, f=1.5, none=None, l=[1, "a"], d={"k": B("v")}, t=T(1)),
    call("log", "warning", "an event longer than the thirty columns it is padded to", x=1),
    call("log", "info", "short", logger="db", logger_name="db.pool"),
    call("log", "info", "unsorted keys sort", zeta=1, alpha=2, mid=3),
    call("log", "info", "a str with quotes", q="it's \"quoted\"", nl="two\nlines"),
    call("log", "info", "objects", o=O("<Point x=1 y=2>", "(1, 2)")),
    call("log", "info", "an exception value", e=E("ValueError", "x")),
    call("log", "error", "exc_info prints below", exc_info=E("ValueError", "bad", notes=["see docs"])),
    call("log", "error", "exc_info=True outside prints nothing", exc_info=True),
    call("log", "error", "an exception key", exception="Traceback text\nhere"),
    call("log", "info", "", timestamp=""),
    wrap("raw", RETURN, [P("ConsoleRenderer", colors=False)], flt(0)),
    call("raw", "info", "a level with no style", level="trace"),
    call("raw", "info", "a short level", level="x"),
    call("raw", "info", "a level padded past nine", level="verbose_debug"))

job("ConsoleRenderer options",
    clock(1714564803000000),
    wrap("pad", RETURN, [LEVEL, P("ConsoleRenderer", colors=False, pad_event=12, pad_level=False)], flt(0)),
    call("pad", "info", "short", k=1),
    call("pad", "critical", "longer than twelve", k=2),
    wrap("raw", RETURN, [LEVEL, P("ConsoleRenderer", colors=False, repr_native_str=True, sort_keys=False)], flt(0)),
    call("raw", "info", "repr_native_str", zeta="z", alpha="a", n=1),
    wrap("keys", RETURN, [LEVEL, P("TimeStamper", fmt="%H:%M:%S", key="ts"), P("EventRenamer", to="msg"),
                          P("ConsoleRenderer", colors=False, event_key="msg", timestamp_key="ts", pad_event=0)], flt(0)),
    call("keys", "info", "renamed", user="u"),
    wrap("none", RETURN, [P("ConsoleRenderer", colors=False)], flt(0)),
    call("none", "info", "no level, no timestamp", a=1),
    call("none", "info", "a timestamp of any type", timestamp=1714564800.5),
    call("none", "info", "trailing blanks are stripped"))

job("the ConsoleRenderer with colors",
    clock(1714564804000000),
    wrap("log", RETURN, [LEVEL, P("TimeStamper", fmt="%H:%M:%S"), P("ConsoleRenderer", colors=True)], flt(0)),
    call("log", "debug", "debug", a=1),
    call("log", "info", "info", s="text"),
    call("log", "warning", "warning"),
    call("log", "error", "error", exc_info=E("RuntimeError", "boom")),
    call("log", "critical", "critical", logger="core"),
    wrap("raw", RETURN, [P("ConsoleRenderer", colors=True)], flt(0)),
    call("raw", "info", "notset", level="notset"),
    call("raw", "info", "unknown level", level="trace"),
    wrap("pl", RETURN, [LEVEL, P("ConsoleRenderer", colors=True, pad_level=False, pad_event=8)], flt(0)),
    call("pl", "info", "x", k="v"))

job("level_styles is changed in place",
    styles("S", colors=True),
    show("S"),
    wrap("one", RETURN, [LEVEL, P("ConsoleRenderer", colors=True, level_styles="S")], flt(0)),
    show("S"),
    wrap("two", RETURN, [LEVEL, P("ConsoleRenderer", colors=True, level_styles="S")], flt(0)),
    show("S"),
    call("one", "info", "built first"),
    call("two", "info", "built second"),
    styles("C", mapping={"info": "<I>", "oops": "<O>"}),
    wrap("c", RETURN, [LEVEL, P("ConsoleRenderer", colors=False, level_styles="C")], flt(0)),
    show("C"),
    call("c", "info", "the widest key is four"),
    call("c", "warning", "no style"),
    styles("P", colors=False),
    wrap("p", RETURN, [LEVEL, P("ConsoleRenderer", colors=False, level_styles="P")], flt(0)),
    show("P"),
    call("p", "info", "plain"),
    styles("E", mapping={}),
    wrap("e", RETURN, [LEVEL, P("ConsoleRenderer", colors=False, level_styles="E")], flt(0)))

job("KeyValueRenderer options",
    wrap("plain", RETURN, [LEVEL, KV], flt(0)),
    call("plain", "info", "insertion order", b=1, a="x", c=[1]),
    wrap("sorted", RETURN, [LEVEL, KVS], flt(0)),
    call("sorted", "info", "sorted", b=1, a="x", c=[1]),
    wrap("order", RETURN, [LEVEL, P("KeyValueRenderer", key_order=["event", "missing", "level"])], flt(0)),
    call("order", "info", "key_order first", z=1, a=2),
    wrap("both", RETURN, [LEVEL, P("KeyValueRenderer", key_order=["level", "missing"], sort_keys=True)], flt(0)),
    call("both", "info", "then sorted", z=1, a=2),
    wrap("drop", RETURN, [LEVEL, P("KeyValueRenderer", key_order=["missing", "event", "none"], drop_missing=True)], flt(0)),
    call("drop", "info", "drop_missing", none=None, x=1),
    wrap("native", RETURN, [LEVEL, P("KeyValueRenderer", repr_native_str=False)], flt(0)),
    call("native", "info", "bare strs", s="two words", q="it's", n=1, b=B("b")))

job("LogfmtRenderer",
    wrap("log", RETURN, [LEVEL, P("LogfmtRenderer")], flt(0)),
    call("log", "info", "plain", n=1, f=2.5, s="word"),
    call("log", "info", "needs quotes", s="two words", eq="a=b", q='say "hi"'),
    call("log", "info", "backslashes", alone="C:\\temp", spaced="C:\\Program Files", nl="a\nb", tab="a\tb"),
    call("log", "info", "flags", on=True, off=False, none=None),
    call("log", "info", "containers", l=[1, 2], d={"a": 1}, t=T(), b=B("x y"), e="", u="café"),
    callkw("log", "info", ["bad key"], {"my key": 1}),
    callkw("log", "info", ["tab key"], {"a\tb": 1}),
    callkw("log", "info", ["empty key"], {"": 1}),
    wrap("opts", RETURN, [LEVEL, P("LogfmtRenderer", key_order=["level", "event", "missing"], bool_as_flag=False)], flt(0)),
    call("opts", "info", "bools spelled out", on=True, off=False),
    wrap("dm", RETURN, [LEVEL, P("LogfmtRenderer", key_order=["missing", "event"], drop_missing=True, sort_keys=True)], flt(0)),
    call("dm", "info", "dropped and sorted", z=None, a=1))

job("JSONRenderer",
    wrap("log", RETURN, [LEVEL, P("JSONRenderer")], flt(0)),
    call("log", "info", "types", i=1, f=2.5, s="x", n=None, b=True, l=[1, [2]], d={"a": {"b": []}}, t=T(1, 2)),
    call("log", "info", "fallbacks", raw=B("\x00\xff"), o=O("<Conn #4>"), e=E("ValueError", "x")),
    call("log", "info", "__structlog__", o=O("<User 7>", sl={"id": 7, "name": "ada"}), r=O("<R>", sl=O("<inner>"))),
    call("log", "info", "floats", nan=F("nan"), inf=F("inf"), ninf=F("-inf"), big=1e22, small=1e-7, neg=-0.0),
    call("log", "info", "keys", d=D([1, "int"], [True, "bool"], [None, "none"], [2.5, "float"], [False, 0])),
    call("log", "info", "a tuple key", d=D([T(1, 2), "x"])),
    call("log", "info", "escapes", s="tab\there \"q\" back\\slash\u0001\u007f", u="café ☕ 😀"),
    wrap("sk", RETURN, [LEVEL, P("JSONRenderer", sort_keys=True, indent=2)], flt(0)),
    call("sk", "info", "sorted and indented", z=1, a={"y": [1, {}], "x": []}),
    wrap("na", RETURN, [P("JSONRenderer", ensure_ascii=False, separators=[",", ":"])], flt(0)),
    call("na", "info", "not ascii", u="café ☕ 😀", c="\u0001\u007f"),
    wrap("i0", RETURN, [P("JSONRenderer", indent=0)], flt(0)),
    call("i0", "info", "indent zero", l=[1, 2]))

job("TimeStamper",
    clock(1714564800000000),
    wrap("iso", RETURN, [P("TimeStamper", fmt="iso"), KV], flt(0)),
    call("iso", "info", "utc iso has a Z and no zero microseconds"),
    call("iso", "info", "a quarter second later"),
    wrap("isol", RETURN, [P("TimeStamper", fmt="ISO", utc=False), KV], flt(0)),
    call("isol", "info", "local iso is naive"),
    wrap("unix", RETURN, [P("TimeStamper"), KV], flt(0)),
    call("unix", "info", "unix"),
    call("unix", "info", "unix"),
    wrap("f1", RETURN, [P("TimeStamper", fmt="%d/%b/%Y:%H:%M:%S %z", key="time"), KV], flt(0)),
    call("f1", "info", "apache style"),
    wrap("f2", RETURN, [P("TimeStamper", fmt="%a %A %B %j %y %I%p %f %Z|%z|%%", utc=False), KV], flt(0)),
    call("f2", "info", "local, so no zone"),
    wrap("f3", RETURN, [P("TimeStamper", fmt="%a %A %B %j %y %I%p %f %Z", utc=True), KV], flt(0)),
    call("f3", "info", "utc"),
    clock(1735689599999999),
    call("iso", "info", "the last microsecond of 2024"),
    call("f2", "info", "the first of 2025, local"),
    clock(951825600000000),
    call("f3", "info", "a leap day"),
    wrap("bad", RETURN, [P("TimeStamper", utc=False), KV], flt(0)),
    wrap("maybe", RETURN, [P("MaybeTimeStamper", fmt="iso"), KV], flt(0)),
    call("maybe", "info", "adds one"),
    call("maybe", "info", "keeps one", timestamp="given"),
    wrap("mk", RETURN, [P("MaybeTimeStamper", fmt="iso", key="ts"), KV], flt(0)),
    call("mk", "info", "looks for timestamp, not ts", ts="given"),
    call("mk", "info", "so timestamp stops it", timestamp="t"))

job("EventRenamer",
    wrap("log", RETURN, [P("EventRenamer", to="msg"), KV], GENERIC),
    call("log", "info", "renamed", a=1),
    call("log", "info"),
    wrap("rb", RETURN, [P("EventRenamer", to="message", replace_by="_event"), KV], flt(0)),
    callkw("rb", "info", ["took the event"], {"_event": "user.login", "u": 1}),
    call("rb", "info", "no _event"),
    callkw("rb", "info", ["None counts as missing"], {"_event": None}),
    wrap("same", RETURN, [P("EventRenamer", to="event"), KV], flt(0)),
    call("same", "info", "renamed to itself", a=1))

job("UnicodeEncoder and UnicodeDecoder",
    wrap("enc", RETURN, [P("UnicodeEncoder"), KV], flt(0)),
    call("enc", "info", "café", n=1, b=B("x")),
    wrap("asc", RETURN, [P("UnicodeEncoder", encoding="ascii"), KV], flt(0)),
    call("asc", "info", "backslashreplace", s="café ☕ 😀"),
    wrap("rep", RETURN, [P("UnicodeEncoder", encoding="ascii", errors="replace"), KV], flt(0)),
    call("rep", "info", "replace", s="café ☕ 😀"),
    wrap("ign", RETURN, [P("UnicodeEncoder", encoding="ascii", errors="ignore"), KV], flt(0)),
    call("ign", "info", "ignore", s="café ☕ 😀"),
    wrap("strict", RETURN, [P("UnicodeEncoder", encoding="ascii", errors="strict"), KV], flt(0)),
    call("strict", "info", "plain ascii is fine"),
    call("strict", "info", "café"),
    wrap("dec", RETURN, [P("UnicodeDecoder"), KV], flt(0)),
    call("dec", "info", "decoded", ok=B("café"), bad=B(b"a\xffb"), cut=B(b"x\xe2\x98"), mid=B(b"\xe2\x98z"), n=1),
    wrap("round", RETURN, [P("UnicodeEncoder"), P("UnicodeDecoder"), P("JSONRenderer")], flt(0)),
    call("round", "info", "there and back", s="naïve"))

job("contextvars",
    wrap("log", RETURN, ["merge_contextvars", KVS], flt(0)),
    ctx_bind(request_id="r-1", user="ada"),
    call("log", "info", "merged in"),
    call("log", "info", "an event value wins", user="bob"),
    bind("log", "b", request_id="bound"),
    call("b", "info", "a bound value wins too"),
    CTX_GET,
    merged("b"),
    ctx_unbind("user", "never_bound"),
    call("log", "info", "user unbound"),
    ctx_bind(user=None),
    call("log", "info", "None is a value"),
    ctx_bound({"request_id": "inner", "span": 7},
              call("log", "info", "inside bound_contextvars"),
              CTX_GET),
    call("log", "info", "restored, and span is gone"),
    CTX_GET,
    CTX_CLEAR,
    call("log", "info", "cleared"),
    CTX_GET,
    ctx_bound({"only": 1},
              call("log", "info", "a fresh key")),
    call("log", "info", "a key bound only in the block is unbound after"))

job("contextvars are cleared between jobs",
    wrap("log", RETURN, ["merge_contextvars", KVS], flt(0)),
    call("log", "info", "nothing left over"),
    CTX_GET)

job("capture_logs",
    clock(1714564805000000),
    get("log"),
    call("log", "info", "printed before"),
    capture(call("log", "info", "captured", a=1),
            call("log", "warning", "also captured"),
            call("log", "exception", "exception"),
            call("log", "debug", "debug too"),
            get("other", "factory", "args"),
            call("other", "info", "a new logger is captured too")),
    call("log", "info", "printed after"))

job("capture_logs keeps a configured chain",
    configure([LEVEL, KV], flt(20), RETURN),
    get("log"),
    call("log", "info", "rendered"),
    capture(call("log", "info", "captured", x=1),
            call("log", "debug", "filtered before the chain"),
            call("log", "warn", "warn")),
    call("log", "info", "rendered again"))

job("a cached logger sees capture_logs",
    configure([LEVEL, KV], flt(0), RETURN, cache=True),
    get("log"),
    call("log", "info", "cached"),
    capture(call("log", "info", "the default list is changed in place")),
    configure([P("JSONRenderer")]),
    capture(call("log", "info", "but now it has its own list")),
    call("log", "info", "rendered by the old list"))

job("LogCapture as a processor",
    wrap("log", RETURN, [P("LogCapture", name="cap"), KV], GENERIC),
    call("log", "info", "one", a=1),
    call("log", "exception", "exception"),
    call("log", "warn", "warn"),
    call("log", "custom", "custom"),
    entries("cap"),
    wrap("f", RETURN, [P("LogCapture", name="cap2")], flt(30)),
    call("f", "info", "filtered"),
    call("f", "fatal", "fatal"),
    entries("cap2"))

job("dropping events",
    wrap("log", RETURN, [LEVEL, P("drop_if", key="level", value="debug"), KV], flt(0)),
    call("log", "debug", "dropped"),
    call("log", "info", "kept"),
    wrap("s", RETURN, [P("sample", event="heartbeat", every=3), KV], flt(0)),
    call("s", "info", "heartbeat", n=1),
    call("s", "info", "heartbeat", n=2),
    call("s", "info", "other"),
    call("s", "info", "heartbeat", n=3),
    call("s", "info", "heartbeat", n=4),
    call("s", "info", "heartbeat", n=5),
    call("s", "info", "heartbeat", n=6))

job("what the last processor returns",
    wrap("t", RETURN, [P("as_tuple")], flt(0)),
    call("t", "info", "a tuple is (args, kwargs)", a=1),
    wrap("d", RETURN, [LEVEL], flt(0)),
    call("d", "info", "a dict becomes keyword arguments", a=1),
    wrap("s", RETURN, [P("return", value="just this")], flt(0)),
    call("s", "info", "ignored"),
    wrap("b", RETURN, [P("return", value=B("bytes"))], flt(0)),
    call("b", "info", "ignored"),
    wrap("i", RETURN, [P("return", value=42)], flt(0)),
    call("i", "info", "an int"),
    wrap("n", RETURN, [P("return", value=None)], flt(0)),
    call("n", "info", "None"),
    wrap("l", RETURN, [P("return", value=["a", "list"])], flt(0)),
    call("l", "info", "a list"),
    wrap("e", RETURN, [], flt(0)),
    call("e", "info", "no processors at all", k=1),
    wrap("pt", RETURN, [P("return", value=T(T("a", "b"), {"k": 1}))], flt(0)),
    call("pt", "info", "ignored"))

job("a PrintLogger takes one message",
    wrap("d", PRINT, [LEVEL], flt(0)),
    call("d", "info", "a dict"),
    wrap("e", PRINT, [P("return", value={})], flt(0)),
    call("e", "info", "an empty dict"),
    wrap("m", PRINT, [P("return", value={"message": "by keyword"})], flt(0)),
    call("m", "info", "message as a keyword"),
    wrap("t", PRINT, [P("return", value=T(T("a", "b"), {}))], flt(0)),
    call("t", "info", "two arguments"),
    wrap("mm", PRINT, [P("return", value=T(T("a"), {"message": "b"}))], flt(0)),
    call("mm", "info", "message twice"),
    wrap("b", PRINT, [P("return", value=B("bytes print as a repr"))], flt(0)),
    call("b", "info", "bytes"),
    wrap("ok", PRINT, [KV], flt(0)),
    call("ok", "info", "a str"))

job("WriteLogger and BytesLogger",
    wrap("w", {"t": "write"}, [KV], flt(0)),
    call("w", "info", "write logger"),
    wrap("wb", {"t": "write"}, [P("return", value=B("b"))], flt(0)),
    call("wb", "info", "bytes"),
    wrap("wd", {"t": "write"}, [LEVEL], flt(0)),
    call("wd", "info", "a dict"),
    wrap("bl", {"t": "bytes"}, [KV, P("encode")], flt(0)),
    call("bl", "info", "bytes logger", u="café"),
    wrap("bs", {"t": "bytes"}, [KV], flt(0)),
    call("bs", "info", "a str"),
    wrap("bt", {"t": "bytes"}, [P("return", value=T(T(B("a")), {}))], flt(0)),
    call("bt", "info", "a tuple"))

job("CapturingLogger",
    wrap("log", capturing("c"), [LEVEL, KV], GENERIC),
    call("log", "info", "info"),
    call("log", "anything_goes", "x"),
    wrap("raw", capturing("c"), [LEVEL], flt(0)),
    call("raw", "warning", "as kwargs", k=1),
    wrap("tup", capturing("c"), [P("return", value=T(T(1, 2), {"a": B("b")}))], flt(0)),
    call("tup", "info", "ignored"),
    calls("c"),
    calls("c"),
    configure([LEVEL, KV], flt(0), capturing("d")),
    get("p"),
    get("q"),
    call("p", "info", "from p"),
    call("q", "info", "from q, the same logger"),
    calls("d"))

job("processors that raise",
    wrap("log", RETURN, [LEVEL, P("raise", exc=E("RuntimeError", "processor broke")), KV], flt(0)),
    call("log", "info", "boom"),
    wrap("k", RETURN, [P("raise", exc=E("KeyError", "missing")), KV], flt(0)),
    call("k", "info", "boom"),
    wrap("ok", RETURN, [P("drop_if", key="skip", value=True), P("raise", exc=E("ValueError", "after the drop")), KV], flt(0)),
    call("ok", "info", "dropped first", skip=True),
    call("ok", "info", "reaches the raise", skip=False))

job("the context and the event dict",
    wrap("base", RETURN, [KV], GENERIC),
    bind("base", "log", event="from the context", user="a"),
    call("log", "info", "the event argument wins"),
    call("log", "info"),
    callkw("log", "info", [], {"user": "b", "event": "keyword"}),
    bind("log", "l2", level="bound"),
    wrap("lv", RETURN, [LEVEL, KV], flt(0), level="initial"),
    call("lv", "info", "add_log_level overwrites in place"),
    bind("lv", "lv2", z=1),
    call("lv2", "warning", "and keeps the place"))

job("values in the KeyValueRenderer",
    wrap("log", RETURN, [KV], flt(0)),
    call("log", "info", "repr", e=E("KeyError", "k"), e2=E("ValueError"), o=O("<Obj>", "str of obj"),
         t=T(1), t2=T(), t3=T("a", None), d=D([1, 2], [T(1), [3]]), f=1e16, g=1.0, h=0.1 + 0.2,
         neg=-0.0, nan=F("nan"), inf=F("-inf"), s="tab\tnew\nline", q="'\"", u="é\u00a0\u200b",
         big=2 ** 62, nb=B(b"\x00\t\\'\""), nb2=B(b"'"), emp=B(b"")))

job("set_exc_info",
    wrap("log", RETURN, ["set_exc_info", "format_exc_info", P("KeyValueRenderer", key_order=["event"])], GENERIC),
    call("log", "exception", "outside"),
    raising(E("ConnectionError", "refused"),
            call("log", "exception", "inside"),
            call("log", "exception", "explicit False", exc_info=False),
            call("log", "error", "error is not exception")),
    wrap("f", RETURN, ["set_exc_info", "format_exc_info", P("KeyValueRenderer", key_order=["event"])], flt(0)),
    raising(E("ConnectionError", "refused"),
            call("f", "exception", "the filtering logger calls error"),
            call("f", "error", "error alone")))

job("exceptions in the default configuration",
    clock(1714564806000000),
    get("log"),
    raising(E("ValueError", "invalid literal for int() with base 10: 'x'"),
            call("log", "exception", "parse failed", line=3)),
    raising(E("PaymentError", "card declined", module="shop.payments", cause=E("TimeoutError", "gateway")),
            call("log", "error", "payment", exc_info=True, order=17)),
    call("log", "error", "a formatted exception wins over exc_info", exception="pre-formatted",
         exc_info=E("ValueError", "x")),
    call("log", "error", "a formatted exception alone", exception="pre-formatted"))

job("configure, then reset_defaults",
    configure([LEVEL, KV], flt(30), RETURN),
    get("log"),
    call("log", "info", "filtered"),
    call("log", "warning", "configured"),
    RESET,
    clock(1714564807000000),
    call("log", "info", "the proxy reads the defaults again"),
    configure(factory=RETURN),
    call("log", "info", "only the factory changed"),
    configure(wrapper=GENERIC),
    call("log", "notice", "only the wrapper changed"))

job("note on positional arguments to a lazy proxy",
    configure([KV], flt(0), RETURN),
    get("log", "name", 1),
    call("log", "info", "factory arguments go to the factory, %s", "unused"))


# --- data for the programs ---------------------------------------------

rng = random.Random(197)
paths = [("GET", "/api/orders"), ("GET", "/api/orders/{id}"), ("POST", "/api/orders"),
         ("GET", "/api/users/{id}"), ("DELETE", "/api/orders/{id}"), ("GET", "/health"),
         ("POST", "/api/login")]
users = ["ada", "grace", "linus", "Zoë", "", "björn", "mei"]
rows = []
t = 1714568400000000
for i in range(48):
    t += rng.randrange(40000, 2500000)
    m, p = rng.choice(paths)
    if "{id}" in p:
        p = p.replace("{id}", str(rng.randrange(1, 900)))
    r = rng.random()
    if r < 0.70:
        status = 200 if m != "POST" else 201
    elif r < 0.80:
        status = rng.choice([400, 404, 409])
    elif r < 0.86:
        status = 401
    elif r < 0.92:
        status = 429
    else:
        status = rng.choice([500, 502, 503])
    ms = rng.randrange(2, 400)
    if rng.random() < 0.15:
        ms = rng.randrange(1000, 4500)
    user = rng.choice(users) if p != "/health" else ""
    ip = "10.%d.%d.%d" % (rng.randrange(0, 4), rng.randrange(0, 256), rng.randrange(1, 255))
    auth = ("Bearer tok_%06x" % rng.randrange(1 << 24)) if user and rng.random() < 0.5 else ""
    size = rng.randrange(0, 20000) if status < 400 else rng.randrange(0, 300)
    rows.append([str(t), m, p, str(status), str(ms), user, ip, "req-%04d" % (i + 1), auth, str(size)])

tasks = []
kinds = ["email", "resize", "export", "webhook"]
for i in range(22):
    kind = kinds[i % 4] if i % 7 else rng.choice(kinds)
    outcomes = []
    for a in range(3):
        r = rng.random()
        if r < 0.6:
            outcomes.append("ok")
            break
        elif r < 0.8:
            outcomes.append("TimeoutError:read timed out after 30s")
        elif r < 0.9:
            outcomes.append('ValueError:bad "format" in row %d' % rng.randrange(1, 99))
        else:
            outcomes.append("PermissionError:/srv/out is read-only")
            break
    payload = {"to": "user%d@example.com" % i} if kind == "email" else \
        {"w": rng.choice([64, 128, 1024]), "h": rng.choice([64, 256])} if kind == "resize" else \
        {"rows": rng.randrange(10, 50000)} if kind == "export" else \
        {"url": "https://hooks.example.com/%d" % i, "secret": "s3cr3t-%d" % i}
    tasks.append({"id": "t%03d" % (i + 1), "kind": kind, "payload": payload,
                  "outcomes": outcomes, "heartbeats": rng.randrange(0, 5),
                  "cost_us": rng.randrange(5000, 900000)})

os.makedirs("data", exist_ok=True)
with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j) + "\n")
with open("data/requests.csv", "w") as f:
    f.write("ts_us,method,path,status,ms,user,ip,request_id,authorization,bytes\n")
    for r in rows:
        f.write(",".join(r) + "\n")
with open("data/tasks.jsonl", "w") as f:
    for t in tasks:
        f.write(json.dumps(t) + "\n")
print("%d jobs, %d requests, %d tasks" % (len(jobs), len(rows), len(tasks)))
