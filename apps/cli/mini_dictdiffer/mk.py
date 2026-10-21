# Writes data/: the jobs mini_dictdiffer runs (data/jobs.jsonl) and the
# files its three programs read. Run with `python3 mk.py`.
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

NAN = float("nan")
INF = float("inf")


def S(*xs):
    """A set, as the jobs write one."""
    return {"$set": list(xs)}


JOBS = []


def job(name, *steps):
    JOBS.append({"name": name, "steps": [list(s) for s in steps]})


def d(name, a, b, **opts):
    """A job that diffs a and b, then patches and reverts with the result."""
    job(name, ("val", "a", a), ("val", "b", b), ("diff", "d", "a", "b", opts),
        ("patch", "p", "d", "a"), ("eq", "p", "b"), ("swap", "s", "d"),
        ("revert", "r", "d", "b"), ("eq", "r", "a"))


# --- diff -------------------------------------------------------------
d("change a value", {"a": "b"}, {"a": "c"})
d("add a nested dict", {}, {"a": {"b": "c"}})
d("add a nested dict, path_limit empty", {}, {"a": {"b": "c"}}, path_limit=[])
d("add a nested dict, path_limit a", {}, {"a": {"b": "c"}}, path_limit=[["a"]])
d("add a nested dict, path_limit a.b", {}, {"a": {"b": "c"}}, path_limit=[["a", "b"]])
d("add to a list", {"fruits": []}, {"fruits": ["apple", "mango"]})
d("add to a list, expanded", {"fruits": []}, {"fruits": ["apple", "mango"]}, expand=True)
d("shrink a list", {"n": [1, 2, 3, 4]}, {"n": [1]})
d("shrink a list, expanded", {"n": [1, 2, 3, 4]}, {"n": [5]}, expand=True)
d("change inside a dict", {"a": {"x": 1}}, {"a": {"x": 2}})
d("no dot notation", {"a": {"x": 1}}, {"a": {"x": 2}}, dot_notation=False)
d("a key with a dot", {"a.b": {"c": 1}}, {"a.b": {"c": 2}})
d("list of dicts", {"items": [{"sku": "A1", "qty": 2}, {"sku": "B2", "qty": 1}]},
  {"items": [{"sku": "A1", "qty": 3}, {"sku": "B2", "qty": 1, "gift": True}]})
d("root lists", [1, 2, 3], [1, 5, 3, 7])
d("root list of dicts", [{"id": 1}], [{"id": 1}, {"id": 2, "tags": []}])
d("root scalars", 1, 2)
d("root scalars equal", "x", "x")
d("dict becomes a list", {"a": {"x": 1}}, {"a": [1]})
d("list becomes a string", {"a": [1]}, {"a": "1"})
d("int and float equal", {"n": 1, "m": 2.0}, {"n": 1.0, "m": 2})
d("bool and int equal", {"t": True, "f": False}, {"t": 1, "f": 0})
d("bool and int differ", {"t": True}, {"t": 2})
d("int and string differ", {"n": 1}, {"n": "1"})
d("none and zero", {"n": None}, {"n": 0})
d("none and none", {"n": None}, {"n": None})
d("strings are values", {"s": "abc"}, {"s": "abd"})
d("float noise hidden", {"x": 0.1 + 0.2}, {"x": 0.3})
d("float noise, no tolerance", {"x": 0.1 + 0.2}, {"x": 0.3}, tolerance=None)
d("relative tolerance", {"x": 100, "y": 100}, {"x": 100.5, "y": 102}, tolerance=0.01)
d("absolute tolerance", {"x": 1.0, "y": 0.0}, {"x": 1.4, "y": 0.6}, tolerance=None, absolute_tolerance=0.5)
d("both tolerances", {"x": 0.001}, {"x": 0.0015}, tolerance=0.1, absolute_tolerance=0.001)
d("nan equals nan", {"x": NAN, "y": [NAN]}, {"x": NAN, "y": [NAN]})
d("nan and a number", {"x": NAN, "y": 1.0}, {"x": 1.0, "y": NAN})
d("infinity", {"x": INF, "y": -INF, "z": INF}, {"x": INF, "y": INF, "z": 1e308})
d("big floats", {"x": 1e300}, {"x": 1.0000000000000002e300})
d("sets of ints", {"s": S(1, 2, 3)}, {"s": S(2, 3, 4)})
d("sets of strings", {"tags": S("db", "web")}, {"tags": S("web", "cache", "edge")})
d("set added whole", {}, {"s": S(1, 2)})
d("set added, path_limit empty", {}, {"s": S(1, 2), "l": [1, {"k": S(3)}]}, path_limit=[])
d("set grows only", {"s": S(1)}, {"s": S(1, 2)})
d("ignore a key", {"a": 1, "b": 2}, {"a": 3, "b": 4}, ignore=["a"])
d("ignore a dotted key", {"a": {"b": 1, "c": 2}}, {"a": {"b": 3, "c": 4}}, ignore=["a.b"])
d("ignore a key path list", {"a": {"b": 1, "c": 2}}, {"a": {"b": 3, "c": 4}}, ignore=[["a", "c"]])
d("ignore a whole subtree", {"a": {"b": 1}, "z": 1}, {"a": {"b": 2}, "z": 2}, ignore=["a"])
d("ignore an added key", {"a": 1}, {"a": 1, "secret": "x"}, ignore=["secret"])
d("ignore a removed key", {"a": 1, "old": 2}, {"a": 1}, ignore=["old"])
d("ignore a list index does nothing", [1, 2], [3, 4], ignore=[0])
d("ignore inside a list", {"l": [{"a": 1, "b": 1}]}, {"l": [{"a": 2, "b": 2}]}, ignore=[["l", 0, "a"]])
d("ignore a dotted key, no dot notation", {"a.b": 1, "a": {"b": 1}}, {"a.b": 2, "a": {"b": 2}},
  ignore=["a.b"], dot_notation=False)
