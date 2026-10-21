# Runs data/jobs.tsv through jsonpath-ng itself (the copy in
# jsonpath_ng/, with the ply/ it is built on) and prints what each job
# gives. Its output is expected.out.
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import jsonpath_ng  # noqa: E402
from jsonpath_ng import jsonpath as jp  # noqa: E402
from jsonpath_ng.parser import parse as base_parse  # noqa: E402
from jsonpath_ng.ext.parser import parse as ext_parse  # noqa: E402
from jsonpath_ng.ext import filter as ext_filter, arithmetic, iterable, string  # noqa: E402
from jsonpath_ng.bin import jsonpath as cli  # noqa: E402

DATA = os.path.join(HERE, "data")
os.chdir(DATA)


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


def op_name(f):
    return f.__name__


# The tree a parse gives, written the way the classes' own reprs write
# it; Union, Intersect, Where and WhereNot have no repr of their own, so
# they are written the same way as Child.
def show(n):
    if isinstance(n, list):
        return "[" + ", ".join(show(x) for x in n) + "]"
    if isinstance(n, tuple):
        return "(" + ", ".join(show(x) for x in n) + ")"
    if not isinstance(n, jp.JSONPath):
        return repr(n)
    name = type(n).__name__
    if isinstance(n, (jp.Child, jp.Descendants, jp.Union, jp.Intersect, jp.Where)):
        return "%s(%s, %s)" % (name, show(n.left), show(n.right))
    if isinstance(n, jp.Fields):
        return repr(n)
    if isinstance(n, jp.Index):
        return repr(n)
    if isinstance(n, jp.Slice):
        return repr(n)
    if isinstance(n, ext_filter.Filter):
        return "Filter(%s)" % show(n.expressions)
    if isinstance(n, ext_filter.Expression):
        if n.op is None:
            return "Expression(%s)" % show(n.target)
        return "Expression(%s %s %s)" % (show(n.target), n.op, show(n.value))
    if isinstance(n, arithmetic.Operation):
        return "Operation(%s %s %s)" % (show(n.left), op_name(n.op), show(n.right))
    if isinstance(n, iterable.SortedThis):
        return "SortedThis(%s)" % show(n.expressions)
    if isinstance(n, (string.Sub, string.Split, string.Str)):
        return repr(n)
    return repr(n)


# repr, except that the key update_or_create files a new list under is
# written LIST_KEY (Python would print the object's address).
def prepr(v):
    if v is jp.LIST_KEY:
        return "LIST_KEY"
    if isinstance(v, dict):
        return "{" + ", ".join("%s: %s" % (prepr(k), prepr(x)) for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + ", ".join(prepr(x) for x in v) + "]"
    return repr(v)


def failure(e):
    return "! %s: %s" % (type(e).__name__, e)


FUNCS = {
    "double": lambda old, data, field: old * 2,
    "upper": lambda old, data, field: old.upper(),
    "inc": lambda old, data, field: old + 1,
    "label": lambda old, data, field: "%s: %s" % (field, old),
}


def mark(old, data, field):
    old["bulk"] = True
    return old


FUNCS["mark"] = mark


def price_of(x):
    return x.get("price") if isinstance(x, dict) else x


TESTS = {
    "any": lambda x: True,
    "cheap": lambda x: price_of(x) < 10,
    "is_list": lambda x: isinstance(x, list),
    "unassigned": lambda x: x.get("assignee") is None,
    "is_none": lambda x: x is None,
    "big": lambda x: x > 150,
}


def load_doc(name):
    if name.startswith("{") or name.startswith("["):
        return json.loads(name)
    with open(os.path.join("docs", name + ".json")) as f:
        return json.load(f)


def show_matches(matches, out):
    if not matches:
        out.append("(none)")
    for m in matches:
        out.append("%s = %s" % (m.full_path, prepr(m.value)))


def run(cols, out):
    kind, which, expr = cols[0], cols[1], unescape(cols[2])
    doc = cols[3] if len(cols) > 3 else ""
    arg = cols[4] if len(cols) > 4 else ""
    parse = base_parse if which == "base" else ext_parse
    if kind == "cli":
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            cli.main("jsonpath.py", expr, *arg.split(" "))
        except Exception as e:
            sys.stdout = old
            out.extend(buf.getvalue().splitlines())
            out.append(failure(e))
            return
        sys.stdout = old
        out.extend(buf.getvalue().splitlines())
        return
    try:
        tree = parse(expr)
    except Exception as e:
        out.append(failure(e))
        return
    if kind == "parse":
        out.append("tree " + show(tree))
        return
    data = load_doc(doc)
    try:
        if kind == "find":
            show_matches(tree.find(data), out)
        elif kind == "update":
            out.append(prepr(tree.update(data, json.loads(arg))))
        elif kind == "updatefn":
            out.append(prepr(tree.update(data, FUNCS[arg])))
        elif kind == "create":
            out.append(prepr(tree.update_or_create(data, json.loads(arg))))
        elif kind == "findcreate":
            show_matches(tree.find_or_create(data), out)
            out.append("data " + prepr(data))
        elif kind == "filter":
            out.append(prepr(tree.filter(TESTS[arg], data)))
    except Exception as e:
        out.append(failure(e))


def main():
    out = []
    with open("jobs.tsv") as f:
        lines = f.read().split("\n")
    for line in lines:
        if line == "":
            continue
        cols = line.split("\t")
        if cols[0] == "==":
            out.append("== " + cols[1])
            continue
        out.append("-- " + " ".join(c for c in cols if c != ""))
        run(cols, out)
    sys.stdout.write("\n".join(out) + "\n")


main()
