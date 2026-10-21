# Writes data/: the TOML files in mk_docs.py (data/docs/), the jobs
# (data/jobs.jsonl), and the repository and service configs the two
# programs work on (data/repo/, data/etc/).
#
# A job is a list of steps that parse documents, read them, change them
# and print them. A value that JSON has no word for is tagged:
# {"$v": name} is a variable a step made, {"$f": "inf"} a float,
# {"$dt"/"$date"/"$time": text} a Python datetime, date or time,
# {"$key": k} a tomlkit key, and {"$call": [fn, args..., {"$kw": {...}}]}
# a call to one of tomlkit's functions.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_docs import DOCS, ETC, REPO  # noqa: E402

jobs = []


def job(name, *steps):
    jobs.append({"name": name, "steps": [list(s) for s in steps]})


def V(n):
    return {"$v": n}


def F(s):
    return {"$f": s}


def DT(s):
    return {"$dt": s}


def DATE(s):
    return {"$date": s}


def TIME(s):
    return {"$time": s}


def K(k):
    return {"$key": k}


def C(fn, *args, **kw):
    a = list(args)
    if kw:
        a.append({"$kw": kw})
    return {"$call": [fn] + a}


# --- reading every document back as it was --------------------------------

for name in DOCS:
    job(f"read {name}", ("rt", name), ("parse", "d", name), ("show", "d"))

job("structure of strings", ("parse", "d", "strings"), ("body", "d"))
job("structure of arrays", ("parse", "d", "arrays"), ("body", "d"))
job("structure of dotted", ("parse", "d", "dotted"), ("body", "d"))
job("structure of netlify", ("parse", "d", "netlify"), ("body", "d"))
job("structure of outoforder", ("parse", "d", "outoforder"), ("body", "d"))
job("structure of dates", ("parse", "d", "dates"), ("body", "d"),
    ("text", "d"))

# --- error messages -------------------------------------------------------

BAD = [
    ("missing value", "a = \n"),
    ("missing equals", "a 1\n"),
    ("two equals", "a == 1\n"),
    ("bare key space", "first name = 1\n"),
    ("empty key", "= 1\n"),
    ("empty table name", "[]\n"),
    ("unterminated table", "[a\nb = 1\n"),
    ("table eof", "[a"),
    ("duplicate key", "a = 1\na = 2\n"),
    ("duplicate key in table", "[t]\nx = 1\nx = 2\n"),
    ("duplicate table", "[t]\nx = 1\n[t]\ny = 2\n"),
    ("table after aot", "[[t]]\nx = 1\n[t]\ny = 2\n"),
    ("aot after table", "[t]\nx = 1\n[[t]]\ny = 2\n"),
    ("dotted redefines table", "[a]\nb.c = 1\n[a.b]\nd = 2\n"),
    ("value then table", "a = 1\n[a]\nb = 2\n"),
    ("leading zero", "n = 012\n"),
    ("double underscore", "n = 1__2\n"),
    ("trailing underscore", "n = 12_\n"),
    ("trailing dot", "n = 1.\n"),
    ("dot exponent", "n = 1.e5\n"),
    ("signed hex", "n = +0x1F\n"),
    ("hex underscore lead", "n = 0x_1F\n"),
    ("bad float", "n = 1.2.3\n"),
    ("plus dot", "n = +.5\n"),
    ("bare word", "n = yes\n"),
    ("bad bool", "b = tru\n"),
    ("bad bool 2", "b = falsey\n"),
    ("bad date", "d = 2024-02-30\n"),
    ("bad datetime", "d = 2024-13-01T00:00:00\n"),
    ("leap second", "d = 2016-12-31T23:59:60Z\n"),
    ("bad time", "t = 25:00:00\n"),
    ("date junk", "d = 2024-01-01 x\n"),
    ("unterminated string", 'a = "abc\n'),
    ("unterminated eof", 'a = "abc'),
    ("bad escape", 'a = "\\q"\n'),
    ("bad unicode", 'a = "\\u12G4"\n'),
    ("surrogate escape", 'a = "\\uD800"\n'),
    ("control char", 'a = "x\u0001y"\n'),
    ("delete char", 'a = "x\u007fy"\n'),
    ("control in comment", "a = 1 # x\u0002\n"),
    ("tab in string ok", 'a = "x\ty"\n'),
    ("newline in basic", 'a = "x\ny"\n'),
    ("six quotes", 'a = """x""""""\n'),
    ("multiline key", 'a."""b""" = 1\n'),
    ("trailing junk", "a = 1 2\n"),
    ("array no comma", "a = [1 2]\n"),
    ("array leading comma", "a = [,1]\n"),
    ("array double comma", "a = [1,,2]\n"),
    ("array eof", "a = [1, 2"),
    ("inline trailing comma", "a = {x = 1,}\n"),
    ("inline leading comma", "a = {, x = 1}\n"),
    ("inline no comma", "a = {x = 1 y = 2}\n"),
    ("inline newline", "a = {x = 1,\n y = 2}\n"),
    ("inline duplicate", "a = {x = 1, x = 2}\n"),
    ("inline eof", "a = {x = 1,"),
    ("table name space", "[a b]\n"),
    ("bad line start", "!x = 1\n"),
    ("only a value", "\"x\"\n"),
    ("backslash ws no newline", 'a = """x\\  y"""\n'),
    ("mixed array", "a = [1, \"x\", 2.5]\n"),
    ("crlf bare cr", "a = 1\rb = 2\n"),
]
for name, src in BAD:
    job(f"error: {name}", ("check", src))

