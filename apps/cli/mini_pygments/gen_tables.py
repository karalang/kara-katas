# Prints the Kara functions that hold Pygments 2.17.2's own tables, for
# mini_pygments.kara: the lexer map (every lexer's names, file patterns,
# mimetypes and priority), the token definitions of the lexers the port
# runs, exactly as their classes write them (before RegexLexerMeta
# processes them), the C lexer's type lists, STANDARD_TYPES, and the
# styles the jobs use.
import re

import pygments.lexer as L
import pygments.unistring as uni
from pygments.lexers import get_lexer_by_name, find_lexer_class_by_name
from pygments.lexers._mapping import LEXERS
from pygments.styles import get_style_by_name, STYLE_MAP
from pygments.token import STANDARD_TYPES, _TokenType

IMPLEMENTED = ["python", "bash", "ini", "diff", "toml", "nginx", "css", "sql", "docker",
               "go", "rust", "javascript", "systemd", "properties", "xml", "html",
               "pytb", "c"]
STYLES = ["default", "monokai", "friendly", "emacs", "solarized-dark", "bw"]
import pygments.lexers.javascript as _js
# longest first, so a class that contains another is taken whole
UNI = dict(sorted({"xid_start": uni.xid_start, "xid_continue": uni.xid_continue,
                   "js_ident_start": _js.JS_IDENT_START, "js_ident_part": _js.JS_IDENT_PART}.items(),
                  key=lambda kv: -len(kv[1])))


def esc_char(ch):
    o = ord(ch)
    if ch == "\\":
        return "\\\\"
    if ch == '"':
        return '\\"'
    if ch == "{":
        return "{"
    if 32 <= o < 127:
        return ch
    if ch == "\n":
        return "\\n"
    if ch == "\t":
        return "\\t"
    return "\\u{%x}" % o


def lit(s):
    return '"' + "".join(esc_char(c) for c in s) + '"'


def strlit(s):
    # a String expression; the long Unicode classes become calls
    parts = []
    rest = s
    while rest:
        best = None
        for name, val in UNI.items():
            i = rest.find(val)
            if i >= 0 and (best is None or i < best[0]):
                best = (i, name, val)
        if best is None:
            parts.append(lit(rest) + ".to_string()")
            break
        i, name, val = best
        if i:
            parts.append(lit(rest[:i]) + ".to_string()")
        parts.append(name + "()")
        rest = rest[i + len(val):]
    if not parts:
        return '"".to_string()'
    return " + ".join(parts) if len(parts) > 1 else parts[0]


def svec(items):
    return "sv(vec![" + ", ".join(lit(x) for x in items) + "])"


def tok(t):
    assert type(t) is _TokenType, t
    return lit(".".join(t))


def closure(fn):
    return dict(zip(fn.__code__.co_freevars, (c.cell_contents for c in fn.__closure__)))


def act(a):
    if a is None:
        return "Act.Skip"
    if type(a) is _TokenType:
        return "Act.Tok(%s.to_string())" % tok(a)
    q = a.__qualname__
    if q.startswith("bygroups"):
        return "Act.Groups(vec![%s])" % ", ".join(act(x) for x in closure(a)["args"])
    if q.startswith("using"):
        c = closure(a)
        other = c.get("_other", L.this)
        name = "this" if other is L.this else other.__name__
        stack = list(c["gt_kwargs"].get("stack", ()))
        kw = sorted(c["kwargs"].items())
        assert not kw, kw
        return "Act.Using(%s.to_string(), %s)" % (lit(name), svec(stack))
    raise AssertionError("unknown action %r" % (a,))


def new_state(ns):
    if isinstance(ns, L.combined):
        return "RawNew.Combined(%s)" % svec(list(ns))
    if isinstance(ns, str):
        return "RawNew.Name(%s.to_string())" % lit(ns)
    if isinstance(ns, tuple):
        return "RawNew.Tuple(%s)" % svec(list(ns))
    raise AssertionError(ns)


def pat(p):
    if isinstance(p, L.words):
        return "Pat.Words(%s, %s, %s)" % (svec(list(p.words)), strlit(p.prefix), strlit(p.suffix))
    assert isinstance(p, str), p
    return "Pat.Re(%s)" % strlit(p)


def rule(r):
    if isinstance(r, L.include):
        return "RawRule.Include(%s.to_string())" % lit(str(r))
    if r is L.inherit:
        return "RawRule.Inherit"
    if isinstance(r, L.default):
        return "RawRule.Default(%s)" % new_state(r.state)
    assert type(r) is tuple and len(r) in (2, 3), r
    ns = new_state(r[2]) if len(r) == 3 else "RawNew.NoNew"
    return "RawRule.Rule(%s, %s, %s)" % (pat(r[0]), act(r[1]), ns)


out = []


def fn(name, ret, body):
    out.append("")
    out.append("fn %s() -> %s {" % (name, ret))
    out.extend("    " + b for b in body)
    out.append("}")


