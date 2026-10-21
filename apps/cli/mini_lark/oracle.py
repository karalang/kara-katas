"""Oracle for mini_lark: runs data/jobs.txt with the vendored lark 1.2.2.

Run from this directory:  python3 -s -P -B oracle.py > expected.out
Every set lark keeps (expected terminals, accepts) is printed sorted, since
Python's set order changes from run to run.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lark import Lark, Tree, Token  # noqa: E402
from lark.exceptions import (  # noqa: E402
    UnexpectedInput, UnexpectedToken, UnexpectedCharacters, GrammarError, LarkError,
)
from lark.indenter import Indenter  # noqa: E402

DATA = os.path.join(HERE, "data")
GDIR = os.path.join(DATA, "grammars")
IDIR = os.path.join(DATA, "inputs")
LDIR = os.path.join(DATA, "lark_grammars")

STATS = {"jobs": 0, "errors": 0}


class TreeIndenter(Indenter):
    NL_type = "_NL"
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 8


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


_CACHE = {}


def load(name, **kw):
    key = (name, tuple(sorted(kw.items())))
    if key not in _CACHE:
        opts = dict(parser="lalr", import_paths=[GDIR])
        if name == "outline.lark":
            opts["postlex"] = TreeIndenter()
        opts.update(kw)
        _CACHE[key] = Lark(read(os.path.join(GDIR, name)), **opts)
    return _CACHE[key]


def user_names(parser, names):
    d = parser.lexer_conf.terminals_by_name if hasattr(parser, "lexer_conf") else {}
    out = []
    for n in names:
        out.append(d[n].user_repr() if n in d else n)
    return sorted(out)


def fmt_error(e, text, parser):
    """lark's own messages, with every set sorted."""
    STATS["errors"] += 1
    if isinstance(e, UnexpectedCharacters):
        msg = "No terminal matches '%s' in the current parser context, at line %d col %d" % (
            e.char, e.line, e.column)
        msg += "\n\n" + e.get_context(text)
        if e.allowed:
            msg += "Expected one of: \n\t* %s\n" % "\n\t* ".join(user_names(parser, e.allowed))
        if e.token_history:
            msg += "\nPrevious tokens: %s\n" % ", ".join(repr(t) for t in e.token_history)
        return "UnexpectedCharacters: " + msg
    if isinstance(e, UnexpectedToken):
        exp = e.accepts or e.expected
        msg = "Unexpected token %r at line %s, column %s.\n" % (e.token, e.line, e.column)
        msg += "Expected one of: \n\t* %s\n" % "\n\t* ".join(user_names(parser, exp))
        if e.token.type != "$END":
            msg += e.get_context(text)
        return "UnexpectedToken: " + msg
    return "%s: %s\n" % (type(e).__name__, e)


def out(s=""):
    sys.stdout.write(s + "\n")


def emit(s):
    sys.stdout.write(s if s.endswith("\n") else s + "\n")


# ---------------------------------------------------------------- grammar
def job_grammar(name):
    p = load(name)
    terms = sorted(p.terminals, key=lambda t: t.name)
    out("terminals: %d" % len(terms))
    for t in terms:
        flags = "".join(sorted(t.pattern.flags))
        out("  %s %s %r%s prio=%d width=%d..%d" % (
            t.name, t.pattern.type, t.pattern.value, (" flags=" + flags) if flags else "",
            t.priority, t.pattern.min_width, min(t.pattern.max_width, 999)))
    ign = sorted(p.ignore_tokens)
    out("ignore: %s" % (" ".join(ign) if ign else "-"))
    rules = []
    for r in p.rules:
        o = r.options
        s = "%s -> %s" % (r.origin.name, " ".join(x.name for x in r.expansion) or "<empty>")
        if r.alias:
            s += " as " + r.alias
        extras = []
        if o.expand1:
            extras.append("expand1")
        if o.keep_all_tokens:
            extras.append("keep")
        if o.priority is not None:
            extras.append("prio=%d" % o.priority)
        if o.template_source:
            extras.append("from=" + o.template_source)
        if o.empty_indices and any(o.empty_indices):
            extras.append("empty=" + "".join("1" if b else "0" for b in o.empty_indices))
        if extras:
            s += "  [" + " ".join(extras) + "]"
        rules.append(s)
    rules.sort()
    out("rules: %d" % len(rules))
    for s in rules:
        out("  " + s)
    out("states: %d" % len(p.parser.parser.parser.parse_table.states))