d("ignore a key with a dot", {"a.b": 1, "a": {"b": 1}}, {"a.b": 2, "a": {"b": 2}}, ignore=[["a.b"]])
d("ignore as a set", {"a": 1, "b": 2}, {"a": 3, "b": 4}, ignore=S("b"))
d("node prefix", {"a": 1}, {"a": 2}, node=["root"])
d("node prefix with an index", {"a": 1}, {"a": 2, "b": 3}, node=["items", 0])
d("path_limit wildcard", {"a": {"x": {"y": 1}}, "b": {"x": {"y": 1}}},
  {"a": {"x": {"y": 2}}, "b": {"x": {"y": 2}}}, path_limit=[["*", "x"]])
d("path_limit stops recursion", {"a": {"b": {"c": 1, "d": 1}}}, {"a": {"b": {"c": 2, "d": 2}}},
  path_limit=[["a", "b"]])
d("path_limit with lists", {}, {"a": [1, [2, 3], {"b": []}]}, path_limit=[])
d("path_limit and expand", {"a": 1}, {"a": 1, "b": {"c": 1}, "d": 2}, path_limit=[], expand=True)
d("removals keep order", {"a": 1, "b": 2, "c": 3}, {"b": 2})
d("additions keep order", {"b": 2}, {"c": 3, "b": 2, "a": 1})
d("deep mix", {"svc": {"ports": [80, 443], "env": {"A": "1"}, "on": True}},
  {"svc": {"ports": [8080], "env": {"A": "1", "B": "2"}, "on": False}})
d("empty to empty", {}, {})
d("unicode", {"name": "café"}, {"name": "café ☃", "emoji": "\U0001f600"})
d("quotes in strings", {"q": "it's"}, {"q": 'say "hi"\n'})

# --- patch, swap, revert with hand-written patches --------------------
job("patch a list insert past the end",
    ("val", "x", {"servers": ["a", "b"]}),
    ("val", "d", [["add", "servers", [[5, "c"], [0, "z"]]]]),
    ("patch", "p", "d", "x"))
job("patch a negative insert",
    ("val", "x", {"l": [1, 2, 3]}),
    ("val", "d", [["add", "l", [[-1, 9], [-10, 0]]]]),
    ("patch", "p", "d", "x"))
job("patch a dotted path through a list",
    ("val", "x", {"items": [{"qty": 1}, {"qty": 2}]}),
    ("val", "d", [["change", "items.0.qty", [1, 5]], ["change", "items.-1.qty", [2, 7]]]),
    ("patch", "p", "d", "x"))
