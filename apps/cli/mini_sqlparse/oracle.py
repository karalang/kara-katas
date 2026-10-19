# The reference run: the jobs in data/jobs.jsonl through the real sqlparse
# 0.5.3 in sqlparse/ (the wheel, unchanged). Run as `python3 -I oracle.py`
# from this directory after mk.py; its output is expected.out.
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlparse  # noqa: E402
from sqlparse import sql as S  # noqa: E402
from sqlparse import tokens as T  # noqa: E402


def read(name):
    with open(os.path.join("data", name), encoding="utf-8", newline="") as fh:
        return fh.read()


def source(j):
    return read(j["file"]) if "file" in j else j["sql"]


def fail(e):
    print("  %s: %s" % (type(e).__name__, e))


def opts_text(o):
    return " ".join("%s=%r" % (k, v) for k, v in o.items())


def show_block(text):
    for line in text.split("\n"):
        print("  |" + line)


# ------------------------------------------------------------------- jobs

def run_tokens(j):
    for tt, v in sqlparse.lexer.tokenize(source(j)):
        print("  %r %r" % (tt, v))


def run_split(j):
    parts = sqlparse.split(source(j), strip_semicolon=j.get("strip_semicolon", False))
    for k, p in enumerate(parts):
        print("  [%d] %r" % (k, p))
    print("  %d statements" % len(parts))


def run_tree(j):
    depth = j.get("depth")
    for k, st in enumerate(sqlparse.parse(source(j))):
        print("  statement %d %s" % (k, st.get_type()))
        f = io.StringIO()
        st._pprint_tree(max_depth=depth, f=f)
        for line in f.getvalue().split("\n")[:-1]:
            print("    " + line)


def call(f):
    try:
        return repr(f())
    except Exception as e:
        return "%s(%s)" % (type(e).__name__, e)


def walk(tl, out):
    for t in tl.tokens:
        if t.is_group:
            out.append(t)
            walk(t, out)


def run_info(j):
    for k, st in enumerate(sqlparse.parse(source(j))):
        print("  statement %d %s %r" % (k, st.get_type(), str(st)[:60]))
        groups = []
        walk(st, groups)
        for g in groups:
            kind = type(g).__name__
            text = str(g)
            if kind == "Identifier":
                print("    Identifier %r name=%s real=%s alias=%s parent=%s cast=%s order=%s star=%s" % (
                    text, call(g.get_name), call(g.get_real_name), call(g.get_alias),
                    call(g.get_parent_name), call(g.get_typecast), call(g.get_ordering),
                    call(g.is_wildcard)))
            elif kind == "Function":
                print("    Function %r name=%s real=%s alias=%s params=%s window=%s" % (
                    text, call(g.get_name), call(g.get_real_name), call(g.get_alias),
                    call(lambda: [str(p) for p in g.get_parameters()]),
                    call(lambda: str(g.get_window()))))
            elif kind == "IdentifierList":
                print("    IdentifierList %s" % call(lambda: [str(x) for x in g.get_identifiers()]))
            elif kind == "Case":
                cases = g.get_cases()
                parts = []
                for cond, val in cases:
                    c = "None" if cond is None else repr("".join(str(x) for x in cond))
                    parts.append("%s->%r" % (c, "".join(str(x) for x in val)))
                print("    Case " + " ".join(parts))
            elif kind == "Comparison":
                print("    Comparison %r %r" % (str(g.left), str(g.right)))
            elif kind == "Comment":
                print("    Comment %r multiline=%r" % (text, bool(g.is_multiline())))
            else:
                print("    %s %r" % (kind, text))


def run_format(j):
    o = dict(j["opts"])
    try:
        out = sqlparse.format(source(j), **o)
    except Exception as e:
        fail(e)
        return
    show_block(out)


# ---------------------------------------------------------------- reports

TABLE_KW = ("FROM", "JOIN", "INTO", "UPDATE", "TABLE")


def is_table_kw(t):
    if not t.is_keyword:
        return False
    n = t.normalized
    return n in TABLE_KW or n.endswith(" JOIN")


def table_name(t):
    if isinstance(t, S.Identifier):
        real = t.get_real_name()
        parent = t.get_parent_name()
        if real is None:
            return None
        return parent + "." + real if parent else real
    if isinstance(t, S.Function):
        return t.get_real_name()
    if t.ttype in T.Name:
        return t.value
    return None


def tables_of(tl, out):
    want = False
    for t in tl.tokens:
        if t.is_whitespace or t.ttype in T.Comment or isinstance(t, S.Comment):
            continue
        if isinstance(t, S.Parenthesis) or isinstance(t, S.Where):
            tables_of(t, out)
        if want:
            if isinstance(t, S.IdentifierList):
                for x in t.get_identifiers():
                    n = table_name(x)
                    if n is not None and n not in out:
                        out.append(n)
            elif isinstance(t, S.Parenthesis):
                pass
            else:
                n = table_name(t)
                if n is not None and n not in out:
                    out.append(n)
            want = False
        if is_table_kw(t):
            want = True
        elif t.is_group and not isinstance(t, (S.Parenthesis, S.Where)):
            tables_of(t, out)
    return out


