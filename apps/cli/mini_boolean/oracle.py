#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py) through the vendored boolean.py and
prints what each step gives: expressions as repr() and str() show them, an
exception as "error <class>: <message>". The three programs (a licence
checker, an access-rule matrix and a truth-table checker) write their
reports under data/out/ and print each file back after "  |".

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import boolean  # noqa: E402
from boolean.boolean import (  # noqa: E402
    OR,
    TOKEN_AND,
    TOKEN_LPAR,
    TOKEN_NOT,
    TOKEN_OR,
    TOKEN_RPAR,
    Symbol,
)

DATA = os.path.join(HERE, "data")
algebra = boolean.BooleanAlgebra()


def unesc(t):
    out = []
    k = 0
    while k < len(t):
        c = t[k]
        if c == "\\" and k + 1 < len(t):
            n = t[k + 1]
            out.append({"\\": "\\", "t": "\t", "n": "\n", "r": "\r"}.get(n, "\\" + n))
            k += 2
        else:
            out.append(c)
            k += 1
    return "".join(out)


def show(w, e):
    w("  -> %r\n" % (e,))
    w("  str: %s\n" % (e,))


def truth(e, attrs):
    """Evaluate e with each of its symbols true when it is in attrs."""
    kw = {name: name in attrs for name in sorted(e.objects)}
    return bool(e(**kw))


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8") as f:
        return f.read()


def write_back(w, rel, lines):
    os.makedirs(os.path.join(DATA, "out"), exist_ok=True)
    path = os.path.join(DATA, "out", rel)
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    back = read(os.path.join("out", rel))
    w("  wrote out/%s (%d lines)\n" % (rel, len(lines)))
    for line in back.split("\n")[:-1]:
        w("  | %s\n" % line)


def licence_tokens(text):
    """SPDX-style tokens for parse(): words split on blanks and brackets,
    AND / OR / NOT in any case, and "X WITH Y" joined into one symbol."""
    out = []
    k = 0
    while k < len(text):
        c = text[k]
        if c in " \t":
            k += 1
            continue
        if c in "()":
            out.append((TOKEN_LPAR if c == "(" else TOKEN_RPAR, c, k))
            k += 1
            continue
        s = k
        while k < len(text) and text[k] not in " \t()":
            k += 1
        word = text[s:k]
        up = word.upper()
        if up == "AND":
            out.append((TOKEN_AND, word, s))
        elif up == "OR":
            out.append((TOKEN_OR, word, s))
        elif up == "NOT":
            out.append((TOKEN_NOT, word, s))
        elif up == "WITH":
            if not out or not isinstance(out[-1][0], Symbol):
                raise ValueError("WITH at position %d does not follow a licence" % s)
            while k < len(text) and text[k] in " \t":
                k += 1
            e = k
            while k < len(text) and text[k] not in " \t()":
                k += 1
            if e == k:
                raise ValueError("WITH at position %d has no exception" % s)
            prev = out.pop()
            out.append((Symbol("%s WITH %s" % (prev[0].obj, text[e:k])), prev[1], prev[2]))
        else:
            out.append((Symbol(word), word, s))
    return out


def licences(w, pkgs, allowed_file):
    w("> licences %s %s\n" % (pkgs, allowed_file))
    allowed = set(read(allowed_file).split())
    lines = ["# licence check of %s against %s\n" % (pkgs, allowed_file)]
    ok = 0
    bad = 0
    for raw in read(pkgs).split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, _, text = line.partition(":")
        name = name.strip()
        text = text.strip()
        try:
            e = algebra.parse(licence_tokens(text))
            s = e.simplify()
            d = algebra.dnf(e)
        except Exception as ex:
            w("  %s: error %s: %s\n" % (name, type(ex).__name__, ex))
            lines.append("%s\tunreadable\t%s\n" % (name, text))
            bad += 1
            continue
        choices = d.args if isinstance(d, OR) else (d,)
        w("  %s: %s\n" % (name, e))
        w("    simplified: %s\n" % s)
        pick = None
        for c in choices:
            names = [str(x) for x in c.get_symbols()]
            fine = all(n in allowed for n in names)
            w("    choice %s -> %s\n" % (" + ".join(names), "allowed" if fine else "not allowed"))
            if fine and pick is None:
                pick = " + ".join(names)
        if pick is None:
            bad += 1
            lines.append("%s\tBLOCKED\t%s\n" % (name, s))
        else:
            ok += 1
            lines.append("%s\tok\t%s\n" % (name, pick))
    lines.append("# %d ok, %d blocked or unreadable\n" % (ok, bad))
    write_back(w, "licences.report", lines)