job("patch a list item by text index",
    ("val", "x", {"tags": ["a", "b", "c"]}),
    ("val", "d", [["change", "tags.01", ["b", "B"]], ["change", "tags.-1", ["c", "C"]],
                  ["change", "tags. 0", ["a", "A"]]]),
    ("patch", "p", "d", "x"))
job("patch a change on a missing key adds it",
    ("val", "x", {"a": 1}),
    ("val", "d", [["change", "b", [None, 2]], ["change", "c.d", [0, 1]]]),
    ("patch", "p", "d", "x"))
job("patch ignores the old value",
    ("val", "x", {"a": 1}),
    ("val", "d", [["change", "a", [99, 2]]]),
    ("patch", "p", "d", "x"))
job("patch a remove of a missing key",
    ("val", "x", {"a": 1}),
    ("val", "d", [["remove", "", [["a", 1], ["b", 2]]]]),
    ("patch", "p", "d", "x"))
job("patch an add under a missing key",
    ("val", "x", {"a": 1}),
    ("val", "d", [["add", "b.c", [["d", 1]]]]),
    ("patch", "p", "d", "x"))
job("patch a remove past a list's end",
    ("val", "x", {"l": [1]}),
    ("val", "d", [["remove", "l", [[3, 1]]]]),
    ("patch", "p", "d", "x"))
job("patch a change past a list's end",
    ("val", "x", {"l": [1]}),
    ("val", "d", [["change", "l.4", [1, 2]]]),
    ("patch", "p", "d", "x"))
job("patch a list index that is not a number",
    ("val", "x", {"l": [{"a": 1}]}),
    ("val", "d", [["change", "l.first.a", [1, 2]]]),
    ("patch", "p", "d", "x"))
job("patch an unknown action",
    ("val", "x", {"a": 1}),
    ("val", "d", [["move", "a", ["b"]]]),
    ("patch", "p", "d", "x"))
job("patch a short entry",
    ("val", "x", {"a": 1}),
    ("val", "d", [["change", "a"]]),
    ("patch", "p", "d", "x"))
job("patch a long entry",
    ("val", "x", {"a": 1}),
    ("val", "d", [["change", "a", [1, 2], "extra"]]),
    ("patch", "p", "d", "x"))
job("patch a change without two values",
    ("val", "x", {"a": 1}),
    ("val", "d", [["change", "a", [1, 2, 3]]]),
    ("patch", "p", "d", "x"))
job("patch into a string",
    ("val", "x", {"s": "abc"}),
    ("val", "d", [["add", "s", [["k", 1]]]]),
    ("patch", "p", "d", "x"))
job("patch into a number",
    ("val", "x", {"n": 5}),
    ("val", "d", [["change", "n.k", [1, 2]]]),
    ("patch", "p", "d", "x"))
job("patch at the root",
    ("val", "x", {"a": 1}),
    ("val", "d", [["add", "", [["b", 2]]], ["remove", "", [["a", 1]]], ["add", [], [["c", 3]]]]),
    ("patch", "p", "d", "x"))
job("patch with a path list",
    ("val", "x", {"a.b": {"c": [1, 2]}}),
    ("val", "d", [["change", ["a.b", "c", 1], [2, 3]], ["add", ["a.b", "c"], [[0, 0]]]]),
    ("patch", "p", "d", "x"))
job("patch keeps the original",
    ("val", "x", {"a": [1]}),
    ("val", "d", [["add", "a", [[1, 2]]]]),
    ("patch", "p", "d", "x"), ("show", "x"))
job("patch the same diff twice",
    ("val", "a", {"l": [1]}), ("val", "b", {"l": [1, 2]}),
    ("diff", "d", "a", "b", {}), ("patch", "p", "d", "a"), ("patch", "q", "d", "p"))
job("swap reverses additions",
    ("val", "d", [["add", "a.b.c", [["a", "b"], ["c", "d"]]], ["change", "x", ["old", "new"]],
                  ["remove", "", [["z", 1]]]]),
    ("swap", "s", "d"), ("swap", "t", "s"))
