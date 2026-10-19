# Writes data/ for mini_jsonpatch: the json-patch-tests suite (copied from
# suite/), Kubernetes-style manifests with kustomize-style RFC 6902 patch
# files, a deployment's revision history, config documents with awkward
# keys, and pairs of documents made by seeded random edits for diffing.
import copy
import json
import os
import random
import shutil

D = "data"


def w(path, text):
    p = os.path.join(D, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def wj(path, value, indent=2):
    w(path, json.dumps(value, indent=indent, ensure_ascii=False) + "\n")


if os.path.isdir(D):
    shutil.rmtree(D)
os.makedirs(os.path.join(D, "suite"))
for f in ["tests.json", "spec_tests.json"]:
    shutil.copy(os.path.join("suite", f), os.path.join(D, "suite", f))

deploy = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "checkout",
        "namespace": "shop",
        "labels": {"app": "checkout", "tier": "backend"},
        "annotations": {"deployment.kubernetes.io/revision": "7", "team~owner": "payments"},
    },
    "spec": {
        "replicas": 3,
        "selector": {"matchLabels": {"app": "checkout"}},
        "strategy": {"type": "RollingUpdate", "rollingUpdate": {"maxSurge": "25%", "maxUnavailable": 0}},
        "template": {
            "metadata": {"labels": {"app": "checkout", "tier": "backend"}},
            "spec": {
                "containers": [
                    {
                        "name": "app",
                        "image": "registry.example/checkout:2.4.1",
                        "args": ["--port=8080", "--log-level=info"],
                        "ports": [{"containerPort": 8080, "name": "http"}],
                        "env": [
                            {"name": "DB_HOST", "value": "db.shop.svc"},
                            {"name": "CACHE_TTL", "value": "30"},
                        ],
                        "resources": {"limits": {"cpu": "500m", "memory": "256Mi"}, "requests": {"cpu": 0.25, "memory": "128Mi"}},
                        "readinessProbe": {"httpGet": {"path": "/healthz", "port": 8080}, "periodSeconds": 10},
                    },
                    {"name": "sidecar", "image": "registry.example/envoy:1.29", "args": []},
                ],
                "tolerations": [],
                "nodeSelector": {"kubernetes.io/os": "linux"},
            },
        },
    },
}
wj("k8s/deployment.json", deploy)

service = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {"name": "checkout", "namespace": "shop"},
    "spec": {"selector": {"app": "checkout"}, "ports": [{"port": 80, "targetPort": "http"}], "type": "ClusterIP"},
}
wj("k8s/service.json", service)

