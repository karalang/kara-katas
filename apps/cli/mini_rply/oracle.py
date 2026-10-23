"""Run data/jobs.txt against the vendored rply 0.7.8 and print the results:
expected.out.

Run: python3 -I -B oracle.py > expected.out
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

from rply import LexerGenerator, ParserGenerator, ParsingError, LexingError  # noqa: E402
from rply.errors import ParserGeneratorError  # noqa: E402
from rply.token import Token  # noqa: E402

DATA = os.path.join(HERE, "data")


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8", newline="") as f:
        return f.read()


# ------------------------------------------------------------ grammars

class Node:
    def __init__(self, name, children):
        self.name = name
        self.children = children


class HandlerError(Exception):
    pass


def handle(token):
    pos = token.getsourcepos()
    raise HandlerError("unexpected %s %r at %d:%d"
                       % (token.gettokentype(), token.getstr(), pos.lineno, pos.colno))


def action(name):
    return lambda p: Node(name, list(p))


def load(rel):
    g = {"tokens": [], "lex": [], "ignore": [], "prec": [], "rules": [], "onerror": False}
    for line in read(rel).split("\n"):
        if not line or line.startswith("#"):
            continue
        word, _, rest = line.partition(" ")
        if word == "tokens":
            g["tokens"] = rest.split()
        elif word == "lex":
            name, _, pattern = rest.partition(" ")
            g["lex"].append((name, pattern))
        elif word == "ignore":
            g["ignore"].append(rest)
        elif word == "prec":
            parts = rest.split()
            g["prec"].append((parts[0], parts[1:]))
        elif word == "rule":
            text, _, prec = rest.partition(" %prec ")
            g["rules"].append((text, prec or None))
        elif word == "onerror":
            g["onerror"] = True
        else:
            raise SystemExit("bad grammar line " + line)
    return g


def build(rel):
    """(lexer, parser, warnings); the error and the warnings so far if the
    build raises."""
    g = load(rel)
    lg = LexerGenerator()
    for name, pattern in g["lex"]:
        lg.add(name, pattern)
    for pattern in g["ignore"]:
        lg.ignore(pattern)
    caught = []
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            pg = ParserGenerator(g["tokens"], precedence=g["prec"])
            for text, prec in g["rules"]:
                words = text.split()
                pg.production(text, precedence=prec)(action(words[0] if words else ""))
            if g["onerror"]:
                pg.error(handle)
            parser = pg.build()
            err = None
        except Exception as e:
            parser = None
            err = e
        caught = [str(x.message) for x in w]
    return lg.build(), parser, caught, err


def describe(e):
    if isinstance(e, KeyError):
        return "KeyError: %s" % e
    return "%s: %s" % (type(e).__name__, e)


def pos_str(sp):
    if sp is None:
        return "no position"
    return "%d:%d (index %d)" % (sp.lineno, sp.colno, sp.idx)


def show(x):
    if isinstance(x, Token):
        return "%s=%r" % (x.name, x.value)
    return "(" + " ".join([x.name] + [show(c) for c in x.children]) + ")"


def parse_text(parser, lexer, text):
    """The tree, or the error as a line."""
    try:
        return parser.parse(lexer.lex(text)), None
    except LexingError as e:
        return None, "LexingError at %s" % pos_str(e.getsourcepos())
    except ParsingError as e:
        return None, "ParsingError at %s" % pos_str(e.getsourcepos())
    except HandlerError as e:
        return None, "handler: %s" % e
    except Exception as e:
        return None, describe(e)


# ------------------------------------------------------------ jobs

def job_build(rel):
    _, parser, caught, err = build(rel)
    for m in caught:
        print("  warning: " + m)
    if err is not None:
        print("  error " + describe(err))
        return
    t = parser.lr_table
    defaults = sum(1 for d in t.default_reductions if d)
    print("  productions %d, states %d, default reductions %d"
          % (len(t.grammar.productions), len(t.lr_action), defaults))
    for tok, how in sorted((a, b) for _, a, b in t.sr_conflicts):
        print("  shift/reduce on %s, resolved as %s" % (tok, how))
    for chosen, rejected in sorted((a, b) for _, a, b in t.rr_conflicts):
        print("  reduce/reduce: %s over %s" % (chosen, rejected))


def job_tokens(grel, irel):
    lexer, _, _, _ = build(grel)
    stream = lexer.lex(read(irel))
    while True:
        try:
            t = next(stream)
        except StopIteration:
            break
        except LexingError as e:
            print("  LexingError at " + pos_str(e.getsourcepos()))
            break
        print("  %s=%r at %s" % (t.name, t.value, pos_str(t.getsourcepos())))


def job_parse(grel, irel):
    lexer, parser, _, err = build(grel)
    if err is not None:
        print("  error " + describe(err))
        return
    tree, err = parse_text(parser, lexer, read(irel))
    print("  " + (err if err is not None else show(tree)))


# ------------------------------------------------------------ !calc

class EvalError(Exception):
    pass


def floordiv(a, b):
    if b == 0:
        raise EvalError("division by zero")
    return a // b


def ev(n, env):
    if isinstance(n, Token):
        if n.name == "NUMBER":
            return int(n.value)
        if n.value not in env:
            raise EvalError("unknown variable %s" % n.value)
        return env[n.value]
    c = n.children
    if len(c) == 1:
        return ev(c[0], env)
    if len(c) == 2:
        return -ev(c[1], env)
    if isinstance(c[0], Token) and c[0].name == "LPAREN":
        return ev(c[1], env)
    if isinstance(c[0], Token) and c[0].name == "IDENT":
        args = []
        a = c[2]
        while len(a.children) == 3:
            args.insert(0, ev(a.children[2], env))
            a = a.children[0]
        args.insert(0, ev(a.children[0], env))
        f = c[0].value
        if f == "max":
            return max(args)
        if f == "min":
            return min(args)
        if f == "abs" and len(args) == 1:
            return abs(args[0])
        raise EvalError("unknown function %s/%d" % (f, len(args)))
    a, op, b = ev(c[0], env), c[1].name, ev(c[2], env)
    if op == "PLUS":
        return a + b
    if op == "MINUS":
        return a - b
    if op == "TIMES":
        return a * b
    if op == "DIV":
        return floordiv(a, b)
    if op == "MOD":
        if b == 0:
            raise EvalError("modulo by zero")
        return a % b
    if op == "POW":
        if b < 0:
            raise EvalError("negative exponent")
        return a ** b
    if op == "EQ":
        return int(a == b)
    if op == "LT":
        return int(a < b)
    return int(a > b)


def prog_calc(grel, irel):
    lexer, parser, _, _ = build(grel)
    env = {}
    for line in read(irel).split("\n"):
        if not line or line.startswith("#"):
            continue
        print("  > " + line)
        tree, err = parse_text(parser, lexer, line)
        if err is not None:
            print("    " + err)
            continue
        try:
            if len(tree.children) == 3:
                name = tree.children[0].value
                env[name] = ev(tree.children[2], env)
                print("    %s := %d" % (name, env[name]))
            else:
                print("    = %d" % ev(tree.children[0], env))
        except EvalError as e:
            print("    error: %s" % e)
    print("  variables: " + ", ".join("%s=%d" % kv for kv in sorted(env.items())))


# ------------------------------------------------------------ !json

def to_value(n):
    """A tree of value nodes as (kind, payload)."""
    c = n.children[0]
    if isinstance(c, Token):
        return ("scalar", c.value)
    if c.name == "object":
        pairs = []
        if len(c.children) == 3:
            m = c.children[1]
            stack = []
            while len(m.children) == 3:
                stack.append(m.children[2])
                m = m.children[0]
            stack.append(m.children[0])
            for p in reversed(stack):
                pairs.append((p.children[0].value, to_value(p.children[2])))
        return ("object", pairs)
    items = []
    if len(c.children) == 3:
        e = c.children[1]
        stack = []
        while len(e.children) == 3:
            stack.append(e.children[2])
            e = e.children[0]
        stack.append(e.children[0])
        items = [to_value(v) for v in reversed(stack)]
    return ("array", items)


def pretty(v, ind):
    kind, x = v
    if kind == "scalar":
        return x
    pad = "  " * (ind + 1)
    if kind == "object":
        if not x:
            return "{}"
        body = ",\n".join("%s%s: %s" % (pad, k, pretty(val, ind + 1)) for k, val in x)
        return "{\n" + body + "\n" + "  " * ind + "}"
    if not x:
        return "[]"
    body = ",\n".join(pad + pretty(val, ind + 1) for val in x)
    return "[\n" + body + "\n" + "  " * ind + "]"


def stats(v, depth, acc):
    kind, x = v
    acc["depth"] = max(acc["depth"], depth)
    if kind == "scalar":
        acc["scalars"] += 1
    elif kind == "object":
        acc["objects"] += 1
        for _, val in x:
            stats(val, depth + 1, acc)
    else:
        acc["arrays"] += 1
        for val in x:
            stats(val, depth + 1, acc)


def prog_json(grel, files):
    lexer, parser, _, _ = build(grel)
    for rel in files:
        tree, err = parse_text(parser, lexer, read(rel))
        if err is not None:
            print("  %s: %s" % (rel, err))
            continue
        v = to_value(tree)
        acc = {"depth": 0, "scalars": 0, "objects": 0, "arrays": 0}
        stats(v, 1, acc)
        print("  %s: %d objects, %d arrays, %d scalars, depth %d"
              % (rel, acc["objects"], acc["arrays"], acc["scalars"], acc["depth"]))
        for line in pretty(v, 0).split("\n"):
            print("    | " + line)


# ------------------------------------------------------------ !query

def load_table(name):
    path = "tables/%s.csv" % name
    if not os.path.exists(os.path.join(DATA, path)):
        raise EvalError("no table %s" % name)
    rows = [r.split(",") for r in read(path).split("\n") if r]
    return rows[0], rows[1:]


def flatten(n, item_at):
    out = []
    while len(n.children) == 3:
        out.insert(0, n.children[2])
        n = n.children[0]
    out.insert(0, n.children[0])
    return out


def is_int(s):
    t = s[1:] if s.startswith("-") else s
    return t.isdigit() and t.isascii()


def operand(o, header, row):
    t = o.children[0]
    if t.name == "IDENT":
        if t.value not in header:
            raise EvalError("no column %s" % t.value)
        return row[header.index(t.value)]
    if t.name == "STRING":
        return t.value[1:-1]
    return t.value


def compare(a, op, b):
    if is_int(a) and is_int(b):
        a, b = int(a), int(b)
    return {"=": a == b, "<>": a != b, "<": a < b, ">": a > b,
            "<=": a <= b, ">=": a >= b}[op]


def holds(c, header, row):
    ch = c.children
    if len(ch) == 2:
        return not holds(ch[1], header, row)
    if isinstance(ch[0], Token):
        return holds(ch[1], header, row)
    if ch[1].name == "OR":
        return holds(ch[0], header, row) or holds(ch[2], header, row)
    if ch[1].name == "AND":
        return holds(ch[0], header, row) and holds(ch[2], header, row)
    return compare(operand(ch[0], header, row), ch[1].value, operand(ch[2], header, row))


def sort_key(v):
    return (0, int(v), "") if is_int(v) else (1, 0, v)


def run_query(tree):
    _, cols, _, table, where, order, limit = tree.children
    header, rows = load_table(table.value)
    if isinstance(cols.children[0], Token):
        names = header
    else:
        names = [t.value for t in flatten(cols.children[0], 2)]
    for n in names:
        if n not in header:
            raise EvalError("no column %s" % n)
    if where.children:
        rows = [r for r in rows if holds(where.children[1], header, r)]
    if order.children:
        col = order.children[2].value
        if col not in header:
            raise EvalError("no column %s" % col)
        k = header.index(col)
        desc = bool(order.children[3].children) and order.children[3].children[0].name == "DESC"
        rows = sorted(rows, key=lambda r: sort_key(r[k]), reverse=desc)
    if limit.children:
        rows = rows[:int(limit.children[1].value)]
    idx = [header.index(n) for n in names]
    out = [names] + [[r[i] for i in idx] for r in rows]
    widths = [max(len(r[i]) for r in out) for i in range(len(names))]
    lines = []
    for j, r in enumerate(out):
        lines.append("  ".join(v.ljust(w) for v, w in zip(r, widths)).rstrip())
        if j == 0:
            lines.append("  ".join("-" * w for w in widths))
    lines.append("(%d row%s)" % (len(rows), "" if len(rows) == 1 else "s"))
    return lines


def prog_query(grel, irel):
    lexer, parser, _, _ = build(grel)
    for line in read(irel).split("\n"):
        if not line:
            continue
        print("  > " + line)
        tree, err = parse_text(parser, lexer, line)
        if err is not None:
            print("    " + err)
            continue
        try:
            for out in run_query(tree):
                print("    " + out)
        except EvalError as e:
            print("    error: %s" % e)


def main():
    for line in read("jobs.txt").split("\n"):
        if not line:
            continue
        if line.startswith("#"):
            print(line)
            continue
        print("> " + line)
        parts = line.split(" ")
        cmd, args = parts[0], parts[1:]
        if cmd == "build":
            job_build(args[0])
        elif cmd == "tokens":
            job_tokens(args[0], args[1])
        elif cmd == "parse":
            job_parse(args[0], args[1])
        elif cmd == "!calc":
            prog_calc(args[0], args[1])
        elif cmd == "!json":
            prog_json(args[0], args[1:])
        elif cmd == "!query":
            prog_query(args[0], args[1])
        else:
            raise SystemExit("unknown job " + line)


main()