job("revert a list removal",
    ("val", "a", [1, 2, 3]), ("val", "b", [1]),
    ("diff", "d", "a", "b", {}), ("revert", "r", "d", "b"), ("eq", "r", "a"))
job("revert in the wrong order",
    ("val", "a", {"l": [1, 2, 3]}), ("val", "b", {"l": [9]}),
    ("diff", "d", "a", "b", {"expand": True}), ("revert", "r", "d", "b"), ("eq", "r", "a"))
job("revert onto something else",
    ("val", "a", {"a": 1}), ("val", "b", {"a": 2, "b": 3}), ("val", "c", {"x": 0}),
    ("diff", "d", "a", "b", {}), ("revert", "r", "d", "c"))

# --- dot_lookup -------------------------------------------------------
for src, lookup, parent in (
        ({"a": {"b": "hello"}}, "a.b", False),
        ({"a": {"b": "hello"}}, "a.b", True),
        ({"a": {"b": "hello"}}, "", False),
        ({"a": {"b": "hello"}}, [], False),
        ({"a": {"b": "hello"}}, None, False),
        ({"a": [{"b": 1}, {"b": 2}]}, "a.1.b", False),
        ({"a": [{"b": 1}, {"b": 2}]}, ["a", "-1"], False),
        ({"a": "xyz"}, ["a", 1], False),
        ({"a": "xyz"}, "a.1", False),
        ({"a": {"b": 1}}, "a.c", False),
        ({"a": [1]}, "a.3", False),
        ({"a": [1]}, "a.x", False),
        ({"a": 5}, "a.b", False),
        ({"a": None}, "a.b", False),
        ({"a": True}, "a.b", False),
        ({"a": {"1": "str key"}}, ["a", 1], False),
        ({"a": 1}, 5, False),
        ({"a": 1}, "a", True),
        ({"a.b": 1}, "a.b", False),
        ({"a.b": 1}, ["a.b"], False)):
    job(f"dot_lookup {json.dumps(lookup)}{' parent' if parent else ''} in {json.dumps(src)}",
        ("val", "x", src), ("val", "k", lookup), ("lookup", "x", "k", parent))

# --- merge ------------------------------------------------------------


def m(name, lca, first, second, actions=(), path_limits=(), picks=None, wildcard=False):
    job(name, ("val", "lca", lca), ("val", "first", first), ("val", "second", second),
        ("merge", "lca", "first", "second",
         {"actions": [list(a) for a in actions], "path_limits": [list(p) for p in path_limits],
          "picks": picks, "wildcard": wildcard}))


m("merge without conflicts", {}, {"foo": "bar"}, {"bar": "foo"})
m("merge the same change", {"a": 1}, {"a": 2}, {"a": 2})
m("merge a conflict, picked", {"a": 1}, {"a": 2}, {"a": 3}, picks=["s"])
m("merge a conflict, unpicked", {"a": 1}, {"a": 2}, {"a": 3})
m("merge a conflict, too many picks", {"a": 1}, {"a": 2}, {"a": 3}, picks=["s", "f"])
m("merge a conflict, an action takes first", {"a": 1, "b": 1}, {"a": 2, "b": 2}, {"a": 3, "b": 3},
  actions=[(["a"], "f"), (["b"], "s")])
m("merge a cascading action", {"a": {"b": {"c": 1}}}, {"a": {"b": {"c": 2}}}, {"a": {"b": {"c": 3}}},
  actions=[(["a"], "s")])
m("merge an action that declines", {"a": {"b": 1}}, {"a": {"b": 2}}, {"a": {"b": 3}},
  actions=[(["a", "b"], "decline"), (["a"], "f")])
m("merge an action that stops", {"a": {"b": 1}}, {"a": {"b": 2}}, {"a": {"b": 3}},
  actions=[(["a", "b"], "stop"), (["a"], "f")], picks=["f"])
m("merge remove against a change below", {"a": {"b": 1}, "z": 0}, {"z": 0}, {"a": {"b": 2}, "z": 0},
  picks=["f"])