P = {}
P["prod-overlay"] = [
    {"op": "replace", "path": "/spec/replicas", "value": 6},
    {"op": "add", "path": "/metadata/labels/env", "value": "prod"},
    {"op": "replace", "path": "/spec/template/spec/containers/0/image", "value": "registry.example/checkout:2.5.0"},
    {"op": "add", "path": "/spec/template/spec/containers/0/env/-", "value": {"name": "REGION", "value": "eu-west-1"}},
    {"op": "test", "path": "/spec/template/spec/containers/0/env/1/name", "value": "CACHE_TTL"},
    {"op": "replace", "path": "/spec/template/spec/containers/0/env/1/value", "value": "300"},
    {"op": "add", "path": "/spec/template/spec/tolerations/0", "value": {"key": "dedicated", "operator": "Equal", "value": "shop", "effect": "NoSchedule"}},
    {"op": "remove", "path": "/spec/template/spec/containers/1"},
    {"op": "add", "path": "/metadata/annotations/deployment.kubernetes.io~1revision", "value": "8"},
]
P["debug-overlay"] = [
    {"op": "copy", "from": "/spec/template/spec/containers/0", "path": "/spec/template/spec/containers/-"},
    {"op": "replace", "path": "/spec/template/spec/containers/2/name", "value": "debug"},
    {"op": "replace", "path": "/spec/template/spec/containers/2/args/1", "value": "--log-level=debug"},
    {"op": "remove", "path": "/spec/template/spec/containers/2/readinessProbe"},
    {"op": "move", "from": "/metadata/annotations/team~0owner", "path": "/metadata/labels/owner"},
    {"op": "add", "path": "/spec/template/spec/containers/0/args/0", "value": "--profile"},
]
P["bad-test"] = [
    {"op": "replace", "path": "/spec/replicas", "value": 2},
    {"op": "test", "path": "/spec/replicas", "value": 3},
]
P["bad-index"] = [{"op": "add", "path": "/spec/template/spec/containers/5", "value": {"name": "x"}}]
P["bad-leading-zero"] = [{"op": "remove", "path": "/spec/template/spec/containers/01"}]
P["bad-hex-index"] = [{"op": "remove", "path": "/spec/template/spec/containers/0x1"}]
P["bad-escape"] = [{"op": "add", "path": "/metadata/labels/a~2b", "value": "x"}]
P["bad-replace-dash"] = [{"op": "replace", "path": "/spec/template/spec/containers/-", "value": {}}]
P["bad-into-child"] = [{"op": "move", "from": "/metadata", "path": "/metadata/labels/meta"}]
P["noop-move"] = [{"op": "move", "from": "/spec/replicas", "path": "/spec/replicas"}]
P["into-string"] = [{"op": "add", "path": "/kind/0", "value": "x"}]
P["remove-in-string"] = [{"op": "remove", "path": "/kind/0"}]
P["test-string-char"] = [{"op": "test", "path": "/kind/0", "value": "D"}, {"op": "test", "path": "/kind/1", "value": "x"}]
P["test-end"] = [{"op": "test", "path": "/spec/template/spec/containers/0/args/-", "value": None}]
P["into-int"] = [{"op": "add", "path": "/spec/replicas/x", "value": 1}]
P["remove-dash"] = [{"op": "remove", "path": "/spec/template/spec/containers/-"}]
P["remove-root"] = [{"op": "remove", "path": ""}]
P["replace-root"] = [{"op": "replace", "path": "", "value": {"kind": "Empty"}}, {"op": "add", "path": "/note", "value": "rebuilt"}]
P["add-root-list"] = [{"op": "add", "path": "", "value": [1, 2]}, {"op": "add", "path": "", "value": [3]}]
P["move-missing"] = [{"op": "move", "from": "/spec/paused", "path": "/spec/suspended"}]
P["copy-missing-index"] = [{"op": "copy", "from": "/spec/template/spec/containers/9", "path": "/spec/x"}]
P["move-dash"] = [{"op": "move", "from": "/spec/template/spec/containers/-", "path": "/spec/x"}]
P["copy-then-edit"] = [
    {"op": "copy", "from": "/spec/selector", "path": "/spec/selectorCopy"},
    {"op": "add", "path": "/spec/selectorCopy/matchLabels/extra", "value": True},
    {"op": "test", "path": "/spec/selector/matchLabels", "value": {"app": "checkout"}},
]
P["test-numbers"] = [
    {"op": "test", "path": "/spec/replicas", "value": 3.0},
    {"op": "test", "path": "/spec/strategy/rollingUpdate/maxUnavailable", "value": False},
    {"op": "test", "path": "/spec/template/spec/containers/0/resources/requests/cpu", "value": 0.25},
    {"op": "test", "path": "/spec/template/spec/containers/0/ports/0", "value": {"name": "http", "containerPort": 8080.0}},
    {"op": "test", "path": "/spec/template/spec/containers/0/ports/0/containerPort", "value": "8080"},
]
P["test-bool-int"] = [{"op": "test", "path": "/spec/strategy/rollingUpdate/maxUnavailable", "value": True}]
P["not-a-list"] = {"op": "add", "path": "/x", "value": 1}
P["empty-object"] = {}
P["strings"] = ["add", "remove"]
P["op-not-string"] = [{"op": 7, "path": "/x"}]
P["path-not-string"] = [{"op": "add", "path": ["spec"], "value": 1}]
P["no-op-member"] = [{"path": "/x", "value": 1}]
P["unknown-op"] = [{"op": "merge", "path": "/x", "value": 1}]
P["late-error"] = [
    {"op": "add", "path": "/spec/paused", "value": True},
    {"op": "copy", "path": "/spec/x"},
]
P["patch-in-string"] = "[{\"op\": \"add\", \"path\": \"/spec/paused\", \"value\": false}]"
P["service-ports"] = [
    {"op": "add", "path": "/spec/ports/-", "value": {"port": 443, "targetPort": "https", "name": "https"}},
    {"op": "add", "path": "/spec/ports/0/name", "value": "http"},
    {"op": "replace", "path": "/spec/type", "value": "LoadBalancer"},
    {"op": "add", "path": "/metadata/annotations", "value": {"service.beta.kubernetes.io/aws-load-balancer-type": "nlb"}},
    {"op": "move", "from": "/spec/ports/1", "path": "/spec/ports/0"},
]
for name, p in P.items():
    wj("patches/" + name + ".json", p, indent=None)

# Patches read through JsonPatch.from_string, where a repeated member turns
# into a list of its values.
w("strpatch/dup-value.json", '[{"op": "add", "path": "/tags", "value": "a", "value": "b"}]\n')
w("strpatch/dup-path.json", '[{"op": "add", "path": "/a", "path": "/b", "value": 1}]\n')
w("strpatch/dup-in-value.json", '[{"op": "add", "path": "/limits", "value": {"cpu": 1, "cpu": 2, "mem": 3}}]\n')
w("strpatch/plain.json", '[{"op": "replace", "path": "/kind", "value": "StatefulSet"}]\n')

