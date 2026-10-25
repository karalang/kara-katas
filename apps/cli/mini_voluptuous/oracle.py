# Runs data/jobs.jsonl through voluptuous 0.15.2 (the package in
# voluptuous/, unchanged) and prints what mini_voluptuous prints. Run
# mk.py first, from this directory.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voluptuous as vol  # noqa: E402
from voluptuous import util, validators  # noqa: E402
from voluptuous.humanize import humanize_error  # noqa: E402

TYPES = {"int": int, "float": float, "str": str, "bool": bool, "dict": dict, "list": list,
         "object": object, "NoneType": type(None)}
EXTRA = {"prevent": vol.PREVENT_EXTRA, "allow": vol.ALLOW_EXTRA, "remove": vol.REMOVE_EXTRA}
CHECKS = {"boolean": validators.Boolean, "istrue": validators.IsTrue, "isfalse": validators.IsFalse,
          "email": validators.Email, "url": validators.Url, "fqdnurl": validators.FqdnUrl,
          "isfile": validators.IsFile, "isdir": validators.IsDir, "pathexists": validators.PathExists}
STRS = {"lower": util.Lower, "upper": util.Upper, "capitalize": util.Capitalize, "title": util.Title,
        "strip": util.Strip}


def key(k):
    if isinstance(k, str):
        return k
    op = k["op"]
    kw = {}
    if "msg" in k:
        kw["msg"] = k["msg"]
    if "default" in k:
        kw["default"] = k["default"]
    if op == "required":
        return vol.Required(k["name"], **kw)
    if op == "optional":
        return vol.Optional(k["name"], **kw)
    if op == "remove":
        return vol.Remove(k["name"])
    if op == "exclusive":
        return vol.Exclusive(k["name"], k["group"], **kw)
    if op == "inclusive":
        return vol.Inclusive(k["name"], k["group"], **kw)
    if op == "extra":
        return vol.Extra
    return build(k)


def build(n):
    if isinstance(n, list):
        return [build(x) for x in n]
    if not isinstance(n, dict):
        return n
    op = n["op"]
    msg = n.get("msg")
    if op == "type":
        return TYPES[n["name"]]
    if op == "lit":
        return n["value"]
    if op == "dict":
        return {key(k): build(v) for k, v in n["keys"]}
    if op == "list":
        return [build(x) for x in n["items"]]
    if op in ("any", "all"):
        cls = vol.Any if op == "any" else vol.All
        return cls(*[build(x) for x in n["of"]], msg=msg, required=n.get("required", False))
    if op == "someof":
        return vol.SomeOf([build(x) for x in n["of"]], min_valid=n.get("min"), max_valid=n.get("max"), msg=msg)
    if op == "maybe":
        return vol.Maybe(build(n["of"]), msg=msg)
    if op == "msg":
        return vol.Msg(build(n["of"]), n["text"])
    if op == "coerce":
        return vol.Coerce(TYPES[n["type"]], msg=msg)
    if op in CHECKS:
        return CHECKS[op](msg=msg)
    if op in STRS:
        return STRS[op]
    if op == "match":
        return vol.Match(n["pattern"], msg=msg)
    if op == "replace":
        return vol.Replace(n["pattern"], n["sub"], msg=msg)
    if op == "range":
        return vol.Range(min=n.get("min"), max=n.get("max"), min_included=n.get("min_included", True),
                         max_included=n.get("max_included", True), msg=msg)
    if op == "clamp":
        return vol.Clamp(min=n.get("min"), max=n.get("max"), msg=msg)
    if op == "length":
        return vol.Length(min=n.get("min"), max=n.get("max"), msg=msg)
    if op == "datetime":
        return vol.Datetime(format=n.get("format"), msg=msg)
    if op == "date":
        return vol.Date(format=n.get("format"), msg=msg)
    if op == "in":
        return vol.In(n["container"], msg=msg)
    if op == "notin":
        return vol.NotIn(n["container"], msg=msg)
    if op == "contains":
        return vol.Contains(n["item"], msg=msg)
    if op == "exactsequence":
        return vol.ExactSequence([build(x) for x in n["of"]], msg=msg)
    if op == "unordered":
        return vol.Unordered([build(x) for x in n["of"]], msg=msg)
    if op == "unique":
        return vol.Unique(msg=msg)
    if op == "equal":
        return vol.Equal(n["target"], msg=msg)
    if op == "number":
        return vol.Number(precision=n.get("precision"), scale=n.get("scale"), msg=msg)
    if op == "defaultto":
        return vol.DefaultTo(n["value"])
    if op == "setto":
        return vol.SetTo(n["value"])
    if op == "literal":
        return vol.Literal(n["value"])
    if op == "self":
        return vol.Self
    raise SystemExit(f"unknown op {op}")


def rs(v):
    # repr, with a dict's keys in sorted order
    if isinstance(v, dict):
        return "{" + ", ".join(f"{rs(k)}: {rs(v[k])}" for k in sorted(v)) + "}"
    if isinstance(v, list):
        return "[" + ", ".join(rs(x) for x in v) + "]"
    return repr(v)


def load(path):
    with open(os.path.join("data", path)) as f:
        return json.load(f)


schemas = {}
for s in load("schemas.json"):
    if "extend" in s:
        schemas[s["name"]] = schemas[s["extend"]].extend(
            build(s["with"]), required=s.get("required"),
            extra=EXTRA[s["extra"]] if "extra" in s else None)
    else:
        schemas[s["name"]] = vol.Schema(build(s["schema"]), required=s["required"], extra=EXTRA[s["extra"]])

n = 0


def run(label, sch, data):
    global n
    n += 1
    try:
        out = sch(data)
    except vol.MultipleInvalid as e:
        k = len(e.errors)
        print(f"job {n} {label}: {k} error{'' if k == 1 else 's'}")
        for line in humanize_error(data, e).split("\n"):
            print("  " + line)
        return
    print(f"job {n} {label}: valid")
    print("  " + rs(out))


with open("data/jobs.jsonl") as f:
    for line in f:
        job = json.loads(line)
        if "infer" in job:
            inferred = vol.Schema.infer(load(job["infer"]))
            n += 1
            print(f"job {n} infer {job['infer']}")
            print("  " + str(inferred))
            for c in job["check"]:
                run(f"inferred {c}", inferred, load(c))
        elif "file" in job:
            sch = schemas[job["schema"]]
            data = load(job["file"])
            if job.get("each"):
                for i, d in enumerate(data):
                    run(f"{job['schema']} {job['file']}[{i}]", sch, d)
            else:
                run(f"{job['schema']} {job['file']}", sch, data)
        else:
            run(f"{job['schema']}({rs(job['data'])})", schemas[job["schema"]], job["data"])
