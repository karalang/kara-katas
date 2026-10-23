#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py) through the vendored TinyDB and prints
what each step gives. A step is a Python expression over TinyDB's API,
evaluated with eval() in an environment that persists until a "reset"
step; "let" binds names (or assigns one item), "do" evaluates for the
effect, "show" prints str() of the value, "cat" prints a file under data/
and an exception prints as "error <class>: <message>". The three programs
(an importer, a report runner and a batch updater) read the files mk.py
wrote and print the files they write after "  |".

Run: python3 -I -B oracle.py > expected.out"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
from tinydb import JSONStorage, Query, TinyDB, where  # noqa: E402
from tinydb.middlewares import CachingMiddleware  # noqa: E402
from tinydb.operations import add, decrement, delete, increment, set, subtract  # noqa: E402
from tinydb.storages import MemoryStorage  # noqa: E402
from tinydb.table import Document  # noqa: E402
from tinydb.utils import LRUCache, freeze  # noqa: E402

DATA = os.path.join(HERE, "data")
os.chdir(HERE)


# Functions the script passes to Query.test, Query.map and Table.update.
def starts_with(value, prefix):
    return value.startswith(prefix)


def is_none(value):
    return value is None


def is_even(value):
    return value % 2 == 0


def lower(value):
    return value.lower()


def words(value):
    return value.split(" ")


def longer_than(value, n):
    return len(value) > n


def boom(value):
    raise ValueError("boom: %s" % value)


def shout(doc):
    doc["name"] = doc["name"].upper()


def ids(docs):
    return [d.doc_id for d in docs]


class ReModule:
    IGNORECASE = re.IGNORECASE
    I = re.I


BASE = {
    "TinyDB": TinyDB,
    "Query": Query,
    "where": where,
    "JSONStorage": JSONStorage,
    "MemoryStorage": MemoryStorage,
    "CachingMiddleware": CachingMiddleware,
    "Document": Document,
    "LRUCache": LRUCache,
    "freeze": freeze,
    "add": add,
    "decrement": decrement,
    "delete": delete,
    "increment": increment,
    "set": set,
    "subtract": subtract,
    "re": ReModule,
    "starts_with": starts_with,
    "is_none": is_none,
    "is_even": is_even,
    "lower": lower,
    "words": words,
    "longer_than": longer_than,
    "boom": boom,
    "shout": shout,
    "ids": ids,
    "sorted": sorted,
    "len": len,
    "list": list,
    "hash": hash,
}


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8") as f:
        return f.read()


def cat(w, rel):
    lines = read(rel).split("\n")
    w("  %s (%d lines)\n" % (rel, len(lines)))
    for ln in lines:
        w("  | %s\n" % ln)