settings = {
    "http": {
        "errors": {"404": "/errors/not-found.html", "500": "/errors/oops.html", "1": "one"},
        "routes": ["/", "/cart", "/cart/checkout", "/api/v1/orders"],
    },
    "paths/with/slashes": {"a~b": 1, "~": 2, "": 3},
    "unicode": {"café": "crème brûlée", "naïve": ["日本", "😀"]},
    "flags": [True, False, None, 0, 1, 1.5, "1"],
    "matrix": [[1, 2], [3, 4], []],
}
wj("config/settings.json", settings)
wj("config/settings-scalar.json", 42)
wj("config/settings-list.json", ["a", "b", "c"])
wj("config/settings-text.json", "plain text")

# A deployment's revision history: each revision edits the last one.
revs = [copy.deepcopy(deploy)]
r = copy.deepcopy(deploy)
r["spec"]["replicas"] = 4
r["spec"]["template"]["spec"]["containers"][0]["image"] = "registry.example/checkout:2.4.2"
revs.append(r)
r = copy.deepcopy(r)
c = r["spec"]["template"]["spec"]["containers"]
c[0]["env"].insert(0, {"name": "FEATURE_X", "value": "on"})
c[0]["args"] = ["--log-level=info", "--port=8080"]
revs.append(r)
r = copy.deepcopy(r)
c = r["spec"]["template"]["spec"]["containers"]
c.reverse()
r["metadata"]["labels"]["tier"] = "core"
del r["metadata"]["annotations"]["team~owner"]
r["metadata"]["annotations"]["team/owner"] = "payments"
revs.append(r)
r = copy.deepcopy(r)
r["spec"]["template"]["spec"]["tolerations"] = [{"key": "spot", "operator": "Exists"}]
r["spec"]["template"]["spec"]["containers"][1]["resources"]["requests"]["cpu"] = "250m"
r["spec"]["strategy"] = {"type": "Recreate"}
revs.append(r)
r = copy.deepcopy(r)
r["spec"]["template"]["spec"]["containers"].pop(0)
r["spec"]["replicas"] = 4.0
revs.append(r)
for i, rv in enumerate(revs):
    wj("history/rev%d.json" % (i + 1), rv)

# Pairs made by seeded random edits.
rng = random.Random(6902)
WORDS = ["alpha", "beta", "gamma", "delta", "x", "y", "1", "2", "10", "a/b", "m~n", "", "zé"]


def rand_scalar():
    k = rng.randrange(8)
    if k == 0:
        return rng.randrange(-3, 12)
    if k == 1:
        return rng.choice([0.5, 1.0, 2.0, -0.0, 1e-7, 3.25])
    if k == 2:
        return rng.choice([True, False])
    if k == 3:
        return None
    return rng.choice(WORDS)


def rand_value(depth):
    k = rng.randrange(6)
    if depth <= 0 or k < 3:
        return rand_scalar()
    if k < 5:
        return [rand_value(depth - 1) for _ in range(rng.randrange(0, 6))]
    d = {}
    for _ in range(rng.randrange(0, 6)):
        d[rng.choice(WORDS)] = rand_value(depth - 1)
    return d


def mutate(v, depth):
    if isinstance(v, list):
        v = list(v)
        for _ in range(rng.randrange(1, 4)):
            k = rng.randrange(7)
            if k == 0 and v:
                v.pop(rng.randrange(len(v)))
            elif k == 1:
                v.insert(rng.randrange(len(v) + 1), rand_value(1) if rng.random() < 0.5 else (rng.choice(v) if v else 1))
            elif k == 2 and len(v) > 1:
                i, j = rng.randrange(len(v)), rng.randrange(len(v))
                v[i], v[j] = v[j], v[i]
            elif k == 3 and v:
                i = rng.randrange(len(v))
                v[i] = mutate(v[i], depth - 1) if depth > 0 else rand_scalar()
            elif k == 4:
                rng.shuffle(v)
            elif k == 5 and v:
                v.append(v[rng.randrange(len(v))])
            elif v:
                v.reverse()
        return v
    if isinstance(v, dict):
        items = list(v.items())
        for _ in range(rng.randrange(1, 4)):
            k = rng.randrange(5)
            if k == 0 and items:
                items.pop(rng.randrange(len(items)))
            elif k == 1:
                key = rng.choice(WORDS)
                items = [it for it in items if it[0] != key]
                items.insert(rng.randrange(len(items) + 1), (key, rand_value(1)))
            elif k == 2 and items:
                i = rng.randrange(len(items))
                key = rng.choice(WORDS)
                if all(it[0] != key for it in items):
                    items[i] = (key, items[i][1])
            elif k == 3 and items:
                i = rng.randrange(len(items))
                items[i] = (items[i][0], mutate(items[i][1], depth - 1) if depth > 0 else rand_scalar())
            else:
                rng.shuffle(items)
        return dict(items)
    if rng.random() < 0.5:
        return rand_scalar()
    return rand_value(2)