# ---------------------------------------------------------------- calc
class CalcError(Exception):
    pass


def calc_eval(t, env):
    if isinstance(t, Token):
        raise CalcError("unexpected token " + t.type)
    d = t.data
    c = t.children
    if d == "number":
        return int(c[0])
    if d == "var":
        if str(c[0]) not in env:
            raise CalcError("undefined variable " + str(c[0]))
        return env[str(c[0])]
    if d == "neg":
        return -calc_eval(c[0], env)
    if d in ("add", "sub", "mul", "div", "mod", "pow"):
        a = calc_eval(c[0], env)
        b = calc_eval(c[1], env)
        if d == "add":
            return a + b
        if d == "sub":
            return a - b
        if d == "mul":
            return a * b
        if d in ("div", "mod"):
            if b == 0:
                raise CalcError("division by zero")
            return a // b if d == "div" else a % b
        if b < 0:
            raise CalcError("negative exponent")
        return a ** b
    if d == "call":
        fname = str(c[0])
        args = [calc_eval(x, env) for x in c[1:] if x is not None]
        if fname == "max" and args:
            return max(args)
        if fname == "min" and args:
            return min(args)
        if fname == "abs" and len(args) == 1:
            return abs(args[0])
        raise CalcError("unknown function %s/%d" % (fname, len(args)))
    raise CalcError("unknown node " + d)


def job_calc(inp):
    p = load("calc.lark")
    env = {}
    for line in read(os.path.join(IDIR, inp)).split("\n"):
        if not line.strip():
            continue
        out("calc> " + line)
        try:
            t = p.parse(line)
        except UnexpectedInput as e:
            emit(fmt_error(e, line, p))
            continue
        try:
            if isinstance(t, Tree) and t.data == "assign_var":
                v = calc_eval(t.children[1], env)
                env[str(t.children[0])] = v
                out("%s = %d" % (t.children[0], v))
            else:
                out("= %d" % calc_eval(t, env))
        except CalcError as e:
            STATS["errors"] += 1
            out("error: %s" % e)
    out("vars: " + ", ".join("%s=%d" % (k, env[k]) for k in sorted(env)))


# ---------------------------------------------------------------- json
JSON_ERRORS = [
    ("missing value", ['{"foo": }']),
    ("missing opening", ['{"foo": ]}', '{"foor": }}', '{"foo": }']),
    ("missing closing", ['{"foo": [}', '{', '{"a": 1', '[1']),
    ("missing comma", ['[1 2]', '[false 1]', '["b" 1]', '{"a":true 1:4}', '{"a":1 1:4}', '{"a":"b" 1:4}']),
    ("trailing comma", ['[,]', '[1,]', '[1,2,]', '{"foo":1,}', '{"foo":false,"bar":true,}']),
    ("double comma", ['[1,,]', '{"a": 1, "b": [1, 2,, 3]}']),
]


def json_walk(t, path, lines):
    if isinstance(t, Token):
        lines.append("%s = %s" % (path, t))
        return
    d = t.data
    if d == "object":
        if not [c for c in t.children if c is not None]:
            lines.append("%s = {}" % path)
        for pair in t.children:
            if pair is None:
                continue
            key = str(pair.children[0].children[0])[1:-1]
            json_walk(pair.children[1], path + "." + key, lines)
    elif d == "array":
        items = [c for c in t.children if c is not None]
        if not items:
            lines.append("%s = []" % path)
        for i, c in enumerate(items):
            json_walk(c, "%s[%d]" % (path, i), lines)
    elif d == "string":
        lines.append("%s = %s" % (path, t.children[0]))
    elif d == "number":
        lines.append("%s = %s" % (path, t.children[0]))
    else:
        lines.append("%s = %s" % (path, d))


