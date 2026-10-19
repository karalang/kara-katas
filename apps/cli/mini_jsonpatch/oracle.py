# The reference run for mini_jsonpatch: the same jobs through the real
# jsonpatch 1.33 and jsonpointer 3.0.0 on Python 3.13. make_patch walks
# dict keys through Python sets, so the run pins PYTHONHASHSEED=0 to make
# the order of a diff's operations reproducible.
import json
import os
import sys

if os.environ.get("PYTHONHASHSEED") != "0":
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)

import jsonpatch
import jsonpointer

D = "data"
OUT = []


def say(s=""):
    OUT.append(s)


def load(path):
    with open(os.path.join(D, path), encoding="utf-8") as f:
        return json.load(f)


def err(e):
    return "%s: %s" % (type(e).__name__, e)


def opts(text):
    indent = None
    uni = False
    f = text.split()
    i = 0
    while i < len(f):
        if f[i] == "--indent":
            indent = int(f[i + 1])
            i += 1
        elif f[i] == "-u":
            uni = True
        i += 1
    return indent, uni


def dumps(v, indent=None, uni=False):
    return json.dumps(v, indent=indent, ensure_ascii=not uni)


def roundtrip(a, b, text):
    try:
        r = jsonpatch.apply_patch(a, json.loads(text))
    except Exception as e:
        return "roundtrip: error: " + err(e)
    if r != b:
        return "roundtrip: NOT equal: " + dumps(r)
    return "roundtrip: equal"


def suite(path):
    cases = load(path)
    say("== suite %s (%d cases)" % (path, len(cases)))
    for i, t in enumerate(cases):
        say("[%d] %s" % (i, t.get("comment", "-")))
        if t.get("disabled"):
            say("  disabled in the suite")
        try:
            r = jsonpatch.apply_patch(t["doc"], t["patch"])
            say("  result: " + dumps(r))
            ok = "expected" in t and r == t["expected"]
            if "error" not in t and "expected" not in t:
                ok = True
        except Exception as e:
            say("  error: " + err(e))
            ok = "error" in t
        say("  suite: " + ("pass" if ok else "differs"))


def run():
    with open(os.path.join(D, "jobs.txt"), encoding="utf-8") as f:
        jobs = [l.rstrip("\n").split("\t") for l in f if l.strip()]
    for j in jobs:
        kind = j[0]
        if kind == "suite":
            suite(j[1])
        elif kind == "jsonpatch":
            say("== jsonpatch %s %s %s" % (j[1], j[2], j[3]))
            indent, uni = opts(j[1])
            try:
                r = jsonpatch.apply_patch(load(j[2]), load(j[3]))
                say(dumps(r, indent, uni))
            except Exception as e:
                say("error: " + err(e))
        elif kind == "fromstring":
            say("== fromstring %s %s" % (j[1], j[2]))
            with open(os.path.join(D, j[2]), encoding="utf-8") as f:
                text = f.read()
            try:
                p = jsonpatch.JsonPatch.from_string(text)
                say("patch: " + p.to_string())
                say(dumps(p.apply(load(j[1]))))
            except Exception as e:
                say("error: " + err(e))
        elif kind == "jsondiff":
            say("== jsondiff %s %s %s" % (j[1], j[2], j[3]))
            indent, uni = opts(j[1])
            a, b = load(j[2]), load(j[3])
            p = jsonpatch.make_patch(a, b)
            if p.patch:
                say(dumps(p.patch, indent, uni))
                say("exit 1")
            else:
                say("exit 0")
            say(roundtrip(a, b, p.to_string()))
        elif kind == "history":
            say("== history %s" % j[1])
            n = int(j[2])
            revs = [load("%s/rev%d.json" % (j[1], i)) for i in range(1, n + 1)]
            texts = []
            total = {}
            for i in range(n - 1):
                p = jsonpatch.make_patch(revs[i], revs[i + 1])
                count = {}
                for op in p.patch:
                    count[op["op"]] = count.get(op["op"], 0) + 1
                    total[op["op"]] = total.get(op["op"], 0) + 1
                tally = ", ".join("%s %d" % (k, count[k]) for k in ["add", "remove", "replace", "move", "copy", "test"] if k in count)
                say("rev%d -> rev%d: %d ops (%s)" % (i + 1, i + 2, len(p.patch), tally))
                texts.append(p.to_string())
                say("  " + texts[-1])
            doc = revs[0]
            for t in texts:
                doc = jsonpatch.apply_patch(doc, json.loads(t))
            tally = ", ".join("%s %d" % (k, total[k]) for k in ["add", "remove", "replace", "move", "copy", "test"] if k in total)
            say("replayed %d patches onto rev1 (%s)" % (len(texts), tally))
            say("  equal to rev%d: %s" % (n, doc == revs[-1]))
        elif kind == "pairs":
            say("== pairs %s" % j[1])
            with open(os.path.join(D, j[1]), encoding="utf-8") as f:
                pairs = [json.loads(l) for l in f if l.strip()]
            for i, pr in enumerate(pairs):
                try:
                    p = jsonpatch.make_patch(pr["a"], pr["b"])
                except Exception as e:
                    say("[%d] make_patch: error: %s" % (i, err(e)))
                    continue
                t = p.to_string()
                say("[%d] %s" % (i, t))
                say("  " + roundtrip(pr["a"], pr["b"], t))
        elif kind == "jsonpointer":
            say("== jsonpointer %s %r %s" % (j[1], j[2], j[3]))
            indent, _ = opts(j[1])
            try:
                for name in j[3].split():
                    doc = load(name)
                    try:
                        r = jsonpointer.resolve_pointer(doc, j[2])
                        say(json.dumps(r, indent=indent))
                    except jsonpointer.JsonPointerException as e:
                        say("stderr: Could not resolve pointer: %s" % str(e))
            except Exception as e:
                say("error: " + err(e))
        elif kind == "set":
            say("== set %s %r %s" % (j[1], j[2], j[3]))
            try:
                r = jsonpointer.set_pointer(load(j[1]), j[2], json.loads(j[3]), inplace=False)
                say(dumps(r))
            except Exception as e:
                say("error: " + err(e))
        elif kind == "ptr":
            try:
                p = jsonpointer.JsonPointer(j[1])
                say("ptr %r: parts %r, path %r" % (j[1], p.parts, p.path))
            except Exception as e:
                say("ptr %r: error: %s" % (j[1], err(e)))
        elif kind == "contains":
            a, b = jsonpointer.JsonPointer(j[1]), jsonpointer.JsonPointer(j[2])
            say("%r contains %r: %s" % (j[1], j[2], b in a))
        elif kind == "join":
            try:
                say("%r joined with %r: %r" % (j[1], j[2], jsonpointer.JsonPointer(j[1]).join(j[2]).path))
            except Exception as e:
                say("%r joined with %r: error: %s" % (j[1], j[2], err(e)))
        elif kind == "from_parts":
            say("from_parts %s: %r" % (j[1], jsonpointer.JsonPointer.from_parts(json.loads(j[1])).path))


run()
sys.stdout.write("\n".join(OUT) + "\n")