def flags_of(st):
    flags = []
    kind = st.get_type()
    first = st.token_first(skip_cm=True)
    if kind == "SELECT" or (first is not None and first.ttype == T.Keyword.CTE):
        for t in st.tokens:
            if t.ttype is T.Wildcard or (isinstance(t, S.Identifier) and t.is_wildcard()):
                flags.append("select-star")
                break
            if isinstance(t, S.IdentifierList) and any(
                    x.ttype is T.Wildcard or (isinstance(x, S.Identifier) and x.is_wildcard())
                    for x in t.get_identifiers()):
                flags.append("select-star")
                break
            if t.match(T.Keyword, "FROM"):
                break
    if kind in ("UPDATE", "DELETE"):
        if not any(isinstance(t, S.Where) for t in st.tokens):
            flags.append("no-where")
    if kind in ("CREATE", "ALTER", "DROP", "CREATE OR REPLACE"):
        flags.append("ddl")
    return flags


def run_lint(j):
    d = os.path.join("data", j["dir"])
    totals = {}
    nflags = 0
    for name in sorted(os.listdir(d)):
        if not name.endswith(".sql"):
            continue
        text = read(os.path.join(j["dir"], name))
        stmts = [s for s in sqlparse.parse(text) if s.token_first(skip_cm=True) is not None]
        print("  %s: %d statements" % (name, len(stmts)))
        for k, st in enumerate(stmts):
            kind = st.get_type()
            totals[kind] = totals.get(kind, 0) + 1
            tabs = tables_of(st, [])
            fl = flags_of(st)
            nflags += len(fl)
            line = str(st).strip().split("\n")[0]
            if len(line) > 50:
                line = line[:47] + "..."
            print("    %d %s tables=[%s]%s  %s" % (k + 1, kind, ", ".join(tabs),
                                                  "".join(" !" + f for f in fl), line))
    for kind in sorted(totals):
        print("  total %s %d" % (kind, totals[kind]))
    print("  flags %d" % nflags)


def ms(text):
    whole, _, frac = text.partition(".")
    frac = (frac + "000")[:3]
    return int(whole) * 1000 + int(frac)


def fingerprint(sqltext):
    st = sqlparse.parse(sqlparse.format(sqltext, keyword_case="upper", strip_comments=True))[0]
    out = []
    for t in st.flatten():
        if t.ttype in T.Number or t.ttype is T.String.Single:
            out.append("?")
        elif t.is_whitespace:
            if out and out[-1] != " ":
                out.append(" ")
        else:
            out.append(t.value)
    text = "".join(out).strip()
    while "?, ?" in text:
        text = text.replace("?, ?", "?")
    return text


def run_querylog(j):
    groups = {}
    order = []
    for line in read(j["file"]).split("\n"):
        if not line.startswith("("):
            continue
        close = line.index(")")
        t = ms(line[1:close])
        rest = line[close + 2:]
        cut = rest.rfind("; args=")
        q = rest[:cut]
        st = sqlparse.parse(q)[0]
        fp = fingerprint(q)
        if fp not in groups:
            groups[fp] = [0, 0, st.get_type(), tables_of(st, [])]
            order.append(fp)
        groups[fp][0] += 1
        groups[fp][1] += t
    ranked = sorted(order, key=lambda f: (-groups[f][1], f))
    for fp in ranked:
        n, total, kind, tabs = groups[fp]
        print("  %5dms x%d %s [%s] %s" % (total, n, kind, ", ".join(tabs), fp))


def run_tables(j):
    for k, st in enumerate(sqlparse.parse(source(j))):
        if st.token_first(skip_cm=True) is None:
            continue
        print("  %d %s [%s]" % (k + 1, st.get_type(), ", ".join(tables_of(st, []))))


def run_splitfiles(j):
    stem = os.path.splitext(os.path.basename(j["file"]))[0]
    outdir = os.path.join("data", "out", stem)
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for st in sqlparse.parse(read(j["file"])):
        if st.token_first(skip_cm=True) is None:
            continue
        n += 1
        kind = st.get_type().lower().replace(" ", "_")
        body = sqlparse.format(str(st), reindent=True, keyword_case="upper", strip_comments=True).strip()
        path = os.path.join(outdir, "%03d_%s.sql" % (n, kind))
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(body + "\n")
    for name in sorted(os.listdir(outdir)):
        with open(os.path.join(outdir, name), "rb") as fh:
            data = fh.read()
        first = data.decode("utf-8").split("\n")[0]
        print("  %s %d bytes %d lines  %s" % (name, len(data), data.count(b"\n"), first))


RUN = {"tokens": run_tokens, "split": run_split, "tree": run_tree, "info": run_info,
       "format": run_format, "lint": run_lint, "querylog": run_querylog,
       "tables": run_tables, "splitfiles": run_splitfiles}


def main():
    with open("data/jobs.jsonl", encoding="utf-8") as fh:
        jobs = [json.loads(line) for line in fh]
    for n, j in enumerate(jobs):
        src = j["file"] if "file" in j else (j["dir"] if "dir" in j else repr(j["sql"]))
        extra = ""
        if "opts" in j:
            extra = " " + opts_text(j["opts"])
        if j.get("strip_semicolon"):
            extra += " strip_semicolon"
        if "depth" in j and j["depth"] is not None:
            extra += " depth=%d" % j["depth"]
        print("== %d %s %s%s" % (n, j["op"], src, extra))
        RUN[j["op"]](j)


main()