def job_json(inp):
    p = load("json.lark")
    text = read(os.path.join(IDIR, inp))
    try:
        t = p.parse(text)
    except UnexpectedInput as e:
        emit(fmt_error(e, text, p))
        label = e.match_examples(p.parse, JSON_ERRORS, use_accepts=True)
        out("classified: %s" % (label or "unknown"))
        return
    lines = []
    json_walk(t, "$", lines)
    for ln in lines:
        out(ln)
    out("subtrees: %d" % len(list(t.iter_subtrees())))


def job_recover(inp):
    p = load("json.lark")
    text = read(os.path.join(IDIR, inp))
    skipped = []

    def on_error(e):
        if isinstance(e, UnexpectedToken) and e.token.type != "$END":
            skipped.append(e)
            out("skip %r at line %d, column %d" % (e.token, e.line, e.column))
            return True
        return False

    try:
        t = p.parse(text, on_error=on_error)
    except UnexpectedInput as e:
        emit(fmt_error(e, text, p))
        return
    STATS["errors"] += len(skipped)
    emit(t.pretty())


# ---------------------------------------------------------------- conf
UNITS = {"ms": 1, "s": 1000, "m": 60000, "h": 3600000, "d": 86400000,
         "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}


def conf_value(t):
    d = t.data
    c = t.children
    if d == "string":
        return str(c[0])
    if d == "int":
        return str(int(c[0]))
    if d in ("duration", "size"):
        s = str(c[0])
        i = 0
        while i < len(s) and s[i].isdigit():
            i += 1
        n = int(s[:i]) * UNITS[s[i:]]
        return "%d%s (%s)" % (n, "ms" if d == "duration" else "B", s)
    if d == "true":
        return "true"
    if d == "false":
        return "false"
    if d == "env":
        return "${%s}" % str(c[0])[1:-1]
    if d == "list":
        return "[" + ", ".join(conf_value(x) for x in c if x is not None) + "]"
    raise ValueError(d)


def conf_items(items, prefix, entries, order):
    for it in items:
        if it.data == "block":
            name = str(it.children[0])
            label = it.children[1]
            p = prefix + name + ("[" + str(label)[1:-1] + "]" if label is not None else "") + "."
            conf_items(it.children[2:], p, entries, order)
        else:
            key = prefix + ".".join(str(x) for x in it.children[0].children)
            val = conf_value(it.children[1])
            if it.data == "append":
                if key not in entries or not entries[key].startswith("["):
                    STATS["errors"] += 1
                    out("error: += on %s, which is not a list" % key)
                    continue
                old = entries[key]
                entries[key] = old[:-1] + (", " if old != "[]" else "") + val + "]"
            else:
                if key in entries:
                    out("note: %s redefined" % key)
                else:
                    order.append(key)
                entries[key] = val


def job_conf(inp):
    p = load("conf.lark")
    text = read(os.path.join(IDIR, inp))
    try:
        t = p.parse(text)
    except UnexpectedInput as e:
        emit(fmt_error(e, text, p))
        return
    entries = {}
    order = []
    conf_items(t.children, "", entries, order)
    for k in order:
        out("%s = %s" % (k, entries[k]))


# ---------------------------------------------------------------- sql
def sql_expr(t, cols):
    if isinstance(t, Token):
        return str(t)
    d = t.data
    c = t.children
    if d == "ref":
        cols.add(str(c[0]))
        return str(c[0])
    if d == "qualified":
        cols.add("%s.%s" % (c[0], c[1]))
        return "%s.%s" % (c[0], c[1])
    if d in ("int", "string"):
        return str(c[0])
    if d == "func":
        args = [sql_expr(x, cols) for x in c[1:] if x is not None]
        return "%s(%s)" % (str(c[0]).lower(), ", ".join(args) if args else "*")
    if d in ("or_", "and_"):
        return "(%s %s %s)" % (sql_expr(c[0], cols), d[:-1].upper(), sql_expr(c[1], cols))
    if d == "not_":
        return "(NOT %s)" % sql_expr(c[0], cols)
    if d in ("compare", "binop"):
        return "(%s %s %s)" % (sql_expr(c[0], cols), c[1], sql_expr(c[2], cols))
    if d == "is_null":
        return "(%s IS NULL)" % sql_expr(c[0], cols)
    if d == "in_list":
        return "(%s IN [%s])" % (sql_expr(c[0], cols), ", ".join(sql_expr(x, cols) for x in c[1:]))
    return "<%s>" % d


def sql_source(t):
    name, alias = t.children
    return str(name) + (" " + str(alias) if alias is not None else "")


def job_sql(inp):
    p = load("sql.lark")
    text = read(os.path.join(IDIR, inp))
    try:
        t = p.parse(text)
    except UnexpectedInput as e:
        emit(fmt_error(e, text, p))
        return
    for i, sel in enumerate(x for x in t.children if x is not None):
        cols = set()
        c = sel.children
        distinct = c[0] is not None
        out("query %d%s" % (i + 1, " (distinct)" if distinct else ""))
        columns = c[1]
        if columns.data == "all_columns":
            out("  columns: *")
        else:
            parts = []
            for col in columns.children:
                e = sql_expr(col.children[0], cols)
                if col.children[1] is not None:
                    e += " as " + str(col.children[1])
                parts.append(e)
            out("  columns: " + ", ".join(parts))
        out("  from: " + sql_source(c[2]))
        for x in c[3:]:
            if x is None:
                continue
            if x.data == "join":
                kind = str(x.children[0]).upper() if x.children[0] is not None else "INNER"
                out("  join: %s %s on %s" % (kind, sql_source(x.children[1]), sql_expr(x.children[2], cols)))
            elif x.data == "where":
                out("  where: " + sql_expr(x.children[0], cols))
            elif x.data == "group":
                out("  group: " + ", ".join(sql_expr(e, cols) for e in x.children))
            elif x.data == "order":
                parts = []
                for o in x.children:
                    s = sql_expr(o.children[0], cols)
                    d = o.children[1]
                    parts.append(s + " " + (str(d).upper() if d is not None else "ASC"))
                out("  order: " + ", ".join(parts))
            elif x.data == "limit":
                out("  limit: %s" % x.children[0])
        out("  names: " + ", ".join(sorted(cols)))


# ---------------------------------------------------------------- outline
def job_outline(inp):
    p = load("outline.lark")
    text = read(os.path.join(IDIR, inp))
    try:
        t = p.parse(text)
    except UnexpectedInput as e:
        emit(fmt_error(e, text, p))
        return
    except LarkError as e:
        STATS["errors"] += 1
        out("%s: %s" % (type(e).__name__, e))
        return
    counts = {"items": 0, "done": 0}
    tags = {}

    def walk(item, depth):
        counts["items"] += 1
        entry = item.children[0]
        words = []
        done = False
        for tok in entry.children:
            if tok.type == "DONE":
                done = True
            elif tok.type == "TAG":
                tags[str(tok)] = tags.get(str(tok), 0) + 1
                words.append(str(tok))
            else:
                words.append(str(tok))
        if done:
            counts["done"] += 1
        kids = [k for k in item.children[1:] if k is not None]
        out("%s%s %s%s" % ("  " * depth, "[x]" if done else "[ ]", " ".join(words),
                          " (%d)" % len(kids) if kids else ""))
        for k in kids:
            walk(k, depth + 1)

    roots = [t] if t.data == "item" else t.children
    for r in roots:
        walk(r, 0)
    out("items: %d, done: %d" % (counts["items"], counts["done"]))
    out("tags: " + ", ".join("%s=%d" % (k, tags[k]) for k in sorted(tags)))


# ---------------------------------------------------------------- generic
def parse_opts(args):
    kw = {}
    for a in args:
        k, v = a.split("=", 1)
        kw[k] = {"true": True, "false": False}.get(v, v)
    return kw


def job_parse(gname, inp, opts):
    p = load(gname, **parse_opts(opts))
    text = read(os.path.join(IDIR, inp))
    try:
        t = p.parse(text)
    except UnexpectedInput as e:
        emit(fmt_error(e, text, p))
        return
    emit(t.pretty())
    toks = list(t.scan_values(lambda v: isinstance(v, Token)))
    out("tokens: %d, subtrees: %d" % (len(toks), len(list(t.iter_subtrees()))))


def job_lex(gname, inp):
    p = load(gname, lexer="basic")
    for line in read(os.path.join(IDIR, inp)).split("\n"):
        if not line.strip():
            continue
        try:
            toks = list(p.lex(line))
            out("%s: %s" % (line, " ".join("%s@%d=%s" % (t.type, t.column, t) for t in toks)))
        except UnexpectedInput as e:
            out("%s: error" % line)
            emit(fmt_error(e, line, p))


def job_complete(gname, text):
    p = load(gname)
    ip = p.parse_interactive(text)
    try:
        toks = ip.exhaust_lexer()
    except UnexpectedInput as e:
        emit(fmt_error(e, text, p))
        return
    out("input: %r (%d tokens)" % (text, len(toks)))
    acc = sorted(ip.accepts())
    out("accepts: " + " ".join(acc))
    out("as written: " + " ".join(user_names(p, acc)))


def sort_dashes(msg):
    """Sort each run of tab-dash lines: lark builds them from a set."""
    lines = msg.split("\n")
    res = []
    run = []
    for ln in lines + [None]:
        if ln is not None and ln.startswith("\t- "):
            run.append(ln)
            continue
        res.extend(sorted(run))
        run = []
        if ln is not None:
            res.append(ln)
    return "\n".join(res)


def job_badgrammars():
    blocks = read(os.path.join(DATA, "bad_grammars.txt")).split("%%% ")[1:]
    for b in blocks:
        title, _, body = b.partition("\n")
        out("-- " + title)
        try:
            Lark(body, parser="lalr", import_paths=[GDIR])
            out("ok")
        except GrammarError as e:
            STATS["errors"] += 1
            emit("GrammarError: %s" % sort_dashes(str(e)))
        except UnexpectedInput as e:
            emit(fmt_error(e, body, None))
        except LarkError as e:
            STATS["errors"] += 1
            emit("%s: %s" % (type(e).__name__, e))


def job_meta():
    meta = Lark(read(os.path.join(LDIR, "lark.lark")), parser="lalr")
    files = [(GDIR, f) for f in sorted(os.listdir(GDIR))] + [(LDIR, f) for f in sorted(os.listdir(LDIR))]
    for d, f in files:
        text = read(os.path.join(d, f))
        try:
            t = meta.parse(text)
        except UnexpectedInput as e:
            out("%s: parse error" % f)
            emit(fmt_error(e, text, meta))
            continue
        kinds = {}
        for c in t.children:
            kinds[c.data] = kinds.get(c.data, 0) + 1
        out("%s: %s" % (f, ", ".join("%s=%d" % (k, kinds[k]) for k in sorted(kinds))))


def main():
    for raw in read(os.path.join(DATA, "jobs.txt")).split("\n"):
        if not raw or raw.startswith("#"):
            continue
        parts = raw.split(" ")
        cmd = parts[0]
        STATS["jobs"] += 1
        out("== " + raw)
        if cmd == "grammar":
            job_grammar(parts[1])
        elif cmd == "calc":
            job_calc(parts[1])
        elif cmd == "json":
            job_json(parts[1])
        elif cmd == "recover":
            job_recover(parts[1])
        elif cmd == "conf":
            job_conf(parts[1])
        elif cmd == "sql":
            job_sql(parts[1])
        elif cmd == "outline":
            job_outline(parts[1])
        elif cmd == "parse":
            job_parse(parts[1], parts[2], parts[3:])
        elif cmd == "lex":
            job_lex(parts[1], parts[2])
        elif cmd == "complete":
            job_complete(parts[1], raw.split(" ", 2)[2])
        elif cmd == "badgrammars":
            job_badgrammars()
        elif cmd == "meta":
            job_meta()
        elif cmd == "summary":
            out("jobs: %d, errors reported: %d" % (STATS["jobs"], STATS["errors"]))
        else:
            out("unknown job " + cmd)


if __name__ == "__main__":
    main()
