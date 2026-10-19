# The reference run for mini_jmespath: the same jobs through the real
# jmespath 1.0.1 on Python 3.13. A `jp` job does what the `jp.py` script
# that ships with the library does: it prints the result as JSON with an
# indent of 4, or names the error on stderr and exits with 1.
import json
import os
import sys

import jmespath
from jmespath import exceptions

D = "data"
OUT = []


def say(s=""):
    OUT.append(s)


def load(path):
    with open(os.path.join(D, path), encoding="utf-8") as f:
        return json.load(f)


def q(s):
    return json.dumps(s, ensure_ascii=False)


def err(e):
    return "%s: %s" % (type(e).__name__, e)


KIND = {
    "ParseError": "syntax", "LexerError": "syntax", "IncompleteExpressionError": "syntax",
    "EmptyExpressionError": "syntax", "ArityError": "invalid-arity", "VariadictArityError": "invalid-arity",
    "JMESPathTypeError": "invalid-type", "UnknownFunctionError": "unknown-function", "ValueError": "invalid-value",
}


def suite(path):
    groups = load(path)
    say("== suite %s (%d cases)" % (path, sum(len(g["cases"]) for g in groups)))
    passed = 0
    total = 0
    for gi, g in enumerate(groups):
        for ci, c in enumerate(g["cases"]):
            total += 1
            say("[%d.%d] %s" % (gi, ci, q(c["expression"])))
            try:
                r = jmespath.search(c["expression"], g["given"])
                say("  result: " + json.dumps(r, ensure_ascii=False))
                ok = "error" not in c and r == c["result"]
            except Exception as e:
                say("  error: " + err(e))
                ok = KIND.get(type(e).__name__) == c.get("error")
            if ok:
                passed += 1
            else:
                say("  suite expects: " + ("error " + c["error"] if "error" in c else json.dumps(c["result"], ensure_ascii=False)))
    say("passed %d of %d" % (passed, total))


def jp(path, expr):
    say("== jp -f %s %s" % (path, q(expr)))
    data = load(path)
    try:
        say(json.dumps(jmespath.search(expr, data), indent=4, ensure_ascii=False))
        return
    except exceptions.ArityError as e:
        say("stderr: invalid-arity: %s" % e)
    except exceptions.JMESPathTypeError as e:
        say("stderr: invalid-type: %s" % e)
    except exceptions.UnknownFunctionError as e:
        say("stderr: unknown-function: %s" % e)
    except exceptions.ParseError as e:
        say("stderr: syntax-error: %s" % e)
    except Exception as e:
        say("stderr: uncaught " + err(e))
    say("exit 1")


def fuzz(path, exprs):
    data = load(path)
    with open(os.path.join(D, exprs), encoding="utf-8") as f:
        lines = [json.loads(l) for l in f if l.strip()]
    say("== fuzz %s %s (%d expressions)" % (path, exprs, len(lines)))
    tally = {}
    for i, e in enumerate(lines):
        say("[%d] %s" % (i, q(e)))
        try:
            r = jmespath.search(e, data)
            say("  -> " + json.dumps(r, ensure_ascii=False))
            k = "value"
        except Exception as x:
            say("  !! " + err(x))
            k = type(x).__name__
        tally[k] = tally.get(k, 0) + 1
    say("outcomes: " + ", ".join("%s %d" % (k, tally[k]) for k in sorted(tally)))


with open(os.path.join(D, "jobs.jsonl"), encoding="utf-8") as f:
    jobs = [json.loads(l) for l in f if l.strip()]
for j in jobs:
    if j[0] == "suite":
        suite(j[1])
    elif j[0] == "jp":
        jp(j[1], j[2])
    elif j[0] == "fuzz":
        fuzz(j[1], j[2])
sys.stdout.write("\n".join(OUT) + "\n")