# --- reading items --------------------------------------------------------

job("items of pyproject",
    ("parse", "d", "pyproject"),
    ("print", "d", "tool", "poetry", "version"),
    ("raw", "d", "tool", "poetry", "version"),
    ("print", "d", "tool", "poetry", "classifiers"),
    ("raw", "d", "tool", "poetry", "classifiers"),
    ("print", "d", "tool", "poetry", "dependencies", "markdown-it-py"),
    ("raw", "d", "tool", "poetry", "dependencies", "markdown-it-py"),
    ("print", "d", "tool", "poetry", "dependencies", "watchdog", "optional"),
    ("print", "d", "tool", "poetry", "packages", 0, "from"),
    ("print", "d", "tool", "ruff", "line-length"),
    ("print", "d", "tool"),
    ("super", "d", "tool"),
    ("super", "d", "tool", "poetry"),
    ("super", "d", "build-system"),
    ("keys", "d"),
    ("keys", "d", "tool"),
    ("len", "d", "tool", "poetry"),
    ("print", "d", "tool", "poetry", "nope"),
    ("print", "d", "tool", "poetry", "classifiers", 7),
    ("print", "d", "tool", "poetry", "classifiers", -1),
    ("in", "d", "tool"),
    ("in", "d", "poetry"))

job("items of numbers",
    ("parse", "d", "numbers"),
    *[("raw", "d", k) for k in ["int1", "hex2", "oct1", "bin1", "flt8",
                                "sf2", "sf6", "zero", "big", "odd"]],
    *[("print", "d", k) for k in ["int1", "hex2", "flt4", "sf4", "sf6",
                                  "zero", "big", "odd"]])

job("items of dates",
    ("parse", "d", "dates"),
    *[("print", "d", k) for k in ["odt1", "odt2", "odt3", "odt4", "ldt1",
                                  "ld1", "lt1", "lt2", "nanos", "lower",
                                  "spaced", "pipe", "dates"]],
    *[("raw", "d", k) for k in ["odt4", "nanos", "spaced", "pipe", "dates"]])

job("items of netlify",
    ("parse", "d", "netlify"),
    ("print", "d", "redirects"),
    ("print", "d", "redirects", 1, "status"),
    ("len", "d", "redirects"),
    ("raw", "d", "redirects", 0),
    ("print", "d", "headers", 0, "values"),
    ("super", "d", "context"),
    ("raw", "d", "build"))