m("merge a change below against a remove", {"a": {"b": 1}}, {"a": {"b": 2}}, {}, picks=["s"])
m("merge list additions", {"l": [1]}, {"l": [1, 2]}, {"l": [1, 3]}, picks=["f"])
m("merge list additions on both sides of a key", {"l": [1], "m": [1]}, {"l": [1, 2]}, {"m": [1, 3], "l": [1]})
m("merge wildcard actions", {"users": {"ann": {"role": "dev"}, "bob": {"role": "dev"}}, "theme": "light"},
  {"users": {"ann": {"role": "lead"}, "bob": {"role": "ops"}}, "theme": "dark"},
  {"users": {"ann": {"role": "admin"}, "bob": {"role": "qa"}}, "theme": "blue"},
  actions=[(["users", "*"], "s"), (["theme"], "f")], wildcard=True)
m("merge plus wildcard", {"p": {"x": 1, "y": {"z": 1}}}, {"p": {"x": 2, "y": {"z": 2}}},
  {"p": {"x": 3, "y": {"z": 3}}}, actions=[(["p", "+"], "f")], wildcard=True, picks=["s"])
m("merge star at the root", {"a": 1, "b": {"c": 1}}, {"a": 2, "b": {"c": 2}}, {"a": 3, "b": {"c": 3}},
  actions=[(["*"], "s")], wildcard=True)
m("merge with path limits", {"cfg": {"a": 1, "b": 1}}, {"cfg": {"a": 2, "b": 1}}, {"cfg": {"a": 1, "b": 2}},
  path_limits=[["cfg"]], picks=["s"])
m("merge additions of the same key", {}, {"k": {"a": 1}}, {"k": {"a": 1}})
m("merge additions that differ", {}, {"k": 1}, {"k": 2}, picks=["f"])
m("merge sets", {"s": S(1)}, {"s": S(1, 2)}, {"s": S(1, 3)}, picks=["f"])
m("merge many", {"a": 1, "b": 2, "c": [1, 2], "d": {"e": 1}},
  {"a": 10, "b": 2, "c": [1, 2, 3], "d": {"e": 1, "f": 2}},
  {"a": 1, "b": 20, "c": [1], "d": {}}, picks=["s", "f"])
m("merge identical removals", {"a": 1, "b": 2}, {"b": 2}, {"b": 2})

# --- programs' data ---------------------------------------------------
FILES = {}


def put(path, obj):
    FILES[path] = json.dumps(obj, indent=2) + "\n"


def svc(image, replicas, cpu, mem, env, ports, updated, by, **extra):
    s = {"kind": "Service",
         "metadata": {"labels": {"team": extra.pop("team", "platform"), "tier": extra.pop("tier", "backend")},
                      "updated_at": updated, "deployed_by": by},
         "spec": {"image": image, "replicas": replicas, "resources": {"cpu": cpu, "memory": mem},
                  "env": env, "ports": ports}}
    s["spec"].update(extra)
    return s


put("desired/api.json", svc("registry.example/api:1.14.2", 3, 0.5, "512Mi",
                            {"LOG_LEVEL": "info", "DB_POOL": 20, "FEATURE_X": False},
                            [{"name": "http", "port": 8080}, {"name": "metrics", "port": 9090}],
                            "2026-10-20T08:00:00Z", "ci", healthcheck={"path": "/healthz", "interval": 10}))
put("deployed/api.json", svc("registry.example/api:1.14.1", 2, 0.5000000000000001, "512Mi",
                             {"LOG_LEVEL": "debug", "DB_POOL": 20, "FEATURE_X": False, "HOTFIX": "1"},
                             [{"name": "http", "port": 8080}, {"name": "metrics", "port": 9091}],
                             "2026-10-19T23:41:07Z", "oncall", healthcheck={"path": "/healthz", "interval": 10}))
put("desired/worker.json", svc("registry.example/worker:2.3.0", 4, 1.0, "1Gi",
                               {"QUEUE": "jobs", "CONCURRENCY": 8},
                               [], "2026-10-20T08:00:00Z", "ci", tier="jobs"))
put("deployed/worker.json", svc("registry.example/worker:2.3.0", 4, 1, "1Gi",
                                {"QUEUE": "jobs", "CONCURRENCY": 8},
                                [], "2026-10-18T10:12:00Z", "ci", tier="jobs"))