def write_back(w, rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    cat(w, rel)


def tsv(rel):
    rows = []
    for ln in read(rel).split("\n"):
        if ln and not ln.startswith("#"):
            rows.append(ln.split("\t"))
    return rows


# ------------------------------------------------------------ programs

def value_of(text):
    if text == "None":
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    if text == "[]":
        return []
    body = text[1:] if text.startswith("-") else text
    if body.isdigit():
        return int(text)
    if body.count(".") == 1 and body.replace(".", "").isdigit():
        return float(text)
    return text


def clause(text):
    field, op, rest = (text.split(" ", 2) + ["", ""])[:3]
    f = Query()[field]
    if op == "==":
        return f == value_of(rest)
    if op == "!=":
        return f != value_of(rest)
    if op == "<":
        return f < value_of(rest)
    if op == "<=":
        return f <= value_of(rest)
    if op == ">":
        return f > value_of(rest)
    if op == ">=":
        return f >= value_of(rest)
    if op == "~":
        return f.matches(rest)
    if op == "has":
        return f.any([rest])
    if op == "all":
        return f.all(rest.split("|"))
    if op == "in":
        return f.one_of(rest.split("|"))
    if op == "exists":
        return f.exists()
    raise ValueError("unknown operator %r" % op)


def parse_query(text):
    out = None
    for alt in text.split(" | "):
        q = None
        for c in alt.split(" & "):
            q = clause(c) if q is None else q & clause(c)
        out = q if out is None else out | q
    return out


def import_csv(w, rel, dbrel):
    lines = [ln for ln in read(rel).split("\n") if ln]
    header = lines[0].split(",")
    docs = []
    for ln in lines[1:]:
        rec = dict(zip(header, ln.split(",")))
        doc = {"name": rec["name"], "email": rec["email"] or None}
        if rec["age"]:
            doc["age"] = int(rec["age"])
        doc["city"] = rec["city"]
        doc["tags"] = rec["tags"].split(";") if rec["tags"] else []
        if rec["score"]:
            doc["score"] = float(rec["score"])
        doc["active"] = rec["active"] == "true"
        docs.append(Document(doc, doc_id=int(rec["id"])))
    db = TinyDB(os.path.join("data", dbrel), indent=2)
    db.truncate()
    got = db.insert_multiple(docs)
    w("  inserted %d documents: %s\n" % (len(got), got))
    db.close()
    cat(w, dbrel)


def report(w, rel, dbrel, outrel):
    db = TinyDB(os.path.join("data", dbrel), indent=2)
    out = []
    for name, text in tsv(rel):
        try:
            docs = db.search(parse_query(text))
            names = ", ".join(d["name"] for d in docs)
            out.append("%s: %d (%s)" % (name, db.count(parse_query(text)), names))
        except Exception as e:
            out.append("%s: error %s: %s" % (name, type(e).__name__, e))
    db.close()
    write_back(w, outrel, "\n".join(out) + "\n")


OPS = {
    "increment": lambda f, v: increment(f),
    "decrement": lambda f, v: decrement(f),
    "add": lambda f, v: add(f, v),
    "subtract": lambda f, v: subtract(f, v),
    "set": lambda f, v: set(f, v),
    "delete": lambda f, v: delete(f),
}


def apply(w, rel, dbrel):
    db = TinyDB(os.path.join("data", dbrel), indent=2)
    for op, field, value, cond in tsv(rel):
        try:
            fields = OPS[op](field, value_of(value))
            if cond == "-":
                got = db.update(fields)
            else:
                got = db.update(fields, parse_query(cond))
            w("  %s %s where %s -> %s\n" % (op, field, cond, got))
        except Exception as e:
            w("  %s %s where %s -> error %s: %s\n" % (op, field, cond, type(e).__name__, e))
    db.close()
    cat(w, dbrel)


# ------------------------------------------------------------ jobs

def fresh():
    shutil.rmtree(os.path.join(DATA, "db"), ignore_errors=True)
    os.makedirs(os.path.join(DATA, "db"))
    return dict(BASE)


def run(w):
    env = fresh()
    for ln in read("jobs.tsv").split("\n"):
        if not ln:
            continue
        kind, src = ln.split("\t", 1)
        if kind == "#":
            w("\n# %s\n" % src)
            continue
        if kind == "reset":
            env = fresh()
            continue
        w("> %s\n" % src)
        try:
            if kind == "let":
                lhs, expr = src.split(" = ", 1)
                val = eval(expr, {"__builtins__": {}}, env)
                if lhs.endswith("]"):
                    k = lhs.rindex("[")
                    target = eval(lhs[:k], {"__builtins__": {}}, env)
                    key = eval(lhs[k + 1:-1], {"__builtins__": {}}, env)
                    target[key] = val
                else:
                    names = [n.strip() for n in lhs.split(",")]
                    if len(names) == 1:
                        env[names[0]] = val
                    else:
                        for n, v in zip(names, list(val)):
                            env[n] = v
            elif kind == "do":
                eval(src, {"__builtins__": {}}, env)
            elif kind == "show":
                w("%s\n" % (eval(src, {"__builtins__": {}}, env),))
            elif kind == "cat":
                cat(w, src)
            elif kind == "program":
                args = src.split(" ")
                if args[0] == "import":
                    import_csv(w, args[1], args[2])
                elif args[0] == "report":
                    report(w, args[1], args[2], args[3])
                elif args[0] == "apply":
                    apply(w, args[1], args[2])
        except Exception as e:
            w("error %s: %s\n" % (type(e).__name__, e))


def main():
    out = []
    run(out.append)
    sys.stdout.write("".join(out))


main()