job("out of order tables",
    ("parse", "d", "outoforder"),
    ("print", "d", "fruit"),
    ("keys", "d", "fruit"),
    ("print", "d", "fruit", "apple"),
    ("print", "d", "fruit", "apple", "texture"),
    ("set", "d", "fruit", "banana", {"color": "yellow"}),
    ("text", "d"),
    ("set", "d", "fruit", "apple", "color", "green"),
    ("text", "d"),
    ("del", "d", "fruit", "orange"),
    ("text", "d"),
    ("show", "d"))

job("out of order then replace",
    ("parse", "d", "outoforder"),
    ("get", "f", "d", "fruit"),
    ("set", "f", "apple", "fresh"),
    ("text", "d"),
    ("show", "d"),
    ("print", "f", "apple"))

job("dotted keys",
    ("parse", "d", "dotted"),
    ("print", "d", "physical"),
    ("super", "d", "physical"),
    ("raw", "d", "a"),
    ("print", "d", "3"),
    ("set", "d", "physical", "size", "medium"),
    ("text", "d"),
    ("set", "d", "site", "example.org", False),
    ("del", "d", "physical", "color"),
    ("text", "d"),
    ("append", "d", K(["x", "y", "z"]), 9),
    ("text", "d"),
    ("append", "d", K(["u", "v"]), {"w": 1}))

# --- changing documents ---------------------------------------------------

job("bump pyproject",
    ("parse", "d", "pyproject"),
    ("get", "p", "d", "tool", "poetry"),
    ("set", "p", "version", "2.4.0"),
    ("get", "deps", "p", "dependencies"),
    ("set", "deps", "httpx", "^0.27"),
    ("set", "deps", "jinja2", {"version": "^3.1", "extras": ["i18n"]}),
    ("del", "d", "tool", "poetry", "group", "dev", "dependencies", "pytest-cov"),
    ("get", "cls", "p", "classifiers"),
    ("insert", "cls", 2, "Programming Language :: Python :: 3.12"),
    ("push", "cls", "Typing :: Typed"),
    ("set", "d", "tool", "ruff", "line-length", 88),
    ("get", "ign", "d", "tool", "ruff", "lint", "ignore"),
    ("push", "ign", "E501"),
    ("text", "d"))

job("new tables in pyproject",
    ("parse", "d", "pyproject"),
    ("get", "tool", "d", "tool"),
    ("set", "tool", "black", {"line-length": 100, "target-version": ["py39"]}),
    ("set", "tool", "mypy", {"strict": True, "overrides": [
        {"module": "tests.*", "disallow_untyped_defs": False}]}),
    ("set", "d", "project", {"name": "inkwell", "urls": {
        "Homepage": "https://inkwell.example.org"}}),
    ("set", "d", "readme-note", "see README"),
    ("text", "d"),
    ("show", "d", "tool", "mypy"))

job("cargo dependencies",
    ("parse", "d", "cargo"),
    ("get", "deps", "d", "dependencies"),
    ("let", "it", C("inline_table")),
    ("update", "it", {"version": "1.0", "features": ["full"]}),
    ("set", "deps", "tokio", V("it")),
    ("set", "deps", "log", "0.4.21"),
    ("del", "deps", "memmap2"),
    ("get", "feat", "d", "features"),
    ("set", "feat", "mmap", []),
    ("set", "feat", "default", ["std"]),
    ("set", "d", "package", "version", "0.10.0"),
    ("get", "bins", "d", "bin"),
    ("push", "bins", {"name": "ferrite-repair", "path": "src/bin/repair.rs"}),
    ("del", "d", "profile", "release", "debug"),
    ("set", "d", "profile", "release", "strip", "symbols"),
    ("text", "d"),
    ("len", "bins"))

