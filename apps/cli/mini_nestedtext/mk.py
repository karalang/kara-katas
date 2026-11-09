"""Writes data/ for mini_nestedtext: the settings files of a small web
shop's services written in NestedText, a list of how each one is loaded and
which of its keys to locate, and a file of single cases, each a document
and the options it is loaded with, that go through every line kind, the
inline forms, the duplicate-key policies and every error the loader raises.

`files/*.nt` are NestedText. `loads.jsonl` holds one
`[file, top, options, [[keys, kind], ...]]` array per line and `cases.jsonl`
one `[name, top, options, text]` array per line. The options are `on_dup`
(`error`, `ignore`, `replace` or `dedup`), `normalize` (lower-case the key
and turn spaces into underscores), `source` and `dialect`.

Run from this directory: python3 -s -P -B mk.py"""
import json
import os

FILES = {
    "deploy.nt": """\
# Deploy settings for the shop's API service.
service: shop-api
version: 2.14.0
owner: platform team
note: retries: 3, backoff: exponential
hosts:
    - api-1.internal.example
    - api-2.internal.example
    -
        name: api-canary.internal.example
        weight: 5
ports:
    [80, 443, 8443]
limits:
    {cpu: 500m, memory: 1Gi, burst: }
env:
    LOG_LEVEL: info
    DATABASE_URL: postgres://shop:not-a-real-password@db.internal.example/shop
    FEATURE_FLAGS: {new_checkout: on, beta_banner: off}
motd:
    > Welcome to shop-api.
    >
    > Maintenance window: Sundays 02:00\u201304:00 UTC.

health checks:
    : GET /healthz
    : (load balancer)
        interval: 10s
        timeout: 2s
    GET /ready: {interval: 30s}
""",
    "contacts.nt": """\
# Who to call about the shop.
Zo\u00eb M\u00fcller:
    role: on-call lead
    phone:
        mobile: +31 6 0000 0001
        desk: ext. 214
    address:
        > Keizersgracht 1
        > 1015 CJ Amsterdam
        > Netherlands
\u674e\u96f7:
    role: payments
    phone:
        mobile: +86 100 0000 0002
    languages: [zh, en]
    hours:
        [09:00-17:00 CST, \u5468\u4e00\u5230\u5468\u4e94]
Sam O\u2019Neil:
    role:
    phone:
        desk: ext. 101
    notes:
        > Prefers email.
        >   (Answers within a day.)
""",
    "matrix.nt": """\
# CI matrix: one entry per job.
-
    name: unit
    python:
        [3.11, 3.12, 3.13]
    os: ubuntu-latest

-
    name: integration
    services:
        - postgres:16
        - redis:7
    env:
        {DB: postgres, CACHE: redis}
    allow failure:
-
    name: docs
    run:
        > make html
        > make linkcheck
    tags: []
- lint
""",
    "notes.nt": """\
> Release 2.14.0
>
> - Checkout keeps the basket when the session expires.
>   Indented lines keep their spaces.
> - The canary takes 5% of traffic.
""",
    "settings.nt": """\
Log Level: debug
Max Connections: 20
Request Timeout: 15s
Cache:
    Time To Live: 300
    Backend: redis
""",
    "settings_dup.nt": """\
Log Level: debug
Max Connections: 20
log level: warn
""",
    "inventory.nt": """\
web:
    host: web-1.internal.example
    host: web-2.internal.example
    role: frontend
db:
    host: db-1.internal.example
    host: db-2.internal.example
    host: db-3.internal.example
""",
    "broken.nt": """\
service: shop-worker
queues:
    - orders
\t- refunds
""",
}