def access(w, rules_file, users_file):
    w("> access %s %s\n" % (rules_file, users_file))
    rules = []
    for raw in read(rules_file).split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, _, text = line.partition(":")
        name = name.strip()
        try:
            e = algebra.parse(text.strip())
        except Exception as ex:
            w("  %s: error %s: %s\n" % (name, type(ex).__name__, ex))
            continue
        s = e.simplify()
        w("  %s: %s\n" % (name, e))
        w("    simplified: %s\n" % s)
        w("    cnf: %s\n" % algebra.cnf(e))
        w("    dnf: %s\n" % algebra.dnf(e))
        if s == algebra.TRUE:
            w("    always granted\n")
        elif s == algebra.FALSE:
            w("    never granted\n")
        rules.append((name, s))
    users = []
    for raw in read(users_file).split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, _, attrs = line.partition(":")
        users.append((name.strip(), set(attrs.split())))
    lines = ["user\t" + "\t".join(n for n, _ in rules) + "\n"]
    for uname, attrs in users:
        row = [uname]
        for _, s in rules:
            try:
                row.append("Y" if truth(s, attrs) else "-")
            except Exception as ex:
                row.append("!" + type(ex).__name__)
        lines.append("\t".join(row) + "\n")
    write_back(w, "access.matrix", lines)


def truthtable(w, text):
    w("> truthtable %r\n" % text)
    e = algebra.parse(text)
    forms = [("expr", e), ("simplify", e.simplify()), ("cnf", algebra.cnf(e)),
             ("dnf", algebra.dnf(e))]
    for label, f in forms:
        w("  %s: %s\n" % (label, f))
    names = sorted(e.objects)
    w("  " + " ".join(names) + " | " + " ".join(lab for lab, _ in forms) + "\n")
    rows = 1 << len(names)
    agree = 0
    for r in range(rows):
        attrs = set(n for i, n in enumerate(names) if (r >> (len(names) - 1 - i)) & 1)
        cells = []
        vals = []
        for _, f in forms:
            try:
                v = truth(f, attrs)
                vals.append(v)
                cells.append("1" if v else "0")
            except Exception as ex:
                vals.append(None)
                cells.append(type(ex).__name__)
        bits = " ".join("1" if n in attrs else "0" for n in names)
        w("  " + bits + " | " + " ".join(cells) + "\n")
        if len(set(vals)) == 1:
            agree += 1
    w("  %d of %d rows agree\n" % (agree, rows))