job("cargo aot insert and delete",
    ("parse", "d", "cargo"),
    ("get", "bins", "d", "bin"),
    ("insert", "bins", 0, {"name": "ferrite-first", "path": "src/main.rs"}),
    ("del", "bins", 1),
    ("text", "d"),
    ("set", "bins", 0, {"name": "x"}))

job("workspace members",
    ("parse", "d", "workspace"),
    ("get", "m", "d", "workspace", "members"),
    ("push", "m", "crates/web"),
    ("insert", "m", 0, "crates/alpha"),
    ("del", "m", 2),
    ("text", "d"),
    ("set", "m", 1, "crates/beta"),
    ("print", "m"),
    ("raw", "m"),
    ("get", "e", "d", "workspace", "exclude"),
    ("push", "e", "crates/old"),
    ("insert", "e", 0, "crates/zero"),
    ("raw", "e"),
    ("del", "e", 0),
    ("del", "e", -1),
    ("raw", "e"),
    ("del", "e", 0),
    ("raw", "e"),
    ("push", "e", "only"),
    ("raw", "e"),
    ("del", "e", 3))

job("netlify redirects",
    ("parse", "d", "netlify"),
    ("get", "r", "d", "redirects"),
    ("push", "r", {"from": "/old", "to": "/new", "status": 302}),
    ("set", "d", "build", "environment", "HUGO_VERSION", "0.126.0"),
    ("set", "d", "build", "processing", {"skip_processing": True}),
    ("text", "d"))

job("service settings",
    ("parse", "d", "service"),
    ("set", "d", "log_level", "debug"),
    ("set", "d", "region", "eu-west-1"),
    ("set", "d", "server", "port", 9443),
    ("del", "d", "cache"),
    ("set", "d", "database", "pool_size", 40),
    ("set", "d", "database", "replica", {"url": "postgres://replica", "pool_size": 5}),
    ("get", "u", "d", "upstreams"),
    ("del", "u", 0),
    ("text", "d"),
    ("show", "d"))

job("service replace kinds",
    ("parse", "d", "service"),
    ("set", "d", "server", "plain"),
    ("set", "d", "log_format", {"style": "json", "color": False}),
    ("text", "d"),
    ("keys", "d"),
    ("set", "d", "upstreams", "none"),
    ("text", "d"),
    ("keys", "d"))

job("hugo menus",
    ("parse", "d", "hugo"),
    ("get", "mm", "d", "menu", "main"),
    ("push", "mm", {"name": "About", "url": "/about/", "weight": 3}),
    ("set", "d", "params", "social", "rss", True),
    ("set", "d", "languages", "de", {"languageName": "Deutsch", "weight": 3}),
    ("text", "d"),
    ("print", "d", "languages", "fr", "languageName"))

job("alacritty colors",
    ("parse", "d", "alacritty"),
    ("set", "d", "colors", "normal", "blue", "#81a2be"),
    ("set", "d", "window", "opacity", 1.0),
    ("set", "d", "window", "dimensions", "lines", 40),
    ("set", "d", "font", "bold", "style", "Heavy"),
    ("get", "b", "d", "keyboard", "bindings"),
    ("push", "b", {"key": "Q", "mods": "Command", "action": "Quit"}),
    ("text", "d"))

job("crlf document",
    ("parse", "d", "crlf"),
    ("set", "d", "server", "port", 443),
    ("set", "d", "server", "tls", "enabled", True),
    ("set", "d", "server", "name", "edge"),
    ("text", "d"))

job("strings changed",
    ("parse", "d", "strings"),
    ("set", "d", "str1", "plain now"),
    ("set", "d", "str2", "line one\nline two"),
    ("set", "d", "winpath", "D:\\data"),
    ("raw", "d", "winpath"),
    ("raw", "d", "str2"),
    ("set", "d", "emoji", C("string", "it's \"fine\"", literal=False)),
    ("raw", "d", "emoji"))

