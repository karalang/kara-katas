# Runs jobs.tsv through pyhcl itself (the copy in hcl/, unchanged, with
# the PLY it bundles) and prints what mini_pyhcl prints.
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import hcl  # noqa: E402
from hcl.lexer import Lexer  # noqa: E402

DATA = os.path.join(HERE, "data")


def read(name):
    # hcltool opens the file in binary mode and pyhcl decodes it as UTF-8
    with open(os.path.join(DATA, name), "rb") as f:
        return f.read()


def fail(e):
    return "! %s: %s" % (type(e).__name__, e)


def pretty(obj):
    # what hcltool writes
    return json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))


def compact(obj):
    return json.dumps(obj, sort_keys=True)


def entries(v):
    # a block HCL repeated decodes to a list of dicts
    if isinstance(v, dict):
        return list(v.items())
    if isinstance(v, list):
        out = []
        for x in v:
            out.extend(entries(x))
        return out
    return []


def get(v, key, default=None):
    if isinstance(v, dict):
        return v.get(key, default)
    return default


def terraform(d):
    names = sorted(n for n in os.listdir(os.path.join(DATA, d)) if n.endswith(".tf") or n.endswith(".tf.json"))
    for name in names:
        print("  %s:" % name)
        try:
            cfg = hcl.loads(read(d + "/" + name))
        except Exception as e:
            print("    " + fail(e))
            continue
        if "terraform" in cfg:
            print("    terraform %s" % compact(cfg["terraform"]))
        for pname, body in entries(cfg.get("provider")):
            print("    provider %s %s" % (pname, compact(body)))
        for vname, body in entries(cfg.get("variable")):
            default = get(body, "default")
            line = "    variable %s default=%s" % (vname, "-" if default is None else compact(default))
            if get(body, "type") is not None:
                line += " type=%s" % get(body, "type")
            if get(body, "description") is not None:
                line += " (%s)" % get(body, "description")
            print(line)
        for section in ("data", "resource"):
            for rtype, named in entries(cfg.get(section)):
                for rname, body in entries(named):
                    keys = sorted(body.keys()) if isinstance(body, dict) else []
                    print("    %s %s.%s: %s" % (section, rtype, rname, ", ".join(keys)))
        for mname, body in entries(cfg.get("module")):
            print("    module %s source=%s version=%s" % (mname, get(body, "source"), get(body, "version", "-")))
        for oname, body in entries(cfg.get("output")):
            print("    output %s sensitive=%s value=%s" % (oname, get(body, "sensitive", False), compact(get(body, "value"))))


def vault(name, checks):
    policy = hcl.loads(read(name))
    rules = dict(entries(policy.get("path")))
    for check in checks:
        op, _, path = check.partition(":")
        rule = None
        if path in rules:
            rule = path
        else:
            for p in rules:
                if p.endswith("*") and path.startswith(p[:-1]):
                    if rule is None or len(p) > len(rule):
                        rule = p
        if rule is None:
            print("  %s %s: denied (no rule)" % (op, path))
            continue
        caps = get(rules[rule], "capabilities", [])
        verdict = "denied" if "deny" in caps or op not in caps else "allowed"
        print("  %s %s: %s by %s" % (op, path, verdict, json.dumps(rule)))


def nomad(name):
    spec = hcl.loads(read(name))
    for jname, job in entries(spec.get("job")):
        print("  job %s type=%s priority=%s datacenters=%s" % (
            jname, get(job, "type"), get(job, "priority"), ",".join(get(job, "datacenters", []))))
        total_cpu, total_mem = 0, 0
        for gname, group in entries(get(job, "group")):
            count = get(group, "count", 1)
            print("    group %s count=%d" % (gname, count))
            for tname, task in entries(get(group, "task")):
                res = get(task, "resources", {})
                cpu, mem = get(res, "cpu", 100), get(res, "memory", 300)
                total_cpu += cpu * count
                total_mem += mem * count
                print("      task %s driver=%s cpu=%d memory=%d config=%s" % (
                    tname, get(task, "driver"), cpu, mem, compact(get(task, "config"))))
                if get(task, "env") is not None:
                    print("        env %s" % compact(get(task, "env")))
        print("    total cpu=%d memory=%d" % (total_cpu, total_mem))


def consul(name):
    cfg = hcl.loads(read(name))
    for key in sorted(cfg):
        print("  %s: %s %s" % (key, type(cfg[key]).__name__, compact(cfg[key])))


def tokens(name, mode):
    lexer = Lexer(export_comments=mode)
    lexer.input(read(name).decode("utf-8"))
    while True:
        tok = lexer.token()
        if tok is None:
            break
        print("  %s %r line %d at %d" % (tok.type, tok.value, tok.lineno, tok.lexpos))


def run(job):
    kind = job[0]
    if kind == "load":
        mode = job[2] if len(job) > 2 else None
        obj = hcl.loads(read(job[1]), export_comments=mode)
        print(pretty(obj))
    elif kind == "tokens":
        tokens(job[1], job[2] if len(job) > 2 else None)
    elif kind == "terraform":
        terraform(job[1])
    elif kind == "vault":
        vault(job[1], job[2:])
    elif kind == "nomad":
        nomad(job[1])
    elif kind == "consul":
        consul(job[1])


with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
    jobs = [line.split("\t") for line in f.read().split("\n")[:-1]]
for job in jobs:
    print("-- " + " ".join(job))
    try:
        run(job)
    except Exception as e:
        print(fail(e))