# [file, top, options, [[keys, kind], ...]]
LOADS = [
    ["deploy.nt", "dict", {}, [
        [["service"], "value"],
        [["note"], "value"],
        [["hosts", 2, "weight"], "key"],
        [["hosts", 2], "key"],
        [["hosts", 2], "value"],
        [["ports", 1], "value"],
        [["ports"], "value"],
        [["limits", "burst"], "value"],
        [["limits", "memory"], "key"],
        [["env", "FEATURE_FLAGS"], "value"],
        [["motd"], "value"],
        [["motd"], "key"],
        [["health checks", "GET /healthz\n(load balancer)"], "key"],
        [["health checks", "GET /healthz\n(load balancer)", "timeout"], "value"],
        [["health checks", "GET /ready", "interval"], "value"],
        [["hosts", 9], "value"],
        [[], "value"],
    ]],
    ["contacts.nt", "dict", {}, [
        [["Zo\u00eb M\u00fcller", "address"], "value"],
        [["\u674e\u96f7", "hours", 1], "value"],
        [["\u674e\u96f7", "languages"], "value"],
        [["Sam O\u2019Neil", "role"], "value"],
        [["Sam O\u2019Neil", "notes"], "value"],
    ]],
    ["matrix.nt", "list", {}, [
        [[0, "python", 2], "value"],
        [[1, "allow failure"], "value"],
        [[1, "env", "CACHE"], "key"],
        [[2, "run"], "value"],
        [[2, "tags"], "value"],
        [[3], "value"],
        [[3], "key"],
    ]],
    ["matrix.nt", "dict", {}, []],
    ["notes.nt", "str", {}, [[[], "value"]]],
    ["notes.nt", "any", {}, []],
    ["settings.nt", "dict", {"normalize": True}, [
        [["log_level"], "value"],
        [["cache", "time_to_live"], "value"],
        [["cache", "time_to_live"], "key"],
    ]],
    ["settings.nt", "dict", {}, [[["Log Level"], "value"]]],
    ["settings_dup.nt", "dict", {"normalize": True}, []],
    ["settings_dup.nt", "dict", {"normalize": True, "on_dup": "replace"}, [
        [["log_level"], "value"],
        [["log_level"], "key"],
    ]],
    ["inventory.nt", "dict", {}, []],
    ["inventory.nt", "dict", {"on_dup": "ignore"}, []],
    ["inventory.nt", "dict", {"on_dup": "replace"}, []],
    ["inventory.nt", "dict", {"on_dup": "dedup"}, [
        [["db", "host \u2014 #3"], "value"],
        [["db", "host \u2014 #4"], "key"],
    ]],
    ["broken.nt", "dict", {}, []],
    ["broken.nt", "dict", {"dialect": "i"}, []],
]