job("comments and indent",
    ("parse", "d", "service"),
    ("get", "port", "d", "server", "port"),
    ("comment", "port", "TLS"),
    ("get", "pool", "d", "database", "pool_size"),
    ("comment", "pool", "# per worker"),
    ("indent", "pool", 4),
    ("get", "srv", "d", "server"),
    ("indent", "srv", 2),
    ("text", "d"))

# --- building documents ---------------------------------------------------

job("new document",
    ("let", "d", C("document")),
    ("add", "d", C("comment", "generated by deploy-tool")),
    ("add", "d", C("nl")),
    ("add", "d", "title", "release"),
    ("let", "t", C("table")),
    ("add", "t", "host", "example.org"),
    ("add", "t", "port", 443),
    ("append", "t", None, C("comment", "ports below 1024 need root")),
    ("add", "d", "server", V("t")),
    ("let", "a", C("aot")),
    ("push", "a", C("item", {"name": "web", "replicas": 3})),
    ("push", "a", C("item", {"name": "worker", "replicas": 1})),
    ("append", "d", "service", V("a")),
    ("let", "s", C("table", True)),
    ("let", "inner", C("table")),
    ("update", "inner", {"x": 1}),
    ("append", "s", "inner", V("inner")),
    ("append", "d", "outer", V("s")),
    ("add", "d", "late", True),
    ("text", "d"),
    ("show", "d"))

job("document errors",
    ("let", "d", C("document")),
    ("add", "d", "x", 1),
    ("add", "d", "x", 2),
    ("add", "d", 5),
    ("append", "d", K(["a", "b"]), {"t": 1}),
    ("del", "d", "zzz"),
    ("pop", "d", "x"),
    ("pop", "d", "x"),
    ("text", "d"))

job("setdefault and pop",
    ("parse", "d", "service"),
    ("setdefault", "d", "version", 2),
    ("setdefault", "d", "owner", "team-orders"),
    ("setdefault", "d", "limits", {"rps": 500}),
    ("pop", "d", "log_format"),
    ("get", "s", "d", "server"),
    ("pop", "s", "workers"),
    ("text", "d"))

job("dumps of plain data",
    ("dumps", {"title": "x", "owner": {"name": "y", "dob": DT("1979-05-27T07:32:00-08:00")},
               "ports": [8000, 8001], "flags": {"a": True}, "z": 1}, False),
    ("dumps", {"title": "x", "owner": {"name": "y", "dob": DT("1979-05-27T07:32:00-08:00")},
               "ports": [8000, 8001], "flags": {"a": True}, "z": 1}, True),
    ("dumps", {"servers": [{"name": "a", "ip": "10.0.0.1"}, {"name": "b"}],
               "mixed": [1, {"x": 2}], "points": [{"x": 1, "y": {"z": 2}}]}, False),
    ("dumps", {"b": 2, "a": {"d": 1, "c": [{"y": 1, "x": 2}]}, "aa": 0}, True),
    ("dumps", {"when": DATE("2024-05-01"), "at": TIME("09:30:00.5"),
               "utc": DT("2024-05-01T09:30:00Z"), "local": DT("2024-05-01T09:30:00"),
               "f": 1.5, "e": 1e-7, "big": 1e300, "inf": F("inf"), "ninf": F("-inf"),
               "nan": F("nan"), "neg0": F("-0.0")}, False),
    ("dumps", {"s": "tab\there \"q\" back\\slash\u0001 \u00e9", "k y": 1,
               "": 2, "dotted.key": 3, "é": 4}, False),
    ("dumps", {"empty": {}, "nested": {"empty": {}}, "list": [], "e2": [[]]}, False))

