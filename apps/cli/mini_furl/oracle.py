"""Run data/jobs.jsonl against the vendored furl 2.1.4 and print what
mini_furl must print.

furl needs orderedmultidict and six, both vendored next to it.

Run: python3 -I -B oracle.py > expected.out
"""
import json
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
os.chdir(HERE)
warnings.simplefilter("ignore")

import furl as furl_pkg  # noqa: E402
from furl import furl  # noqa: E402

assert furl_pkg.__version__ == "2.1.4"


def flat(prefix, d):
    for k, v in d.items():
        if isinstance(v, dict):
            flat(prefix + k + ".", v)
        else:
            print("  %s%s: %r" % (prefix, k, v))


def get(f, name):
    if name == "url":
        return f.url
    if name in ("path", "query", "fragment"):
        return str(getattr(f, name))
    if name == "args":
        return f.args.allitems()
    obj = f
    for part in name.split("."):
        obj = getattr(obj, part)
    return obj


def show(name, thunk):
    try:
        v = thunk()
    except Exception as e:
        print("  %s: error %s: %s" % (name, type(e).__name__, e))
        return
    print("  %s: %r" % (name, v))


def apply(f, op):
    """Run one op on f. Returns the furl to carry on with."""
    name, a = op[0], op[1:]
    if name == "add":
        f.add(**a[0])
    elif name == "set":
        f.set(**a[0])
    elif name == "remove":
        f.remove(**a[0])
    elif name == "join":
        f.join(*a)
    elif name == "div":
        f = f / a[0]
    elif name == "load":
        f.load(a[0])
    elif name == "copy":
        f = f.copy()
    elif name == "attr":
        setattr(f, a[0], a[1])
    elif name == "path.add":
        f.path.add(a[0])
    elif name == "path.set":
        f.path.set(a[0])
    elif name == "path.remove":
        f.path.remove(a[0])
    elif name == "path.normalize":
        f.path.normalize()
    elif name == "path.isabsolute":
        f.path.isabsolute = a[0]
    elif name == "query.add":
        f.query.add(a[0])
    elif name == "query.set":
        f.query.set(a[0])
    elif name == "query.remove":
        f.query.remove(a[0])
    elif name == "query.load":
        f.query.load(a[0])
    elif name == "query.params":
        f.query.params = a[0]
    elif name == "args.set":
        f.args[a[0]] = a[1]
    elif name == "args.add":
        f.args.add(a[0], a[1])
    elif name == "args.del":
        del f.args[a[0]]
    elif name == "fragment.add":
        f.fragment.add(**a[0])
    elif name == "fragment.set":
        f.fragment.set(**a[0])
    elif name == "fragment.remove":
        f.fragment.remove(**a[0])
    elif name == "fragment.load":
        f.fragment.load(a[0])
    elif name == "fragment.path.add":
        f.fragment.path.add(a[0])
    elif name == "fragment.path.remove":
        f.fragment.path.remove(a[0])
    elif name == "fragment.path.isabsolute":
        f.fragment.path.isabsolute = a[0]
    elif name == "fragment.query.add":
        f.fragment.query.add(a[0])
    elif name == "fragment.query.remove":
        f.fragment.query.remove(a[0])
    else:
        raise SystemExit("unknown op " + name)
    return f


def run_job(job):
    spec, ops = job[0], job[1:]
    try:
        f = furl(spec) if isinstance(spec, str) else furl(**spec)
    except Exception as e:
        print("  new: error %s: %s" % (type(e).__name__, e))
        return
    show("new", lambda: f.url)
    for op in ops:
        name = op[0]
        if name == "tostr":
            show(name, lambda: f.tostr(**op[1]))
            continue
        if name == "query.encode":
            show(name, lambda: f.query.encode(**op[1]))
            continue
        if name == "args.get":
            show(name, lambda: f.args[op[1]])
            continue
        if name == "get":
            show(op[1], lambda: get(f, op[1]))
            continue
        if name == "dict":
            try:
                d = f.asdict()
            except Exception as e:
                print("  dict: error %s: %s" % (type(e).__name__, e))
                continue
            flat("", d)
            continue
        try:
            f = apply(f, op)
        except Exception as e:
            print("  %s: error %s: %s" % (name, type(e).__name__, e))
            continue
        show(name, lambda: f.url)


def lines_of(path):
    with open(path, encoding="utf-8") as fh:
        return [ln for ln in fh.read().split("\n") if ln and ln[0] != "#"]


def canon(path):
    """A crawler's link canonicalizer: drop tracking parameters and the
    fragment, resolve dot segments, then count the distinct pages."""
    seen = []
    for link in lines_of(path):
        try:
            f = furl(link)
            for key in list(f.args.keys()):
                if key.startswith("utm_") or key in ("fbclid", "gclid"):
                    del f.args[key]
            f.remove(fragment=True)
            f.path.normalize()
            url = f.url
        except Exception as e:
            print("  %s: error %s: %s" % (link, type(e).__name__, e))
            continue
        new = url not in seen
        if new:
            seen.append(url)
        print("  %s %s" % ("+" if new else "=", url))
    print("  %d links, %d pages" % (len(lines_of(path)), len(seen)))


def redirects(path):
    """Follow each recorded chain of Location headers from its start."""
    for line in lines_of(path):
        hops = line.split("\t")
        f = furl(hops[0])
        print("  start %s" % f.url)
        for loc in hops[1:]:
            try:
                f.join(loc)
                print("  -> %s" % f.url)
            except Exception as e:
                print("  -> %s: error %s: %s" % (loc, type(e).__name__, e))
                break
        print("  host %s, port %s, origin %s" % (f.host, f.port, f.origin))


def api(path):
    """Build an API client's request URLs from a base, a resource path and
    the parameters of each call."""
    for line in lines_of(path):
        base, resource, params = line.split("\t")
        f = furl(base)
        f.path.add(resource)
        f.args.update(json.loads(params))
        page = f.copy()
        page.args["page"] = 2
        print("  %s" % f.tostr(query_dont_quote="/,"))
        print("  %s" % page.tostr(query_delimiter=";"))


PROGRAMS = {"canon": canon, "redirects": redirects, "api": api}


def main():
    with open(os.path.join("data", "jobs.jsonl"), encoding="utf-8") as fh:
        jobs = fh.read().split("\n")
    for job in jobs:
        if not job:
            continue
        if job.startswith("#"):
            print(job)
            continue
        print("> " + job)
        if job.startswith("!"):
            prog, arg = job[1:].split(" ", 1)
            PROGRAMS[prog](arg)
            continue
        run_job(json.loads(job))


main()