# [name, top, options, text]
CASES = [
    # Line kinds.
    ["flat dict", "dict", {}, "a: 1\nb: 2\n"],
    ["colon in value", "dict", {}, "url: http://shop.example:8080/a\n"],
    ["space before colon", "dict", {}, "key   :  v\n"],
    ["tab before colon", "dict", {}, "a\t: b\n"],
    ["no space after colon", "dict", {}, "a:b\n"],
    ["colon inside key", "dict", {}, "a:b: c\n"],
    ["tab after colon", "dict", {}, "a:\tb\n"],
    ["empty value", "dict", {}, "a:\nb: x\n"],
    ["value of one space", "dict", {}, "a: \nb:  \n"],
    ["trailing spaces kept", "dict", {}, "a: x  \n"],
    ["hash in value", "dict", {}, "a: # not a comment\n"],
    ["dash key", "dict", {}, "-a: b\n->: c\n>: d\n"],
    ["list items", "any", {}, "-\n- x\n-  y\n- a: b\n"],
    ["dash without space", "any", {}, "-x\n"],
    ["nested lists", "any", {}, "-\n  - a\n  - b\n- c\n"],
    ["string lines", "any", {}, "> a\n>\n>  b\n> \n"],
    ["string without space", "any", {}, ">a\n"],
    ["comments and blanks", "any", {}, "# c\n\n   # indented\n"],
    ["comment inside dict", "dict", {}, "a:\n    # note\n    - x\n\n    - y\n"],
    ["crlf", "dict", {}, "a: 1\r\nb: 2\r\n"],
    ["lone cr", "dict", {}, "a: 1\rb:\r  - x\r"],
    ["no final newline", "dict", {}, "a: 1\nb: 2"],
    ["byte order mark", "dict", {}, "\ufeffa: b\n"],
    ["unicode key", "dict", {}, "caf\u00e9: cr\u00e8me\n\u65e5\u672c: \u8a9e\n"],
    ["line separator in value", "dict", {}, "a: x\u2028y\n"],
    # Multi-line keys.
    ["multiline key", "dict", {}, ": a\n: b\n    > v\n"],
    ["multiline key with dict", "dict", {}, ": first\n:\n: third\n    x: 1\nnext: 2\n"],
    ["multiline key needs value", "dict", {}, ": k\nb: c\n"],
    ["multiline key at end", "dict", {}, "a: 1\n: k\n"],
    ["multiline key deeper part", "dict", {}, ": k\n  : j\n"],
    # Indentation.
    ["top level indented", "dict", {}, "  a: b\n"],
    ["indent after value", "dict", {}, "a: x\n  b: y\n"],
    ["indent after blank value", "dict", {}, "a:   \n    - x\n"],
    ["indent after list value", "any", {}, "- a\n  - b\n"],
    ["partial dedent", "dict", {}, "a:\n    b: 1\n  c: 2\n"],
    ["deeper string line", "any", {}, "> a\n  > b\n"],
    ["tab indent", "dict", {}, "a:\n\tb: c\n"],
    ["no-break space indent", "dict", {}, "a:\n\u00a0 b: c\n"],
    ["ideographic space indent", "dict", {}, "\u3000a: b\n"],
    ["vertical tab indent", "dict", {}, "a:\n  \x0bb: 1\n"],
    ["unrecognized line", "dict", {}, "a: b\njust words\n"],
    ["unrecognized after comment", "dict", {}, "a: b\n# c\nplain\n"],
    # Mixed containers and the top level.
    ["list then dict", "any", {}, "- a\nb: c\n"],
    ["dict then list", "any", {}, "a: b\n- c\n"],
    ["string then list", "any", {}, "> a\n- b\n"],
    ["inline then dict", "any", {}, "[a]\nb: c\n"],
    ["top dict given list", "dict", {}, "- a\n"],
    ["top list given dict", "list", {}, "a: b\n"],
    ["top str given dict", "str", {}, "a: b\n"],
    ["top dict given string", "dict", {}, "> a\n"],
    ["top any word", "any", {}, "x\n"],
    ["empty dict", "dict", {}, ""],
    ["empty list", "list", {}, "\n\n"],
    ["empty str", "str", {}, "# only a comment\n"],
    ["empty any", "any", {}, ""],
    ["top str", "str", {}, "> one\n> two\n"],
    ["top list inline", "list", {}, "[a, b]\n"],
    ["top dict inline", "dict", {}, "{a: b}\n"],
    ["top str inline", "str", {}, "[a]\n"],
    # Inline lists and dicts.
    ["inline empties", "any", {}, "-\n  []\n-\n  {}\n-\n  [ ]\n"],
    ["inline empty dict with space", "any", {}, "{ }\n"],
    ["inline list", "any", {}, "[a,b ,c ]\n"],
    ["inline list holes", "any", {}, "-\n  [a, , b]\n-\n  [a, b,]\n-\n  [,]\n"],
    ["inline list spaces in item", "any", {}, "[a b, c:d]\n"],
    ["inline value after empty", "any", {}, "-\n  [[] x]\n-\n  [{} {k: v}]\n"],
    ["inline extra character", "any", {}, "[a] b\n"],
    ["inline extra characters", "any", {}, "{a: 1}  ;;\n"],
    ["inline unclosed", "any", {}, "[a, [b, c]\n"],
    ["inline open brace", "any", {}, "{\n"],
    ["inline nested", "any", {}, "{a: 1, b: [x, y], c: {d: e}}\n"],
    ["inline dict trailing comma", "any", {}, "{a: 1,}\n"],
    ["inline dict trailing comma space", "any", {}, "{a: 1, }\n"],
    ["inline dict no colon", "any", {}, "{a 1}\n"],
    ["inline dict two colons", "any", {}, "{a: b: c}\n"],
    ["inline dict empty key", "any", {}, "{: v, k:}\n"],
    ["inline dict tight", "any", {}, "{a:b}\n"],
    ["inline dict list then junk", "any", {}, "{a: [b] c}\n"],
    ["inline list brace", "any", {}, "[a}\n"],
    ["inline list lone brace", "any", {}, "[}\n"],
    ["inline tab", "any", {}, "[a,\tb]\n"],
    ["inline tab error", "dict", {}, "k:\n  [a,\tb] x\n"],
    ["inline wide characters", "any", {}, "[\u65e5\u672c, \u8a9e] x\n"],
    ["inline in dict value", "dict", {}, "k:\n    [x, y]\nm: n\n"],
    ["inline then deeper", "dict", {}, "k:\n  [x]\n    - y\n"],
    ["inline-looking value", "dict", {}, "k: [a, b]\nm: {c: d}\n"],
    ["inline dialect off", "any", {"dialect": "i"}, "{a: b}\n"],
    ["inline dialect off list", "any", {"dialect": "i"}, "[a, b]\n"],
    # Duplicate keys.
    ["dup error", "dict", {}, "name1: value1\nname1: value2\nname3: value3\n"],
    ["dup error with source", "dict", {"source": "shop.nt"}, "a: 1\na: 2\n"],
    ["dup ignore", "dict", {"on_dup": "ignore"}, "key: v1\nkey: v2\nname: v4\nname: v5\n"],
    ["dup replace", "dict", {"on_dup": "replace"}, "key: v1\nother: x\nkey: v2\n"],
    ["dup dedup", "dict", {"on_dup": "dedup"}, "key: v1\nkey: v2\nkey: v3\nname: v4\nname: v5\n"],
    ["dup dedup collides", "dict", {"on_dup": "dedup"}, "k: 1\nk \u2014 #2: x\nk: 2\n"],
    ["dup ignore indented value", "dict", {"on_dup": "ignore"}, "a: 1\na:\n  - x\n"],
    ["dup nested", "dict", {}, "x:\n  a: 1\n  a: 2\n"],
    ["dup multiline key", "dict", {}, ": k\n    > 1\nk: 2\n"],
    ["dup two-line key", "dict", {}, ": a\n: b\n  > v\n: a\n: b\n  > w\n"],
    ["dup inline", "any", {}, "{a: 1, a: 2}\n"],
    ["dup inline indented", "dict", {}, "k:\n    {a: 1,  a: 2}\n"],
    ["dup inline replace", "any", {"on_dup": "replace"}, "{a: 1, b: 2, a: 3}\n"],
    ["dup inline ignore", "any", {"on_dup": "ignore"}, "{a: 1, b: 2, a: 3}\n"],
    ["dup inline dedup", "any", {"on_dup": "dedup"}, "{a: 1, a: 2}\n"],
    ["dup normalized", "dict", {"normalize": True}, "Log Level: debug\nlog level: warn\n"],
    ["dup normalized inline", "any", {"normalize": True}, "{Log Level: debug, LOG LEVEL: warn}\n"],
    ["dup unicode inline", "any", {}, "{caf\u00e9: 1, caf\u00e9: 2}\n"],
]


def put(name, text):
    path = os.path.join("data", name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def main():
    for name, text in FILES.items():
        put("files/" + name, text)
    put("loads.jsonl", "".join(json.dumps(x) + "\n" for x in LOADS))
    put("cases.jsonl", "".join(json.dumps(x) + "\n" for x in CASES))


main()