job("item conversions",
    ("let", "a", C("item", [1, 2, 3])),
    ("raw", "a"),
    ("let", "b", C("item", [{"x": 1}, {"x": 2}])),
    ("raw", "b"),
    ("let", "c", C("item", {"t": {"u": 1}, "v": 2})),
    ("raw", "c"),
    ("let", "e", C("item", [[1, 2], {"k": "v"}, "s"])),
    ("raw", "e"),
    ("let", "f", C("item", F("nan"))),
    ("raw", "f"),
    ("let", "g", C("item", DT("2024-01-02T03:04:05.000600+05:30"))),
    ("raw", "g"),
    ("print", "g"),
    ("let", "h", C("item", TIME("23:59:59"))),
    ("raw", "h"),
    ("let", "i", C("item", True)),
    ("raw", "i"),
    ("let", "j", C("item", -12)),
    ("raw", "j"),
    ("let", "k", C("item", 3.0)),
    ("raw", "k"),
    ("let", "l", C("item", 12345678.9)),
    ("raw", "l"))

job("string constructors",
    ("let", "a", C("string", "plain")),
    ("raw", "a"),
    ("let", "a", C("string", "C:\\temp", literal=True)),
    ("raw", "a"),
    ("let", "a", C("string", "one\ntwo\n", multiline=True)),
    ("raw", "a"),
    ("let", "a", C("string", "has \"\"\" inside \\ and \t tab\r\nnext", multiline=True)),
    ("raw", "a"),
    ("print", "a"),
    ("let", "a", C("string", "lit\nlines", literal=True, multiline=True)),
    ("raw", "a"),
    ("let", "a", C("string", "it's", literal=True)),
    ("let", "a", C("string", "x'''y", literal=True, multiline=True)),
    ("let", "a", C("string", "bell\u0007", literal=True)),
    ("let", "a", C("string", "raw \\n kept", escape=False)),
    ("raw", "a"),
    ("let", "a", C("string", "\u0000\u001f\u007f\u0080 é")),
    ("raw", "a"),
    ("let", "a", C("string", "\"\"\"\"", multiline=True)),
    ("raw", "a"))

job("scalar constructors",
    ("let", "a", C("integer", "42")),
    ("raw", "a"),
    ("let", "a", C("integer", -7)),
    ("raw", "a"),
    ("let", "a", C("float_", "2.50")),
    ("raw", "a"),
    ("let", "a", C("boolean", "true")),
    ("raw", "a"),
    ("let", "a", C("boolean", "True")),
    ("raw", "a"),
    ("let", "a", C("date", "2024-07-04")),
    ("raw", "a"),
    ("let", "a", C("date", "2024-07-04T00:00:00")),
    ("let", "a", C("time", "12:30:45.123")),
    ("raw", "a"),
    ("print", "a"),
    ("let", "a", C("datetime", "2024-07-04 12:30:45+02:00")),
    ("raw", "a"),
    ("print", "a"),
    ("let", "a", C("datetime", "2024-07-04")),
    ("let", "a", C("date", "July 4")),
    ("let", "a", C("array")),
    ("raw", "a"),
    ("let", "a", C("array", "[1, 2,   3]")),
    ("raw", "a"),
    ("let", "a", C("key", "simple")),
    ("let", "a", C("key", "needs quoting")),
    ("let", "w", C("ws", "  \t")),
    ("raw", "w"),
    ("let", "c", C("comment", "hello")),
    ("raw", "c"))

job("value and key_value",
    ("value", "1"),
    ("value", "0x1F"),
    ("value", "true"),
    ("value", "\"s\\u00e9\""),
    ("value", "[1, [2, 3], {a = 1}]"),
    ("value", "{ a = 1, b.c = 2 }"),
    ("value", "1979-05-27"),
    ("value", "1979-05-27 07:32:00"),
    ("value", "07:32:00"),
    ("value", "nan"),
    ("value", "-inf"),
    ("value", "1 2"),
    ("value", "\"unterminated"),
    ("value", ""),
    ("kv", "a = 1"),
    ("kv", "  \"quoted key\"   =   'v'"),
    ("kv", "a.b.c = [1]"),
    ("kv", "x=1 # c"),
    ("kv", "a b = 1"),
    ("kv", "a = "))

