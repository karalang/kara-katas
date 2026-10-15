# The oracle: loads each file with PyYAML 6.0.1 (yaml.safe_load_all) and
# prints each document as json.dumps(doc, indent=2), or PyYAML's error,
# then the deployment report. Run from this directory after mk.py.
import json, os, yaml
def dump(v):
    return json.dumps(v, indent=2, default=str)
files = ["deploy.yaml", "compose.yaml", "ci.yml", "site.yml", "edge.yaml", "multi.yaml",
         "tab.yaml", "quote.yaml", "indent.yaml", "alias.yaml", "flow.yaml", "dash.yaml"]
loaded = {}
for f in files:
    print(f"== {f}")
    try:
        with open("data/" + f) as fh:
            docs = list(yaml.safe_load_all(fh))
        loaded[f] = docs
        for i, d in enumerate(docs):
            print(f"--- document {i + 1}")
            print(dump(d))
    except yaml.YAMLError as e:
        print(f"error: {e}")
print("== report")
for d in loaded["deploy.yaml"]:
    kind = d["kind"]; name = d["metadata"]["name"]
    if kind == "Deployment":
        cs = d["spec"]["template"]["spec"]["containers"]
        print(f"deployment {name}: {d['spec']['replicas']} replicas, " + ", ".join(c["image"] for c in cs))
    elif kind == "Service":
        ps = d["spec"]["ports"]
        print(f"service {name}: " + ", ".join(f"{p['port']}->{p['targetPort']}" for p in ps))
    else:
        print(f"configmap {name}: " + ", ".join(f"{k} ({len(v)} bytes)" for k, v in d["data"].items()))
c = loaded["compose.yaml"][0]
for name, s in c["services"].items():
    ports = s.get("ports", [])
    shown = []
    for p in ports:
        if isinstance(p, str):
            shown.append(p)
        else:
            shown.append(f"{p} (read as a number, not host:container)")
    print(f"service {name}: restart={s.get('restart', 'no')}" + (", ports " + ", ".join(shown) if shown else ""))
wf = loaded["ci.yml"][0]
print("workflow triggers: " + ", ".join(repr(k) for k in wf.keys() if k not in ("name", "jobs")))
for jname, j in wf["jobs"].items():
    m = j["strategy"]["matrix"]
    print(f"job {jname}: {len(j['steps'])} steps, matrix python " + ", ".join(repr(x) for x in m["python"]))
for play in loaded["site.yml"][0]:
    for t in play["tasks"]:
        mods = [k for k in t if k not in ("name", "notify", "when")]
        args = t[mods[0]]
        mode = args.get("mode") if isinstance(args, dict) else None
        print(f"task {t['name']!r}: {mods[0]}" + (f", mode {mode!r}" if mode is not None else ""))