def run(w, st, f):
    op = f[0]
    cur = st["cur"]
    if op == "parse":
        d = unesc(f[1])
        simp = len(f) > 2
        w("> parse(%r%s)\n" % (d, ", simplify=True" if simp else ""))
        st["cur"] = None
        st["cur"] = algebra.parse(d, simplify=simp)
        show(w, st["cur"])
        return
    if op == "tokens":
        d = unesc(f[1])
        w("> tokenize(%r)\n" % d)
        for t in algebra.tokenize(d):
            w("  - %r\n" % (t,))
        return
    if op == "keep":
        st["saved"][f[1]] = cur
        w("> keep as %s\n" % f[1])
        return
    if op == "use":
        st["cur"] = st["saved"][f[1]]
        w("> use %s\n" % f[1])
        show(w, st["cur"])
        return
    if op == "licences":
        licences(w, f[1], f[2])
        return
    if op == "access":
        access(w, f[1], f[2])
        return
    if op == "truthtable":
        truthtable(w, unesc(f[1]))
        return
    if op in ("simplify", "literalize", "flatten", "demorgan", "cancel", "distributive"):
        w("> %s()\n" % op)
    elif op in ("cnf", "dnf"):
        w("> algebra.%s(expr)\n" % op)
    elif op == "subtract":
        w("> subtract(%r, simplify=%s)\n" % (unesc(f[1]), len(f) > 2))
    elif op in ("and", "or", "eq", "lt"):
        w("> %s %s\n" % (op, f[1]))
    elif op == "in":
        w("> %r in expr\n" % unesc(f[1]))
    elif op == "eval":
        w("> expr(%s)\n" % f[1])
    elif op == "subs":
        w("> subs(%s%s%s)\n" % (f[1], ", default=" + f[2] if len(f) > 2 and f[2] != "-" else "",
                                ", simplify=True" if len(f) > 3 else ""))
    else:
        w("> %s\n" % op)
    if cur is None:
        w("  error: no expression\n")
        return
    if op in ("simplify", "literalize", "flatten", "demorgan", "cancel", "distributive"):
        st["cur"] = getattr(cur, op)()
        show(w, st["cur"])
    elif op == "cnf":
        st["cur"] = algebra.cnf(cur)
        show(w, st["cur"])
    elif op == "dnf":
        st["cur"] = algebra.dnf(cur)
        show(w, st["cur"])
    elif op == "subtract":
        r = cur.subtract(algebra.parse(unesc(f[1])), simplify=len(f) > 2)
        if r is None:
            w("  -> None\n")
        else:
            st["cur"] = r
            show(w, r)
    elif op == "and":
        st["cur"] = cur & st["saved"][f[1]]
        show(w, st["cur"])
    elif op == "or":
        st["cur"] = cur | st["saved"][f[1]]
        show(w, st["cur"])
    elif op == "invert":
        st["cur"] = ~cur
        show(w, st["cur"])
    elif op == "eq":
        o = st["saved"][f[1]]
        w("  -> == %r, != %r\n" % (cur == o, cur != o))
    elif op == "lt":
        o = st["saved"][f[1]]
        w("  -> < %r, > %r\n" % (cur < o, o < cur))
    elif op == "in":
        w("  -> %r\n" % (algebra.parse(unesc(f[1])) in cur))
    elif op == "str":
        w("  %s\n" % cur)
    elif op == "pretty":
        for line in cur.pretty().split("\n"):
            w("  | %s\n" % line)
    elif op == "debug":
        for line in cur.pretty(debug=True).split("\n"):
            w("  | %s\n" % line)
    elif op == "flags":
        w("  -> isliteral=%r iscanonical=%r\n" % (cur.isliteral, cur.iscanonical))
    elif op in ("literals", "symbols", "objects"):
        items = sorted(repr(x) for x in getattr(cur, op))
        if not items:
            w("  (none)\n")
        for x in items:
            w("  - %s\n" % x)
    elif op == "get_literals":
        w("  -> %r\n" % cur.get_literals())
    elif op == "get_symbols":
        w("  -> %r\n" % cur.get_symbols())
    elif op == "eval":
        kw = {}
        for part in f[1].split(","):
            if part:
                k, _, v = part.partition("=")
                kw[k] = v == "1"
        w("  -> %r\n" % (cur(**kw),))
    elif op == "subs":
        subs = {}
        for part in unesc(f[1]).split(";"):
            k, _, v = part.partition("=")
            subs[algebra.parse(k)] = algebra.parse(v)
        default = algebra.parse(f[2]) if len(f) > 2 and f[2] != "-" else None
        st["cur"] = cur.subs(subs, default=default, simplify=len(f) > 3)
        show(w, st["cur"])


def main():
    w = sys.stdout.write
    steps = read("jobs.tsv").split("\n")
    st = {"cur": None, "saved": {}}
    for line in steps:
        if not line:
            continue
        f = line.split("\t")
        if f[0] == "job":
            w("== %s\n" % f[1])
            continue
        try:
            run(w, st, f)
        except Exception as e:
            w("  error %s: %s\n" % (type(e).__name__, e))


main()