job("arrays by hand",
    ("let", "a", C("array")),
    ("push", "a", 1),
    ("push", "a", 2),
    ("raw", "a"),
    ("multiline", "a", True),
    ("raw", "a"),
    ("insert", "a", 0, 0),
    ("raw", "a"),
    ("let", "b", C("array")),
    ("add_line", "b", [1, 2, 3]),
    ("add_line", "b", [4, 5, 6], {"comment": "second row"}),
    ("add_line", "b", [], {"indent": ""}),
    ("raw", "b"),
    ("print", "b"),
    ("let", "c", C("array", "[\n    \"a\",\n    \"b\",\n]")),
    ("push", "c", "c"),
    ("insert", "c", 1, "a2"),
    ("raw", "c"),
    ("del", "c", 0),
    ("raw", "c"),
    ("set", "c", -1, "last"),
    ("raw", "c"),
    ("insert", "c", 99, "end"),
    ("raw", "c"),
    ("insert", "c", -99, "start"),
    ("raw", "c"),
    ("clear", "c"),
    ("raw", "c"),
    ("push", "c", 1),
    ("raw", "c"),
    ("let", "e", C("array", "[1, 2] ")),
    ("let", "e", C("array", "[ # c\n  1, # one\n  2\n]")),
    ("push", "e", 3),
    ("raw", "e"),
    ("del", "e", 0),
    ("raw", "e"),
    ("set", "e", 5, 1),
    ("add_line", "e", [C("comment", "no")]))

job("inline tables",
    ("parses", "d", "point = { x = 1, y = 2 }\nempty = {}\n"),
    ("get", "p", "d", "point"),
    ("set", "p", "z", 3),
    ("del", "p", "x"),
    ("raw", "p"),
    ("get", "e", "d", "empty"),
    ("set", "e", "a", 1),
    ("set", "e", "b", {"c": 2}),
    ("raw", "e"),
    ("let", "n", C("inline_table")),
    ("append", "n", "k", "v"),
    ("append", "n", "j", C("integer", "5")),
    ("raw", "n"),
    ("let", "i", C("integer", "7")),
    ("comment", "i", "dropped"),
    ("set", "n", "i", V("i")),
    ("raw", "n"),
    ("set", "d", "point", V("n")),
    ("text", "d"))

job("tables by hand",
    ("let", "d", C("document")),
    ("let", "t", C("table")),
    ("add", "t", "a", 1),
    ("add", "t", C("nl")),
    ("add", "t", "b", 2),
    ("append", "d", "t", V("t")),
    ("let", "u", C("table")),
    ("add", "u", "c", 3),
    ("append", "d", "u", V("u")),
    ("add", "d", "after", "x"),
    ("text", "d"),
    ("body", "d"),
    ("let", "d2", C("document")),
    ("add", "d2", "k", 1),
    ("append", "d2", "t", {"x": {"y": {"z": 1}}}),
    ("text", "d2"),
    ("super", "d2", "t"),
    ("super", "d2", "t", "x"))

# --- files ----------------------------------------------------------------

job("files keep line endings",
    ("fread", "d", "crlf"),
    ("set", "d", "server", "port", 8443),
    ("fwrite", "d", "crlf.toml"),
    ("fread", "e", "service"),
    ("set", "e", "version", 2),
    ("fwrite", "e", "service.toml"),
    ("fread", "m", "mixed"),
    ("set", "m", "b", 20),
    ("fwrite", "m", "mixed.toml"))

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
for name, src in DOCS.items():
    write(f"data/docs/{name}.toml", src)
write("data/docs/mixed.toml", "a = 1\r\nb = 2\nc = 3\r\n")
for name, src in REPO.items():
    write(f"data/repo/{name}", src)
for name, src in ETC.items():
    write(f"data/etc/{name}", src)
with open("data/jobs.jsonl", "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=True) + "\n")
print(len(jobs), "jobs")