lines = []
for n in range(70):
    if n % 3 == 0:
        a = [rng.choice([1, 2, 3, "a", "b", True, None]) for _ in range(rng.randrange(0, 9))]
    elif n % 3 == 1:
        a = rand_value(3)
    else:
        a = {"items": [rand_value(1) for _ in range(rng.randrange(1, 7))], "meta": rand_value(2), "n": rng.randrange(5)}
    b = mutate(a, 3)
    if n % 7 == 3:
        b = mutate(b, 3)
    lines.append(json.dumps({"a": a, "b": b}, ensure_ascii=False))
w("gen/pairs.jsonl", "\n".join(lines) + "\n")

J = []


def job(*fields):
    J.append("\t".join(fields))


job("suite", "suite/tests.json")
job("suite", "suite/spec_tests.json")
for name in P:
    target = "k8s/service.json" if name == "service-ports" else "k8s/deployment.json"
    job("jsonpatch", "", target, "patches/" + name + ".json")
job("jsonpatch", "--indent 2", "k8s/deployment.json", "patches/prod-overlay.json")
job("jsonpatch", "--indent 4 -u", "config/settings.json", "patches/empty-object.json")
job("jsonpatch", "", "config/settings-list.json", "patches/add-root-list.json")
job("jsonpatch", "", "config/settings-text.json", "patches/remove-root.json")
job("jsonpatch", "", "config/settings-scalar.json", "patches/remove-root.json")
job("jsonpatch", "", "config/settings-list.json", "patches/remove-root.json")
job("jsonpatch", "", "config/settings-text.json", "patches/add-root-list.json")
for name in ["dup-value", "dup-path", "dup-in-value", "plain"]:
    job("fromstring", "k8s/service.json", "strpatch/" + name + ".json")
for i in range(1, len(revs)):
    job("jsondiff", "", "history/rev%d.json" % i, "history/rev%d.json" % (i + 1))
job("jsondiff", "--indent 2", "history/rev1.json", "history/rev6.json")
job("jsondiff", "", "history/rev6.json", "history/rev1.json")
job("jsondiff", "", "history/rev3.json", "history/rev3.json")
job("jsondiff", "-u", "config/settings.json", "config/settings-list.json")
job("jsondiff", "", "config/settings-list.json", "config/settings-scalar.json")
job("jsondiff", "", "config/settings-scalar.json", "config/settings-text.json")
job("history", "history", str(len(revs)))
job("pairs", "gen/pairs.jsonl")
for ptr in ["", "/", "/http/errors/404", "/http/routes/2", "/http/routes/-", "/http/routes/-/0", "/http/routes/4",
            "/paths~1with~1slashes/a~0b", "/paths~1with~1slashes/~0", "/paths~1with~1slashes/", "/unicode/café",
            "/unicode/naïve/1", "/flags/0", "/flags/01", "/flags/1 ", "/flags/0_1", "/flags/0x", "/flags/+1",
            "/matrix/1/0", "/matrix/2/0", "/matrix/0/1/x", "/http/routes/0/0", "/http/routes/0/9", "/http/nothing",
            "/http/errors/404/0/x", "flags", "/flags/~2", "/flags/~", "/http/errors/1"]:
    job("jsonpointer", "", ptr, "config/settings.json")
job("jsonpointer", "--indent 2", "/http", "config/settings.json k8s/service.json config/settings-list.json")
job("jsonpointer", "", "/0", "config/settings-list.json config/settings-text.json config/settings-scalar.json")
for ptr, val in [("/http/routes/-", '"/api/v2"'), ("/http/routes/0", '"/home"'), ("/http/newkey", '{"a": [1]}'),
                 ("", '"root"'), ("/matrix/2/0", "7"), ("/matrix/9", "null"), ("/http/errors/x/y", "1"), ("/flags/-", "[]")]:
    job("set", "config/settings.json", ptr, val)
for p in ["", "/", "/a/b~0c~1d", "/~01", "a", "/x~", "/x~3", "/0/-/~1~0", "//"]:
    job("ptr", p)
job("contains", "/a/b/c", "/a/b")
job("contains", "/a/b", "/a/b/c")
job("contains", "/a/b", "")
job("contains", "/a~1b", "/a")
job("join", "/a/b", "/c/d")
job("join", "/a", "x")
job("join", "", "/m~0n")
job("from_parts", '["a", "~", "/", 0, ""]')
job("from_parts", "[]")
job("from_parts", '[1, 2.5, true, null]')
w("jobs.txt", "\n".join(J) + "\n")