put("desired/web.json", svc("registry.example/web:5.0.0", 2, 0.25, "256Mi",
                            {"API_URL": "http://api:8080"},
                            [{"name": "http", "port": 80}, {"name": "https", "port": 443}],
                            "2026-10-20T08:00:00Z", "ci", team="frontend", tier="edge",
                            autoscale={"min": 2, "max": 6, "target_cpu": 0.7}))
put("deployed/web.json", svc("registry.example/web:4.9.3", 2, 0.25, "256Mi",
                             {"API_URL": "http://api:8080", "LEGACY_COOKIES": True},
                             [{"name": "http", "port": 80}],
                             "2026-09-30T17:02:44Z", "ann", team="frontend", tier="edge"))
put("desired/search.json", svc("registry.example/search:0.9.0", 1, 2.0, "4Gi", {}, [{"name": "http", "port": 9200}],
                               "2026-10-20T08:00:00Z", "ci", tier="data"))
put("deployed/cron.json", svc("registry.example/cron:1.0.0", 1, 0.1, "64Mi", {"SCHEDULE": "*/5 * * * *"}, [],
                              "2025-01-02T03:04:05Z", "bob"))

BASE = {"version": 3, "theme": "light", "editor": {"font": "Fira Code", "size": 13, "tabs": 4, "wrap": False},
        "plugins": ["git", "lint"], "users": {"ann": {"role": "dev", "email": "ann@example.org"},
                                              "bob": {"role": "dev", "email": "bob@example.org"}},
        "telemetry": True}
OURS = json.loads(json.dumps(BASE))
OURS["editor"]["size"] = 14
OURS["editor"]["wrap"] = True
OURS["plugins"].append("format")
OURS["users"]["ann"]["role"] = "lead"
OURS["users"]["cid"] = {"role": "dev", "email": "cid@example.org"}
OURS["theme"] = "dark"
THEIRS = json.loads(json.dumps(BASE))
THEIRS["editor"]["size"] = 15
THEIRS["editor"]["tabs"] = 2
THEIRS["plugins"].append("test")
THEIRS["users"]["ann"]["role"] = "admin"
del THEIRS["users"]["bob"]
del THEIRS["telemetry"]
THEIRS["theme"] = "dark"
THEIRS["version"] = 4
put("merge/base.json", BASE)
put("merge/ours.json", OURS)
put("merge/theirs.json", THEIRS)
FILES["merge/policy.txt"] = ("# path (dotted, * and + as wildcards) and who wins: f ours, s theirs,\n"
                             "# ask to leave it for picks.txt\n"
                             "users.* s\n"
                             "version s\n"
                             "plugins ask\n"
                             "editor.size ask\n")
FILES["merge/picks.txt"] = "s\nf\n"

V = [{"name": "orders", "columns": [{"name": "id", "type": "int"}, {"name": "total", "type": "decimal"}],
      "indexes": [], "owner": "sales"}]
v2 = json.loads(json.dumps(V[0]))
v2["columns"].append({"name": "created", "type": "timestamp"})
v2["indexes"].append({"cols": ["created"], "unique": False})
V.append(v2)
v3 = json.loads(json.dumps(v2))
v3["columns"][1]["type"] = "numeric(12,2)"
v3["owner"] = "finance"
v3["comment"] = "customer orders"
V.append(v3)
v4 = json.loads(json.dumps(v3))
del v4["columns"][0]
v4["columns"].insert(0, {"name": "order_id", "type": "bigint"})
v4["indexes"][0]["unique"] = True
del v4["comment"]
V.append(v4)
v5 = json.loads(json.dumps(v4))
v5["columns"] = v5["columns"][:2]
v5["indexes"] = []
v5["partition"] = {"by": "range", "cols": ["created"]}
V.append(v5)
for i, v in enumerate(V):
    put(f"history/v{i + 1}.json", v)


shutil.rmtree("data", ignore_errors=True)
for p, text in FILES.items():
    os.makedirs(os.path.dirname(os.path.join("data", p)), exist_ok=True)
    with open(os.path.join("data", p), "w") as f:
        f.write(text)
with open("data/jobs.jsonl", "w") as f:
    for j in JOBS:
        f.write(json.dumps(j, ensure_ascii=True) + "\n")
print(f"{len(JOBS)} jobs, {len(FILES)} files")