# ------------------------------------------------------------ the map
body = ["let mut v: Vec[LexInfo] = Vec.new();"]
for clsname, (mod, name, aliases, filenames, mimes) in LEXERS.items():
    cls = find_lexer_class_by_name(aliases[0]) if aliases else None
    if cls is None or cls.__name__ != clsname:
        import importlib
        cls = getattr(importlib.import_module(mod), clsname)
    pri = float(cls.priority)
    body.append("v.push(LexInfo { cls: %s.to_string(), name: %s.to_string(), aliases: %s, filenames: %s, mimetypes: %s, priority: %r });"
                % (lit(clsname), lit(name), svec(aliases), svec(filenames), svec(mimes), pri))
body.append("v")
# split into parts of 150 lines
chunks = [body[1:-1][i:i + 150] for i in range(0, len(body) - 2, 150)]
fn("lexer_map", "Vec[LexInfo]", ["let mut v: Vec[LexInfo] = Vec.new();"]
   + ["lexer_map_%d(mut v);" % k for k in range(len(chunks))] + ["v"])
for k, ch in enumerate(chunks):
    out.append("")
    out.append("fn lexer_map_%d(v: mut ref Vec[LexInfo]) {" % k)
    out.extend("    " + b for b in ch)
    out.append("}")

# ------------------------------------------------------- token tables
classes = []
for alias in IMPLEMENTED:
    cls = type(get_lexer_by_name(alias))
    for c in cls.__mro__:
        if "tokens" in c.__dict__ and c is not L.RegexLexer and c not in classes:
            classes.append(c)
# lexers reached through using()
seen = True
while seen:
    seen = False
    for c in list(classes):
        for rules in c.__dict__["tokens"].values():
            for r in rules:
                acts = []
                if type(r) is tuple and len(r) > 1 and callable(r[1]) and type(r[1]) is not _TokenType:
                    acts.append(r[1])
                while acts:
                    a = acts.pop()
                    if a.__qualname__.startswith("bygroups"):
                        acts.extend(x for x in closure(a)["args"] if x is not None and type(x) is not _TokenType)
                    elif a.__qualname__.startswith("using"):
                        o = closure(a).get("_other", L.this)
                        if o is not L.this:
                            for c2 in o.__mro__:
                                if "tokens" in c2.__dict__ and c2 is not L.RegexLexer and c2 not in classes:
                                    classes.append(c2)
                                    seen = True

names = []
for c in classes:
    mro = [m.__name__ for m in c.__mro__ if "tokens" in m.__dict__ and m is not L.RegexLexer]
    flags = int(c.flags) if hasattr(c, "flags") else 0
    states = c.__dict__["tokens"]
    fname = "tokens_" + c.__name__.lower()
    names.append(fname)
    body = ["let mut s: Vec[(String, Vec[RawRule])] = Vec.new();"]
    for st, rules in states.items():
        body.append("s.push((%s.to_string(), vec![" % lit(st))
        for r in rules:
            body.append("    %s," % rule(r))
        body.append("]));")
    body.append("ClassDef { name: %s.to_string(), mro: %s, flags: %d, states: s }" % (lit(c.__name__), svec(mro), flags))
    fn(fname, "ClassDef", body)

fn("class_defs", "Vec[ClassDef]", ["let mut v: Vec[ClassDef] = Vec.new();"]
   + ["v.push(%s());" % n for n in names] + ["v"])

for name, val in UNI.items():
    fn(name, "String", [lit(val) + ".to_string()"])

cl = type(get_lexer_by_name("c"))
for attr in ["stdlib_types", "c99_types", "c11_atomic_types", "linux_types"]:
    fn("c_" + attr, "Vec[String]", [svec(sorted(getattr(cl, attr)))])

# ------------------------------------------------- tokens and styles
fn("standard_types", "Vec[(String, String)]",
   ["vec!["] + ["    (%s.to_string(), %s.to_string())," % (tok(t), lit(v)) for t, v in STANDARD_TYPES.items()] + ["]"])

fn("style_names", "Vec[String]", [svec(list(STYLE_MAP))])
body = ["let mut v: Vec[StyleDef] = Vec.new();"]
for sname in STYLES:
    st = get_style_by_name(sname)
    def opt(x):
        return "None" if x is None else "Some(%s.to_string())" % lit(x)
    items = ", ".join("(%s.to_string(), %s.to_string())" % (tok(t), lit(v)) for t, v in st.styles.items())
    body.append("v.push(StyleDef { name: %s.to_string(), background: %s, highlight: %s, lineno: %s, lineno_bg: %s, lineno_special: %s, lineno_special_bg: %s, styles: vec![%s] });"
                % (lit(sname), opt(st.background_color), opt(st.highlight_color), opt(st.line_number_color),
                   opt(st.line_number_background_color), opt(st.line_number_special_color),
                   opt(st.line_number_special_background_color), items))
body.append("v")
fn("style_defs", "Vec[StyleDef]", body)

print("// ------------------------------------------------- generated tables")
print("// Printed by gen_tables.py from Pygments 2.17.2's own classes.")
print("\n".join(out))
