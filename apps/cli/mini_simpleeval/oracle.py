# Runs data/ through simpleeval itself (the copy in simpleeval.py) and
# prints what each job and program gives. Its output is expected.out.
import json
import os
import re
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import simpleeval  # noqa: E402
from simpleeval import (  # noqa: E402
    DEFAULT_FUNCTIONS,
    EvalWithCompoundTypes,
    InvalidExpression,
    NameNotDefined,
    SimpleEval,
)

DATA = os.path.join(HERE, "data")


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8") as f:
        return f.read()


def load(rel):
    return json.loads(read(rel))


def unescape(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            out.append({"n": "\n", "t": "\t"}.get(n, n))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def tsv(rel):
    rows = []
    for line in read(rel).split("\n"):
        if line:
            rows.append(line.split("\t"))
    return rows


# repr, without the addresses a function or a bound method shows
def no_addr(s):
    return re.sub(r" at 0x[0-9a-f]+", "", s)


def show(v):
    return no_addr(repr(v))


def failure(e):
    return "! %s: %s" % (type(e).__name__, no_addr(str(e)))


CTX_FUNCTIONS = dict(DEFAULT_FUNCTIONS, len=len, round=round, min=min, max=max, abs=abs)
CCTX_FUNCTIONS = dict(CTX_FUNCTIONS, sum=sum, sorted=sorted, any=any, all=all, range=range)


def evaluator(profile, doc):
    if profile == "basic":
        return SimpleEval()
    if profile == "compound":
        return EvalWithCompoundTypes()
    names = load("docs/%s.json" % doc)
    if profile == "ctx":
        return SimpleEval(names=names, functions=dict(CTX_FUNCTIONS))
    return EvalWithCompoundTypes(names=names, functions=dict(CCTX_FUNCTIONS))


def guarded(fn, out):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            r = ("=", fn())
        except Exception as e:  # noqa: BLE001
            r = ("!", e)
    for w in caught:
        out.append("warning: %s: %s" % (w.category.__name__, w.message))
    return r


def run_jobs():
    for row in tsv("jobs.tsv"):
        if row[0] == "==":
            print("== " + row[1])
            continue
        profile, expr, doc = row[0], unescape(row[1]), row[2]
        print("-- %s %s%s" % (profile, row[1], "" if doc == "-" else " @" + doc))
        out = []
        ev = evaluator(profile, doc)
        kind, v = guarded(lambda: ev.eval(expr), out)
        for line in out:
            print(line)
        print(show(v) if kind == "=" else failure(v))


def pricing():
    print("== pricing")
    rules = [(r[0], unescape(r[1])) for r in tsv("shop/pricing.tsv")]
    for order in load("shop/orders.json"):
        ev = EvalWithCompoundTypes(names=order, functions=dict(CCTX_FUNCTIONS))
        for name, expr in rules:
            out = []
            kind, v = guarded(lambda: ev.eval(expr), out)
            print("%s %s %s" % (order["id"], name, show(v) if kind == "=" else failure(v)))


def alerts():
    print("== alerts")
    rules = [(r[0], r[1], unescape(r[2])) for r in tsv("ops/alerts.tsv")]
    counts = {}
    for host in load("ops/hosts.json"):
        ev = EvalWithCompoundTypes(names=host, functions=dict(CCTX_FUNCTIONS))
        fired = []
        for name, sev, expr in rules:
            out = []
            kind, v = guarded(lambda: ev.eval(expr), out)
            if kind == "!":
                fired.append("  %s %s" % (name, failure(v)))
            elif v:
                fired.append("  FIRE %s %s %s" % (sev, name, show(v)))
                counts[sev] = counts.get(sev, 0) + 1
        print("%s: %d" % (host["host"], len(fired)))
        for line in fired:
            print(line)
    print("total: " + ", ".join("%s=%d" % (k, counts[k]) for k in sorted(counts)))


def notify():
    print("== notify")
    templates = [(r[0], unescape(r[1])) for r in tsv("mail/templates.tsv")]
    for user in load("mail/users.json"):
        ev = SimpleEval(names=user, functions=dict(DEFAULT_FUNCTIONS, len=len))
        print("To: " + user["email"])
        for name, expr in templates:
            out = []
            kind, v = guarded(lambda: ev.eval(expr), out)
            if kind == "!":
                print("  [%s] %s" % (name, failure(v)))
            elif v:
                print("  " + str(v))


def sheet():
    print("== sheet")
    rows = [(r[0], unescape(r[1])) for r in tsv("sheet.tsv")]
    cells = dict(rows)
    ev = SimpleEval(functions=dict(DEFAULT_FUNCTIONS, round=round))
    visiting = []

    def lookup(node):
        ref = node.id
        if ref not in cells:
            raise NameNotDefined(ref, ev.expr)
        if ref in visiting:
            raise InvalidExpression("circular reference: " + " -> ".join(visiting + [ref]))
        visiting.append(ref)
        try:
            return ev.eval(cells[ref])
        finally:
            visiting.pop()

    ev.names = lookup
    for ref, expr in rows:
        visiting[:] = [ref]
        out = []
        kind, v = guarded(lambda: ev.eval(expr), out)
        print("%s = %s" % (ref, show(v) if kind == "=" else failure(v)))


def main():
    run_jobs()
    pricing()
    alerts()
    notify()
    sheet()


if __name__ == "__main__":
    main()
