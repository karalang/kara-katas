"""The Python mirror of mini_infer: the same type checker, written first,
whose transcript is expected.out. No OCaml toolchain is installed here, so
this mirror is the oracle; the messages follow OCaml 5's wording and the
algorithms follow OCaml's (levels-based generalisation, Maranget's
usefulness for the match warnings).

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import sys

# ------------------------------------------------------------------ lexer

KEYWORDS = {"let", "rec", "and", "in", "fun", "function", "if", "then", "else",
            "match", "with", "when", "type", "of", "true", "false", "mod"}
SYMS2 = [";;", "::", "->", "<>", "<=", ">=", "||", "&&"]
SYMS1 = "()[]{},;:=<>+-*/^|.@"


class Span:
    __slots__ = ("sl", "sc", "el", "ec", "so", "eo")

    def __init__(self, sl, sc, el, ec, so, eo):
        self.sl, self.sc, self.el, self.ec, self.so, self.eo = sl, sc, el, ec, so, eo


def join(a, b):
    return Span(a.sl, a.sc, b.el, b.ec, a.so, b.eo)


class Tok:
    __slots__ = ("kind", "text", "span")

    def __init__(self, kind, text, span):
        self.kind, self.text, self.span = kind, text, span


class Diag(Exception):
    def __init__(self, span, level, msg, notes=()):
        self.span, self.level, self.msg, self.notes = span, level, msg, list(notes)


def lex(src):
    toks = []
    i, line, col = 0, 1, 1
    n = len(src)

    def adv(k):
        nonlocal i, line, col
        for _ in range(k):
            if src[i] == "\n":
                line += 1
                col = 1
            else:
                col += 1
            i += 1

    while True:
        while i < n:
            c = src[i]
            if c in " \t\r\n":
                adv(1)
            elif src.startswith("(*", i):
                sl, sc, so = line, col, i
                depth = 0
                while True:
                    if i >= n:
                        raise Diag(Span(sl, sc, sl, sc + 2, so, so + 2), "error",
                                   "this comment is not terminated")
                    if src.startswith("(*", i):
                        depth += 1
                        adv(2)
                    elif src.startswith("*)", i):
                        depth -= 1
                        adv(2)
                        if depth == 0:
                            break
                    else:
                        adv(1)
            else:
                break
        if i >= n:
            toks.append(Tok("eof", "", Span(line, col, line, col, i, i)))
            return toks
        sl, sc, so = line, col, i
        c = src[i]
        if c.isdigit():
            j = i
            while j < n and src[j].isdigit():
                j += 1
            kind, text = "int", src[i:j]
            adv(j - i)
        elif c == '"':
            adv(1)
            buf = []
            while True:
                if i >= n or src[i] == "\n":
                    raise Diag(Span(sl, sc, sl, sc + 1, so, so + 1), "error",
                               "this string literal is not terminated")
                d = src[i]
                if d == '"':
                    adv(1)
                    break
                if d == "\\":
                    e = src[i + 1] if i + 1 < n else ""
                    esc = {"n": "\n", "t": "\t", "\\": "\\", '"': '"'}.get(e)
                    if esc is None:
                        raise Diag(Span(line, col, line, col + 2, i, i + 2), "error",
                                   f"illegal backslash escape in string: \\{e}")
                    buf.append(esc)
                    adv(2)
                else:
                    buf.append(d)
                    adv(1)
            kind, text = "string", "".join(buf)
        elif c == "'" and i + 1 < n and ("a" <= src[i + 1] <= "z"):
            j = i + 1
            while j < n and (src[j].isalnum() or src[j] in "_'"):
                j += 1
            kind, text = "tvar", src[i + 1:j]
            adv(j - i)
        elif c.isalpha() or c == "_":
            j = i
            while j < n and (src[j].isalnum() or src[j] in "_'"):
                j += 1
            text = src[i:j]
            if text == "_":
                kind = "sym"
            elif c.isupper():
                kind = "uident"
            elif text in KEYWORDS:
                kind = "kw"
            else:
                kind = "lident"
            adv(j - i)
        else:
            text = None
            for s in SYMS2:
                if src.startswith(s, i):
                    text = s
                    break
            if text is None:
                if c in SYMS1:
                    text = c
                else:
                    raise Diag(Span(sl, sc, sl, sc + 1, so, so + 1), "error",
                               f"illegal character ({c})")
            kind = "sym"
            adv(len(text))
        toks.append(Tok(kind, text, Span(sl, sc, line, col, so, i)))


# ------------------------------------------------------------------ AST
# One node class for expressions, one for patterns, one for type
# expressions. `kind` names the form; the other fields are used as the
# form needs them.


class Node:
    def __init__(self, kind, span, **kw):
        self.kind = kind
        self.span = span
        self.name = kw.get("name", "")      # Var, Ctor, Field, Op, literal text
        self.kids = kw.get("kids", [])      # sub-expressions / sub-patterns
        self.pats = kw.get("pats", [])      # Fun params, binding patterns
        self.arms = kw.get("arms", [])      # (pat, guard or None, body)
        self.binds = kw.get("binds", [])    # Let bindings
        self.fields = kw.get("fields", [])  # (name, span, node)
        self.ty = kw.get("ty", None)        # Constraint type expression
        self.flag = kw.get("flag", False)   # let rec


class Binding:
    def __init__(self, pat, rhs, span):
        self.pat, self.rhs, self.span = pat, rhs, span


class TyExpr:
    # kind: var (name), con (name, args), arrow (args a, b), tuple (args)
    def __init__(self, kind, span, name="", args=()):
        self.kind, self.span, self.name, self.args = kind, span, name, list(args)


class TypeDecl:
    def __init__(self, name, params, span, ctors, fields, alias=None):
        self.name, self.params, self.span = name, params, span
        self.ctors = ctors      # (name, span, [TyExpr]) or None
        self.fields = fields    # (name, span, TyExpr) or None
        self.alias = alias      # TyExpr of an abbreviation, or None


class Item:
    def __init__(self, kind, span, flag=False, binds=(), decls=()):
        self.kind, self.span, self.flag = kind, span, flag
        self.binds, self.decls = list(binds), list(decls)


# ------------------------------------------------------------------ parser


class Parser:
    def __init__(self, toks):
        self.toks = toks
        self.i = 0
        self.last = toks[0].span

    def peek(self, k=0):
        return self.toks[min(self.i + k, len(self.toks) - 1)]

    def at(self, text, k=0):
        t = self.peek(k)
        return t.kind in ("sym", "kw") and t.text == text

    def next(self):
        t = self.toks[self.i]
        if t.kind != "eof":
            self.i += 1
        self.last = t.span
        return t

    def fail(self):
        t = self.peek()
        raise Diag(t.span, "error", "syntax error")

    def expect(self, text):
        if not self.at(text):
            self.fail()
        return self.next()

    def start(self):
        return self.peek().span

    def done(self, s):
        return join(s, self.last)

    # ---- items

    def program(self):
        items = []
        while True:
            while self.at(";;"):
                self.next()
            if self.peek().kind == "eof":
                return items
            if self.at("let"):
                items.append(self.let_item())
            elif self.at("type"):
                items.append(self.type_item())
            else:
                self.fail()

    def let_item(self):
        s = self.start()
        self.expect("let")
        rec = False
        if self.at("rec"):
            self.next()
            rec = True
        binds = [self.binding()]
        while self.at("and"):
            self.next()
            binds.append(self.binding())
        if self.at("in"):
            self.fail()
        return Item("let", self.done(s), flag=rec, binds=binds)

    def type_item(self):
        s = self.start()
        self.expect("type")
        decls = [self.type_decl()]
        while self.at("and"):
            self.next()
            decls.append(self.type_decl())
        return Item("type", self.done(s), decls=decls)

    def type_decl(self):
        params = []
        if self.peek().kind == "tvar":
            t = self.next()
            params.append((t.text, t.span))
        elif self.at("(") and self.peek(1).kind == "tvar":
            self.next()
            while True:
                t = self.next()
                if t.kind != "tvar":
                    self.i -= 1
                    self.fail()
                params.append((t.text, t.span))
                if self.at(","):
                    self.next()
                    continue
                self.expect(")")
                break
        t = self.peek()
        if t.kind != "lident":
            self.fail()
        self.next()
        name, span = t.text, t.span
        self.expect("=")
        if self.at("{"):
            self.next()
            fields = []
            while True:
                f = self.peek()
                if f.kind != "lident":
                    self.fail()
                self.next()
                self.expect(":")
                fields.append((f.text, f.span, self.type_expr()))
                if self.at(";"):
                    self.next()
                    if self.at("}"):
                        break
                    continue
                break
            self.expect("}")
            return TypeDecl(name, params, span, None, fields)
        if not (self.at("|") or self.peek().kind == "uident"):
            return TypeDecl(name, params, span, None, None, self.type_expr())
        ctors = []
        if self.at("|"):
            self.next()
        while True:
            c = self.peek()
            if c.kind != "uident":
                self.fail()
            self.next()
            args = []
            if self.at("of"):
                self.next()
                args.append(self.type_app())
                while self.at("*"):
                    self.next()
                    args.append(self.type_app())
            ctors.append((c.text, c.span, args))
            if self.at("|"):
                self.next()
                continue
            break
        return TypeDecl(name, params, span, ctors, None)

    # ---- type expressions: arrow < tuple < application

    def type_expr(self):
        s = self.start()
        a = self.type_tuple()
        if self.at("->"):
            self.next()
            b = self.type_expr()
            return TyExpr("arrow", self.done(s), args=[a, b])
        return a

    def type_tuple(self):
        s = self.start()
        a = self.type_app()
        if not self.at("*"):
            return a
        items = [a]
        while self.at("*"):
            self.next()
            items.append(self.type_app())
        return TyExpr("tuple", self.done(s), args=items)

    def type_app(self):
        s = self.start()
        t = self.peek()
        if t.kind == "tvar":
            self.next()
            base = TyExpr("var", t.span, name=t.text)
        elif t.kind == "lident":
            self.next()
            base = TyExpr("con", t.span, name=t.text)
        elif self.at("("):
            self.next()
            first = self.type_expr()
            if self.at(","):
                args = [first]
                while self.at(","):
                    self.next()
                    args.append(self.type_expr())
                self.expect(")")
                c = self.peek()
                if c.kind != "lident":
                    self.fail()
                self.next()
                base = TyExpr("con", self.done(s), name=c.text, args=args)
            else:
                self.expect(")")
                base = first
        else:
            self.fail()
        while self.peek().kind == "lident":
            c = self.next()
            base = TyExpr("con", self.done(s), name=c.text, args=[base])
        return base

    # ---- bindings

    def binding(self):
        s = self.start()
        t = self.peek()
        if t.kind == "lident" and self.pat_atom_start(1):
            self.next()
            name = Node("pvar", t.span, name=t.text)
            params = []
            while self.pat_atom_start(0):
                params.append(self.pat_atom())
            ann = None
            if self.at(":"):
                self.next()
                ann = self.type_expr()
            self.expect("=")
            body = self.seq()
            if ann is not None:
                body = Node("constraint", body.span, kids=[body], ty=ann)
            rhs = Node("fun", join(params[0].span, body.span), pats=params, kids=[body])
            return Binding(name, rhs, self.done(s))
        pat = self.pattern()
        if self.at(":"):
            self.next()
            ann = self.type_expr()
            pat = Node("pconstraint", self.done(s), kids=[pat], ty=ann)
        self.expect("=")
        rhs = self.seq()
        return Binding(pat, rhs, self.done(s))

    # ---- expressions

    def seq(self):
        s = self.start()
        e = self.tuple()
        if self.at(";"):
            self.next()
            rest = self.seq()
            return Node("seq", self.done(s), kids=[e, rest])
        return e

    def tuple(self):
        s = self.start()
        e = self.binop(0)
        if not self.at(","):
            return e
        items = [e]
        while self.at(","):
            self.next()
            items.append(self.binop(0))
        return Node("tuple", self.done(s), kids=items)

    LEVELS = [
        (("||",), "left"),
        (("&&",), "left"),
        (("=", "<>", "<", ">", "<=", ">="), "left"),
        (("^", "@"), "right"),
        (("::",), "right"),
        (("+", "-"), "left"),
        (("*", "/", "mod"), "left"),
    ]

    def binop(self, lvl):
        if lvl == len(self.LEVELS):
            return self.unary()
        ops, assoc = self.LEVELS[lvl]
        s = self.start()
        lhs = self.binop(lvl + 1)
        while self.peek().kind in ("sym", "kw") and self.peek().text in ops:
            op = self.next()
            if assoc == "right":
                rhs = self.binop(lvl)
            else:
                rhs = self.binop(lvl + 1)
            lhs = Node("op", self.done(s), name=op.text, kids=[lhs, rhs])
            if assoc == "right":
                break
        return lhs

    def unary(self):
        if self.at("-"):
            s = self.start()
            self.next()
            e = self.unary()
            return Node("neg", self.done(s), kids=[e])
        return self.app()

    def prefix_start(self):
        return any(self.at(k) for k in ("let", "fun", "function", "if", "match"))

    def atom_start(self):
        t = self.peek()
        if t.kind in ("int", "string", "lident", "uident"):
            return True
        return any(self.at(k) for k in ("true", "false", "(", "[", "{"))

    def app(self):
        if self.prefix_start():
            return self.prefix()
        s = self.start()
        t = self.peek()
        if t.kind == "uident" and not self.at(".", 1):
            self.next()
            if self.atom_start():
                arg = self.postfix()
                head = Node("ctor", self.done(s), name=t.text, kids=[arg])
            else:
                head = Node("ctor", t.span, name=t.text)
        else:
            head = self.postfix()
        args = []
        while self.atom_start():
            args.append(self.postfix())
        if not args:
            return head
        return Node("app", self.done(s), kids=[head] + args)

    def postfix(self):
        s = self.start()
        t = self.peek()
        if t.kind == "uident" and self.at(".", 1) and self.peek(2).kind == "lident":
            # a module path, M.x: there are no modules, so it is unbound
            self.next()
            self.next()
            x = self.next()
            e = Node("path", self.done(s), name=t.text + "." + x.text,
                     fields=[(t.text, t.span, None)])
        elif t.kind == "uident":
            # a constructor as an argument takes no argument of its own
            self.next()
            e = Node("ctor", t.span, name=t.text)
        else:
            e = self.atom()
        while self.at("."):
            self.next()
            f = self.peek()
            if f.kind != "lident":
                self.fail()
            self.next()
            e = Node("field", self.done(s), name=f.text, kids=[e],
                     fields=[(f.text, f.span, None)])
        return e

    def atom(self):
        s = self.start()
        t = self.peek()
        if t.kind == "int":
            self.next()
            return Node("int", t.span, name=t.text)
        if t.kind == "string":
            self.next()
            return Node("string", t.span, name=t.text)
        if t.kind == "lident":
            self.next()
            return Node("var", t.span, name=t.text)
        if self.at("true") or self.at("false"):
            self.next()
            return Node("bool", t.span, name=t.text)
        if self.at("("):
            self.next()
            if self.at(")"):
                self.next()
                return Node("unit", self.done(s))
            e = self.seq()
            if self.at(":"):
                self.next()
                ty = self.type_expr()
                self.expect(")")
                return Node("constraint", self.done(s), kids=[e], ty=ty)
            self.expect(")")
            return e
        if self.at("["):
            self.next()
            items = []
            if not self.at("]"):
                items.append(self.tuple())
                while self.at(";"):
                    self.next()
                    if self.at("]"):
                        break
                    items.append(self.tuple())
            self.expect("]")
            return Node("list", self.done(s), kids=items)
        if self.at("{"):
            self.next()
            base = None
            if not (self.peek().kind == "lident" and (self.at("=", 1))):
                base = self.postfix()
                self.expect("with")
            fields = []
            while True:
                f = self.peek()
                if f.kind != "lident":
                    self.fail()
                self.next()
                self.expect("=")
                fields.append((f.text, f.span, self.binop(0)))
                if self.at(";"):
                    self.next()
                    if self.at("}"):
                        break
                    continue
                break
            self.expect("}")
            if base is None:
                return Node("record", self.done(s), fields=fields)
            return Node("with", self.done(s), kids=[base], fields=fields)
        self.fail()

    def prefix(self):
        s = self.start()
        if self.at("let"):
            self.next()
            rec = False
            if self.at("rec"):
                self.next()
                rec = True
            binds = [self.binding()]
            while self.at("and"):
                self.next()
                binds.append(self.binding())
            self.expect("in")
            body = self.seq()
            return Node("let", self.done(s), binds=binds, kids=[body], flag=rec)
        if self.at("fun"):
            self.next()
            params = [self.pat_atom()]
            while self.pat_atom_start(0):
                params.append(self.pat_atom())
            self.expect("->")
            body = self.seq()
            return Node("fun", self.done(s), pats=params, kids=[body])
        if self.at("function"):
            self.next()
            arms = self.arms()
            return Node("function", self.done(s), arms=arms)
        if self.at("if"):
            self.next()
            c = self.seq()
            self.expect("then")
            a = self.tuple()
            if self.at("else"):
                self.next()
                b = self.tuple()
                return Node("if", self.done(s), kids=[c, a, b])
            return Node("if", self.done(s), kids=[c, a])
        self.expect("match")
        e = self.seq()
        self.expect("with")
        arms = self.arms()
        return Node("match", self.done(s), kids=[e], arms=arms)

    def arms(self):
        if self.at("|"):
            self.next()
        arms = []
        while True:
            p = self.pattern()
            g = None
            if self.at("when"):
                self.next()
                g = self.seq()
            self.expect("->")
            body = self.seq()
            arms.append((p, g, body))
            if self.at("|"):
                self.next()
                continue
            return arms

    # ---- patterns

    def pat_atom_start(self, k):
        t = self.peek(k)
        if t.kind in ("int", "string", "lident", "uident"):
            return True
        return any(self.at(x, k) for x in ("_", "true", "false", "(", "[", "{"))

    def pattern(self):
        s = self.start()
        p = self.pat_cons()
        if not self.at(","):
            return p
        items = [p]
        while self.at(","):
            self.next()
            items.append(self.pat_cons())
        return Node("ptuple", self.done(s), kids=items)

    def pat_cons(self):
        s = self.start()
        h = self.pat_app()
        if self.at("::"):
            self.next()
            t = self.pat_cons()
            return Node("pcons", self.done(s), kids=[h, t])
        return h

    def pat_app(self):
        s = self.start()
        t = self.peek()
        if t.kind == "uident":
            self.next()
            if self.pat_atom_start(0):
                arg = self.pat_atom()
                return Node("pctor", self.done(s), name=t.text, kids=[arg])
            return Node("pctor", t.span, name=t.text)
        if self.at("-") and self.peek(1).kind == "int":
            self.next()
            n = self.next()
            return Node("pint", self.done(s), name="-" + n.text)
        return self.pat_atom()

    def pat_atom(self):
        s = self.start()
        t = self.peek()
        if self.at("_"):
            self.next()
            return Node("pwild", t.span)
        if t.kind == "lident":
            self.next()
            return Node("pvar", t.span, name=t.text)
        if t.kind == "uident":
            self.next()
            return Node("pctor", t.span, name=t.text)
        if t.kind == "int":
            self.next()
            return Node("pint", t.span, name=t.text)
        if t.kind == "string":
            self.next()
            return Node("pstring", t.span, name=t.text)
        if self.at("true") or self.at("false"):
            self.next()
            return Node("pbool", t.span, name=t.text)
        if self.at("("):
            self.next()
            if self.at(")"):
                self.next()
                return Node("punit", self.done(s))
            p = self.pattern()
            if self.at(":"):
                self.next()
                ty = self.type_expr()
                self.expect(")")
                return Node("pconstraint", self.done(s), kids=[p], ty=ty)
            self.expect(")")
            return p
        if self.at("["):
            self.next()
            items = []
            if not self.at("]"):
                items.append(self.pat_cons())
                while self.at(";"):
                    self.next()
                    if self.at("]"):
                        break
                    items.append(self.pat_cons())
            self.expect("]")
            return Node("plist", self.done(s), kids=items)
        if self.at("{"):
            self.next()
            fields = []
            while True:
                f = self.peek()
                if f.kind != "lident":
                    self.fail()
                self.next()
                if self.at("="):
                    self.next()
                    p = self.pattern()
                else:
                    p = Node("pvar", f.span, name=f.text)
                fields.append((f.text, f.span, p))
                if self.at(";"):
                    self.next()
                    if self.at("}"):
                        break
                    continue
                break
            self.expect("}")
            return Node("precord", self.done(s), fields=fields)
        self.fail()


# ------------------------------------------------------------------ types
# An arena: each type is an index. A variable has a link (-1 when free)
# and a level; GENERIC marks a generalised variable.

GENERIC = 1 << 30
VAR, CON, ARROW, TUPLE = 0, 1, 2, 3


class Types:
    def __init__(self):
        self.kind = []
        self.name = []
        self.args = []
        self.link = []
        self.level = []

    def new(self, kind, name="", args=(), level=0):
        self.kind.append(kind)
        self.name.append(name)
        self.args.append(list(args))
        self.link.append(-1)
        self.level.append(level)
        return len(self.kind) - 1

    def repr(self, t):
        while self.kind[t] == VAR and self.link[t] >= 0:
            t = self.link[t]
        return t


# ------------------------------------------------------------------ checker

PRELUDE_VALUES = [
    ("not", "bool -> bool"),
    ("print_string", "string -> unit"),
    ("print_endline", "string -> unit"),
    ("print_int", "int -> unit"),
    ("string_of_int", "int -> string"),
    ("string_of_bool", "bool -> string"),
    ("int_of_string", "string -> int"),
    ("string_length", "string -> int"),
    ("failwith", "string -> 'a"),
    ("fst", "'a * 'b -> 'a"),
    ("snd", "'a * 'b -> 'b"),
    ("ignore", "'a -> unit"),
    ("compare", "'a -> 'a -> int"),
    ("max", "'a -> 'a -> 'a"),
    ("min", "'a -> 'a -> 'a"),
]

OP_TYPES = {
    "+": "int -> int -> int", "-": "int -> int -> int",
    "*": "int -> int -> int", "/": "int -> int -> int",
    "mod": "int -> int -> int",
    "^": "string -> string -> string",
    "@": "'a list -> 'a list -> 'a list",
    "&&": "bool -> bool -> bool", "||": "bool -> bool -> bool",
    "=": "'a -> 'a -> bool", "<>": "'a -> 'a -> bool",
    "<": "'a -> 'a -> bool", ">": "'a -> 'a -> bool",
    "<=": "'a -> 'a -> bool", ">=": "'a -> 'a -> bool",
    "::": "'a -> 'a list -> 'a list",
}


class TypeInfo:
    # kind: "abstract", "variant", "record"
    def __init__(self, name, arity, kind, uid):
        self.name, self.arity, self.kind, self.uid = name, arity, kind, uid
        self.params = []      # generic variables
        self.ctors = []       # names, in declaration order
        self.arities = []     # their argument counts
        self.fields = []      # names, in declaration order
        self.param_names = [] # an abbreviation's parameters
        self.body = None      # and its TyExpr
        self.expanding = False


class CtorInfo:
    def __init__(self, name, tinfo, index, args, result):
        self.name, self.tinfo, self.index = name, tinfo, index
        self.args, self.result = args, result


class FieldInfo:
    def __init__(self, name, tinfo, index, ty, result):
        self.name, self.tinfo, self.index = name, tinfo, index
        self.ty, self.result = ty, result


def levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[len(b)]


class Checker:
    def __init__(self, fname, src):
        self.fname = fname
        self.lines = src.split("\n")
        self.ty = Types()
        self.level = 0
        self.trail = []
        self.env = []          # (name, type, binding id)
        self.used = []         # per binding id
        self.types = {}
        self.ctors = {}
        self.fields = {}
        self.uid = 0
        self.ann_vars = {}
        self.records = []      # hover: (span, type)
        self.out = []          # transcript lines
        self.items = []        # (span, ok, records)
        self.quiet = False
        self.t_int = self.con("int")
        self.t_bool = self.con("bool")
        self.t_string = self.con("string")
        self.t_unit = self.con("unit")
        for nm, ar in (("int", 0), ("bool", 0), ("string", 0), ("unit", 0), ("list", 1)):
            self.types[nm] = self.new_typeinfo(nm, ar, "abstract")
        self.prelude_type("type 'a option = None | Some of 'a")
        for nm, s in PRELUDE_VALUES:
            self.bind(nm, self.scheme(s))
        self.op_types = {op: self.scheme(s) for op, s in OP_TYPES.items()}

    # ---- arena helpers

    def con(self, name, args=()):
        return self.ty.new(CON, name, args)

    def arrow(self, a, b):
        return self.ty.new(ARROW, "", [a, b])

    def tuple_ty(self, items):
        return self.ty.new(TUPLE, "", items)

    def var(self):
        return self.ty.new(VAR, "", (), self.level)

    def generic_var(self):
        return self.ty.new(VAR, "", (), GENERIC)

    def new_typeinfo(self, name, arity, kind):
        self.uid += 1
        return TypeInfo(name, arity, kind, self.uid)

    def scheme(self, text):
        toks = lex(text)
        p = Parser(toks)
        te = p.type_expr()
        vars_ = {}
        return self.convert(te, vars_, "scheme")

    def prelude_type(self, text):
        p = Parser(lex(text))
        item = p.type_item()
        self.declare_types(item)

    # ---- environment

    def bind(self, name, t):
        bid = len(self.used)
        self.used.append(False)
        self.env.append((name, t, bid))
        return bid

    def lookup(self, name):
        for k in range(len(self.env) - 1, -1, -1):
            nm, t, bid = self.env[k]
            if nm == name:
                self.used[bid] = True
                return t
        return None

    def suggest(self, name):
        best, bestd = None, 99
        seen = set()
        for nm, _, _ in self.env:
            if nm in seen:
                continue
            seen.add(nm)
            d = levenshtein(name, nm)
            if d <= 2 and d < len(name) and (d < bestd or d == bestd and nm < best):
                best, bestd = nm, d
        return best

    # ---- type expressions

    def convert(self, te, vars_, mode):
        """mode: "scheme" makes each 'a a generic variable; "decl" allows only
        the declaration's parameters; "ann" shares annotation variables
        across the item."""
        if te.kind == "var":
            if te.name in vars_:
                return vars_[te.name]
            if mode == "decl":
                raise Diag(te.span, "error",
                           f"the type variable '{te.name} is unbound in this type declaration")
            if mode == "scheme":
                v = self.generic_var()
            else:
                v = self.ty.new(VAR, "", (), 1)
            vars_[te.name] = v
            return v
        if te.kind == "arrow":
            a = self.convert(te.args[0], vars_, mode)
            b = self.convert(te.args[1], vars_, mode)
            return self.arrow(a, b)
        if te.kind == "tuple":
            return self.tuple_ty([self.convert(x, vars_, mode) for x in te.args])
        info = self.types.get(te.name)
        if info is None:
            raise Diag(te.span, "error", f"unbound type constructor {te.name}")
        if info.arity != len(te.args):
            raise Diag(te.span, "error",
                       f"the type constructor {te.name} expects {info.arity} argument(s), "
                       f"but is here applied to {len(te.args)} argument(s)")
        args = [self.convert(x, vars_, mode) for x in te.args]
        if info.kind == "alias":
            # an abbreviation is expanded where it is used
            if info.expanding:
                raise Diag(te.span, "error", f"the type abbreviation {te.name} is cyclic")
            info.expanding = True
            inner = dict(zip(info.param_names, args))
            try:
                return self.convert(info.body, inner, "decl")
            finally:
                info.expanding = False
        return self.con(te.name, args)

    # ---- unification

    def unify(self, a, b):
        """None on success, else ("clash", x, y) for the innermost pair that
        failed or ("occurs", var, type). A failure undoes every link."""
        mark = len(self.trail)
        r = self.unify_rec(a, b)
        if r is not None:
            while len(self.trail) > mark:
                kind, t, old = self.trail.pop()
                if kind == "link":
                    self.ty.link[t] = -1
                else:
                    self.ty.level[t] = old
        else:
            del self.trail[mark:]
        return r

    def occurs_adjust(self, v, t):
        t = self.ty.repr(t)
        if t == v:
            return True
        if self.ty.kind[t] == VAR:
            if self.ty.level[t] > self.ty.level[v]:
                self.trail.append(("level", t, self.ty.level[t]))
                self.ty.level[t] = self.ty.level[v]
            return False
        for x in self.ty.args[t]:
            if self.occurs_adjust(v, x):
                return True
        return False

    def unify_rec(self, a, b):
        a = self.ty.repr(a)
        b = self.ty.repr(b)
        if a == b:
            return None
        ka, kb = self.ty.kind[a], self.ty.kind[b]
        if ka == VAR or kb == VAR:
            v, t = (a, b) if ka == VAR else (b, a)
            if self.occurs_adjust(v, t):
                return ("occurs", v, t)
            self.trail.append(("link", v, -1))
            self.ty.link[v] = t
            return None
        if ka != kb or self.ty.name[a] != self.ty.name[b] or \
                len(self.ty.args[a]) != len(self.ty.args[b]):
            return ("clash", a, b)
        for x, y in zip(self.ty.args[a], self.ty.args[b]):
            r = self.unify_rec(x, y)
            if r is not None:
                return r
        return None

    def explain(self, r, top_a, top_b):
        if r[0] == "occurs":
            n = self.show([r[1], r[2]], prior=[top_a, top_b])
            return [f"the type variable {n[0]} occurs inside {n[1]}"]
        ra, rb = self.ty.repr(r[1]), self.ty.repr(r[2])
        if (ra, rb) in ((self.ty.repr(top_a), self.ty.repr(top_b)),
                        (self.ty.repr(top_b), self.ty.repr(top_a))):
            return []
        n = self.show([r[1], r[2]], prior=[top_a, top_b])
        return [f"type {n[0]} is not compatible with type {n[1]}"]

    def check_ty(self, span, actual, expected):
        r = self.unify(actual, expected)
        if r is not None:
            s = self.show([actual, expected])
            raise Diag(span, "error",
                       f"this expression has type {s[0]} but an expression was expected of type {s[1]}",
                       self.explain(r, actual, expected))

    def check_pat_ty(self, span, actual, expected):
        r = self.unify(actual, expected)
        if r is not None:
            s = self.show([actual, expected])
            raise Diag(span, "error",
                       f"this pattern matches values of type {s[0]} but a pattern was "
                       f"expected which matches values of type {s[1]}",
                       self.explain(r, actual, expected))

    # ---- levels

    def instantiate(self, t, mapping=None):
        if mapping is None:
            mapping = {}
        t = self.ty.repr(t)
        k = self.ty.kind[t]
        if k == VAR:
            if self.ty.level[t] != GENERIC:
                return t
            if t not in mapping:
                mapping[t] = self.var()
            return mapping[t]
        if not self.ty.args[t]:
            return t
        args = [self.instantiate(x, mapping) for x in self.ty.args[t]]
        return self.ty.new(k, self.ty.name[t], args)

    def generalize(self, t):
        t = self.ty.repr(t)
        if self.ty.kind[t] == VAR:
            if self.ty.level[t] > self.level and self.ty.level[t] != GENERIC:
                self.ty.level[t] = GENERIC
            return
        for x in self.ty.args[t]:
            self.generalize(x)

    # ---- printing

    def show(self, ts, prior=()):
        names = {}
        for t in prior:
            self.show_one(t, names)
        return [self.show_one(t, names) for t in ts]

    def show_one(self, t, names, ctx=0):
        """ctx: 0 top, 1 arrow lhs, 2 tuple item, 3 type argument."""
        t = self.ty.repr(t)
        k = self.ty.kind[t]
        if k == VAR:
            if t not in names:
                i = len(names)
                names[t] = "'" + chr(ord("a") + i % 26) + (str(i // 26) if i >= 26 else "")
            return names[t]
        if k == ARROW:
            s = self.show_one(self.ty.args[t][0], names, 1) + " -> " + \
                self.show_one(self.ty.args[t][1], names, 0)
            return f"({s})" if ctx >= 1 else s
        if k == TUPLE:
            s = " * ".join(self.show_one(x, names, 2) for x in self.ty.args[t])
            return f"({s})" if ctx >= 2 else s
        args = self.ty.args[t]
        if not args:
            return self.ty.name[t]
        if len(args) == 1:
            return self.show_one(args[0], names, 3) + " " + self.ty.name[t]
        return "(" + ", ".join(self.show_one(x, names, 0) for x in args) + ") " + self.ty.name[t]

    # ---- diagnostics

    def emit(self, d):
        tag = d.level
        self.out.append(f"{self.fname}:{d.span.sl}:{d.span.sc}-{d.span.el}:{d.span.ec}: {tag}: {d.msg}")
        line = self.lines[d.span.sl - 1] if d.span.sl - 1 < len(self.lines) else ""
        self.out.append(f"{d.span.sl:>4} | {line}")
        if d.span.el == d.span.sl:
            width = max(1, d.span.ec - d.span.sc)
        else:
            width = max(1, len(line) - d.span.sc + 1)
        self.out.append("     | " + " " * (d.span.sc - 1) + "^" * width)
        for n in d.notes:
            self.out.append("  " + n)

    def warn(self, span, num, msg, notes=()):
        self.emit(Diag(span, f"warning {num}", msg, notes))

    # ---- type declarations

    def declare_types(self, item):
        staged_types = dict(self.types)
        infos = []
        for d in item.decls:
            kind = "record" if d.fields is not None else \
                "alias" if d.alias is not None else "variant"
            info = self.new_typeinfo(d.name, len(d.params), kind)
            info.param_names = [n for n, _ in d.params]
            info.body = d.alias
            info.params = [self.generic_var() for _ in d.params]
            staged_types[d.name] = info
            infos.append(info)
        saved = self.types
        self.types = staged_types
        new_ctors, new_fields = [], []
        try:
            for d, info in zip(item.decls, infos):
                vars_ = {}
                for (pn, ps), v in zip(d.params, info.params):
                    vars_[pn] = v
                result = self.con(d.name, info.params)
                if d.alias is not None:
                    self.convert(d.alias, vars_, "decl")
                elif d.ctors is not None:
                    for idx, (cn, cs, args) in enumerate(d.ctors):
                        targs = [self.convert(a, vars_, "decl") for a in args]
                        info.ctors.append(cn)
                        info.arities.append(len(targs))
                        new_ctors.append(CtorInfo(cn, info, idx, targs, result))
                else:
                    for idx, (fn, fs, te) in enumerate(d.fields):
                        t = self.convert(te, vars_, "decl")
                        info.fields.append(fn)
                        new_fields.append(FieldInfo(fn, info, idx, t, result))
        except Diag:
            self.types = saved
            raise
        for c in new_ctors:
            self.ctors[c.name] = c
        for f in new_fields:
            self.fields[f.name] = f

    # ---- hover records

    def note(self, span, t):
        self.records.append((span, t))

    # ---- expressions

    def check(self, e, expected):
        if e.kind in ("fun", "function"):
            # the expected type reaches the parameters before the body
            self.infer_fun(e, expected)
            return
        t = self.infer(e)
        self.check_ty(e.span, t, expected)

    def infer_fun(self, e, expected):
        r = self.var()
        self.note(e.span, r)
        if e.kind == "function":
            ts, res = self.var(), self.var()
            t = self.arrow(ts, res)
            if expected is not None:
                self.check_ty(e.span, t, expected)
            self.match_arms(e, ts, res)
            self.unify(r, t)
            return r
        tps = [self.var() for _ in e.pats]
        rb = self.var()
        t = rb
        for tp in reversed(tps):
            t = self.arrow(tp, t)
        if expected is not None:
            self.check_ty(e.span, t, expected)
        mark = len(self.env)
        binds = []
        for p, tp in zip(e.pats, tps):
            self.check_pat(p, tp, binds)
        self.push_binds(binds)
        for p in e.pats:
            self.exhaustive_one(p, p.span)
        self.check(e.kids[0], rb)
        del self.env[mark:]
        self.unify(r, t)
        return r

    def infer(self, e):
        t = self.infer_inner(e)
        return t

    def infer_inner(self, e):
        k = e.kind
        if k in ("int", "string", "bool", "unit"):
            t = {"int": self.t_int, "string": self.t_string,
                 "bool": self.t_bool, "unit": self.t_unit}[k]
            self.note(e.span, t)
            return t
        if k == "var":
            s = self.lookup(e.name)
            if s is None:
                msg = f"unbound value {e.name}"
                hint = self.suggest(e.name)
                if hint is not None:
                    msg += f" (did you mean {hint}?)"
                raise Diag(e.span, "error", msg)
            t = self.instantiate(s)
            self.note(e.span, t)
            return t
        if k == "path":
            m, ms, _ = e.fields[0]
            raise Diag(ms, "error", f"unbound module {m}")
        if k == "ctor":
            r = self.var()
            self.note(e.span, r)
            c = self.ctors.get(e.name)
            if c is None:
                raise Diag(e.span, "error", f"unbound constructor {e.name}")
            items = self.ctor_args(e, c)
            mapping = {}
            res = self.instantiate(c.result, mapping)
            targs = [self.instantiate(a, mapping) for a in c.args]
            for x, ta in zip(items, targs):
                self.check(x, ta)
            self.unify(r, res)
            return r
        if k == "tuple":
            r = self.var()
            self.note(e.span, r)
            ts = [self.infer(x) for x in e.kids]
            self.unify(r, self.tuple_ty(ts))
            return r
        if k == "list":
            a = self.var()
            t = self.con("list", [a])
            self.note(e.span, t)
            for x in e.kids:
                self.check(x, a)
            return t
        if k == "op":
            r = self.var()
            self.note(e.span, r)
            ot = self.instantiate(self.op_types[e.name])
            a = self.ty.args[ot][0]
            rest = self.ty.args[ot][1]
            b = self.ty.args[rest][0]
            self.check(e.kids[0], a)
            self.check(e.kids[1], b)
            self.unify(r, self.ty.args[rest][1])
            return r
        if k == "neg":
            self.note(e.span, self.t_int)
            self.check(e.kids[0], self.t_int)
            return self.t_int
        if k == "app":
            r = self.var()
            self.note(e.span, r)
            f = e.kids[0]
            tf = self.infer(f)
            t0 = tf
            for n, arg in enumerate(e.kids[1:]):
                t = self.ty.repr(tf)
                if self.ty.kind[t] == VAR:
                    a, b = self.var(), self.var()
                    self.unify(t, self.arrow(a, b))
                    t = self.ty.repr(tf)
                if self.ty.kind[t] != ARROW:
                    s = self.show([t0])[0]
                    if n == 0:
                        raise Diag(f.span, "error",
                                   f"this expression has type {s}. This is not a function; "
                                   "it cannot be applied")
                    raise Diag(f.span, "error",
                               f"this function has type {s}. It is applied to too many arguments")
                self.check(arg, self.ty.args[t][0])
                tf = self.ty.args[t][1]
            self.unify(r, tf)
            return r
        if k in ("fun", "function"):
            return self.infer_fun(e, None)
        if k == "match":
            r = self.var()
            self.note(e.span, r)
            ts = self.infer(e.kids[0])
            res = self.var()
            self.match_arms(e, ts, res)
            self.unify(r, res)
            return r
        if k == "if":
            r = self.var()
            self.note(e.span, r)
            self.check(e.kids[0], self.t_bool)
            if len(e.kids) == 2:
                self.check(e.kids[1], self.t_unit)
                self.unify(r, self.t_unit)
                return r
            ta = self.infer(e.kids[1])
            self.check(e.kids[2], ta)
            self.unify(r, ta)
            return r
        if k == "seq":
            r = self.var()
            self.note(e.span, r)
            self.check(e.kids[0], self.t_unit)
            self.unify(r, self.infer(e.kids[1]))
            return r
        if k == "constraint":
            r = self.var()
            self.note(e.span, r)
            t = self.convert(e.ty, self.ann_vars, "ann")
            self.check(e.kids[0], t)
            self.unify(r, t)
            return r
        if k == "let":
            r = self.var()
            self.note(e.span, r)
            mark = len(self.env)
            names = self.let_bindings(e.binds, e.flag)
            tb = self.infer(e.kids[0])
            for nm, sp, bid in names:
                if not self.used[bid] and not nm.startswith("_"):
                    self.warn(sp, 26, f"unused variable {nm}")
            del self.env[mark:]
            self.unify(r, tb)
            return r
        if k == "record":
            r = self.var()
            self.note(e.span, r)
            info = self.record_fields(e)
            mapping = {}
            res = self.instantiate(self.fields[e.fields[0][0]].result, mapping)
            seen = {fn for fn, _, _ in e.fields}
            missing = [fn for fn in info.fields if fn not in seen]
            if missing:
                raise Diag(e.span, "error", "some record fields are undefined: " + " ".join(missing))
            for fn, fs, fe in e.fields:
                self.check(fe, self.instantiate(self.fields[fn].ty, mapping))
            self.unify(r, res)
            return r
        if k == "with":
            r = self.var()
            self.note(e.span, r)
            self.record_fields(e)
            mapping = {}
            res = self.instantiate(self.fields[e.fields[0][0]].result, mapping)
            self.check(e.kids[0], res)
            for fn, fs, fe in e.fields:
                self.check(fe, self.instantiate(self.fields[fn].ty, mapping))
            self.unify(r, res)
            return r
        if k == "field":
            r = self.var()
            self.note(e.span, r)
            fn, fs, _ = e.fields[0]
            f = self.fields.get(fn)
            if f is None:
                raise Diag(fs, "error", f"unbound record field {fn}")
            mapping = {}
            res = self.instantiate(f.result, mapping)
            self.check(e.kids[0], res)
            self.unify(r, self.instantiate(f.ty, mapping))
            return r
        raise AssertionError(k)

    def ctor_args(self, e, c):
        """The sub-terms a constructor applies to, checking the arity."""
        n = len(c.args)
        if not e.kids:
            got = 0
            items = []
        else:
            arg = e.kids[0]
            if n >= 2 and arg.kind in ("tuple", "ptuple"):
                items = arg.kids
                got = len(items)
            elif n >= 2 and arg.kind == "pwild":
                return [Node("pwild", arg.span) for _ in range(n)]
            else:
                items = [arg]
                got = 1
        if got != n:
            raise Diag(e.span, "error",
                       f"the constructor {c.name} expects {n} argument(s), "
                       f"but is applied here to {got} argument(s)")
        return items

    def record_fields(self, e):
        fn0, fs0, _ = e.fields[0]
        first = self.fields.get(fn0)
        if first is None:
            raise Diag(fs0, "error", f"unbound record field {fn0}")
        seen = set()
        for fn, fs, _ in e.fields:
            f = self.fields.get(fn)
            if f is None:
                raise Diag(fs, "error", f"unbound record field {fn}")
            if f.tinfo is not first.tinfo:
                raise Diag(fs, "error",
                           f"the record field {fn} belongs to the type {f.tinfo.name} "
                           f"but is mixed here with fields of type {first.tinfo.name}")
            if fn in seen:
                raise Diag(fs, "error", f"the record field {fn} is defined several times")
            seen.add(fn)
        return first.tinfo

    def push_binds(self, binds):
        out = []
        for nm, t, sp in binds:
            out.append((nm, sp, self.bind(nm, t)))
        return out

    def match_arms(self, e, ts, res):
        rows = []
        for p, g, body in e.arms:
            mark = len(self.env)
            binds = []
            self.check_pat(p, ts, binds)
            self.push_binds(binds)
            if g is not None:
                self.check(g, self.t_bool)
            self.check(body, res)
            del self.env[mark:]
            rows.append((self.simple(p), g is not None, p.span))
        self.match_warnings(rows, e.span)

    def let_bindings(self, binds, rec):
        """Binds the names of a let; returns (name, span, binding id) for the
        simple variables, for the unused-variable warning."""
        self.level += 1
        allb = []
        tps = []
        for b in binds:
            tp = self.var()
            if rec:
                p = b.pat
                if p.kind == "pconstraint":
                    p = p.kids[0]
                if p.kind != "pvar":
                    raise Diag(b.pat.span, "error",
                               "only variables are allowed as left-hand side of let rec")
                rhs = b.rhs
                if rhs.kind == "constraint":
                    rhs = rhs.kids[0]
                if rhs.kind not in ("fun", "function"):
                    raise Diag(b.rhs.span, "error",
                               "this kind of expression is not allowed as right-hand side of let rec")
            self.check_pat(b.pat, tp, allb)
            tps.append(tp)
        if rec:
            mark = len(self.env)
            self.push_binds(allb)
            for b, tp in zip(binds, tps):
                self.check(b.rhs, tp)
            del self.env[mark:]
        else:
            for b, tp in zip(binds, tps):
                self.check(b.rhs, tp)
        self.level -= 1
        for nm, t, sp in allb:
            self.generalize(t)
        for b in binds:
            if b.pat.kind != "pvar":
                self.exhaustive_one(b.pat, b.pat.span)
        ids = self.push_binds(allb)
        simple = [b.pat.name for b in binds if b.pat.kind == "pvar"]
        return [x for x in ids if x[0] in simple]

    # ---- patterns

    def check_pat(self, p, expected, binds):
        k = p.kind
        self.note(p.span, expected)
        if k == "pwild":
            return
        if k == "pvar":
            for nm, _, _ in binds:
                if nm == p.name:
                    raise Diag(p.span, "error",
                               f"variable {p.name} is bound several times in this matching")
            binds.append((p.name, expected, p.span))
            return
        if k in ("pint", "pstring", "pbool", "punit"):
            t = {"pint": self.t_int, "pstring": self.t_string,
                 "pbool": self.t_bool, "punit": self.t_unit}[k]
            self.check_pat_ty(p.span, t, expected)
            return
        if k == "ptuple":
            vs = [self.var() for _ in p.kids]
            self.check_pat_ty(p.span, self.tuple_ty(vs), expected)
            for x, v in zip(p.kids, vs):
                self.check_pat(x, v, binds)
            return
        if k in ("pcons", "plist"):
            a = self.var()
            lt = self.con("list", [a])
            self.check_pat_ty(p.span, lt, expected)
            if k == "pcons":
                self.check_pat(p.kids[0], a, binds)
                self.check_pat(p.kids[1], lt, binds)
            else:
                for x in p.kids:
                    self.check_pat(x, a, binds)
            return
        if k == "pctor":
            c = self.ctors.get(p.name)
            if c is None:
                raise Diag(p.span, "error", f"unbound constructor {p.name}")
            items = self.ctor_args(p, c)
            mapping = {}
            res = self.instantiate(c.result, mapping)
            targs = [self.instantiate(a, mapping) for a in c.args]
            self.check_pat_ty(p.span, res, expected)
            for x, ta in zip(items, targs):
                self.check_pat(x, ta, binds)
            return
        if k == "precord":
            self.record_fields(p)
            mapping = {}
            res = self.instantiate(self.fields[p.fields[0][0]].result, mapping)
            self.check_pat_ty(p.span, res, expected)
            for fn, fs, fp in p.fields:
                self.check_pat(fp, self.instantiate(self.fields[fn].ty, mapping), binds)
            return
        if k == "pconstraint":
            t = self.convert(p.ty, self.ann_vars, "ann")
            self.check_pat_ty(p.span, t, expected)
            self.check_pat(p.kids[0], t, binds)
            return
        raise AssertionError(k)

    # ---- the match warnings (Maranget, "Warnings for pattern matching")
    # A simple pattern is None (a wildcard) or (family, tag, args). A family
    # is ("variant", TypeInfo), ("bool",), ("unit",), ("list",),
    # ("tuple", n), ("record", TypeInfo), ("int",) or ("string",); a tag is
    # a constructor index, or the literal for int and string.

    def simple(self, p):
        k = p.kind
        if k in ("pwild", "pvar"):
            return None
        if k == "pconstraint":
            return self.simple(p.kids[0])
        if k == "pint":
            return (("int",), int(p.name), [])
        if k == "pstring":
            return (("string",), p.name, [])
        if k == "pbool":
            return (("bool",), 1 if p.name == "true" else 0, [])
        if k == "punit":
            return (("unit",), 0, [])
        if k == "ptuple":
            return (("tuple", len(p.kids)), 0, [self.simple(x) for x in p.kids])
        if k == "pcons":
            return (("list",), 1, [self.simple(p.kids[0]), self.simple(p.kids[1])])
        if k == "plist":
            r = (("list",), 0, [])
            for x in reversed(p.kids):
                r = (("list",), 1, [self.simple(x), r])
            return r
        if k == "pctor":
            c = self.ctors[p.name]
            items = self.ctor_args(p, c)
            return (("variant", c.tinfo), c.index, [self.simple(x) for x in items])
        if k == "precord":
            info = self.fields[p.fields[0][0]].tinfo
            args = [None] * len(info.fields)
            for fn, fs, fp in p.fields:
                args[self.fields[fn].index] = self.simple(fp)
            return (("record", info), 0, args)
        raise AssertionError(k)

    def signature(self, fam):
        """The constructors of a finite family as (tag, arity), or None."""
        kind = fam[0]
        if kind == "variant":
            return list(enumerate(fam[1].arities))
        if kind == "bool":
            return [(0, 0), (1, 0)]
        if kind == "unit":
            return [(0, 0)]
        if kind == "list":
            return [(0, 0), (1, 2)]
        if kind == "tuple":
            return [(0, fam[1])]
        if kind == "record":
            return [(0, len(fam[1].fields))]
        return None

    def specialize(self, rows, fam, tag, arity):
        out = []
        for r in rows:
            h = r[0]
            if h is None:
                out.append([None] * arity + r[1:])
            elif h[1] == tag:
                out.append(list(h[2]) + r[1:])
        return out

    def default(self, rows):
        return [r[1:] for r in rows if r[0] is None]

    def heads(self, rows):
        fam = None
        tags = []
        for r in rows:
            h = r[0]
            if h is not None:
                fam = h[0]
                if h[1] not in tags:
                    tags.append(h[1])
        return fam, tags

    def missing(self, rows, n):
        if n == 0:
            return None if rows else []
        fam, tags = self.heads(rows)
        sig = self.signature(fam) if fam is not None else None
        if sig is not None and len(tags) == len(sig):
            for tag, ar in sig:
                w = self.missing(self.specialize(rows, fam, tag, ar), ar + n - 1)
                if w is not None:
                    return [(fam, tag, w[:ar])] + w[ar:]
            return None
        w = self.missing(self.default(rows), n - 1)
        if w is None:
            return None
        if fam is None:
            return [None] + w
        if sig is not None:
            for tag, ar in sig:
                if tag not in tags:
                    return [(fam, tag, [None] * ar)] + w
        if fam[0] == "int":
            v = 0
            while v in tags:
                v += 1
            return [(fam, v, [])] + w
        for cand in [""] + [chr(c) for c in range(ord("a"), ord("z") + 1)]:
            if cand not in tags:
                return [(fam, cand, [])] + w
        return [None] + w

    def useful(self, rows, q):
        if not q:
            return not rows
        h = q[0]
        if h is not None:
            return self.useful(self.specialize(rows, h[0], h[1], len(h[2])), list(h[2]) + q[1:])
        fam, tags = self.heads(rows)
        sig = self.signature(fam) if fam is not None else None
        if sig is not None and len(tags) == len(sig):
            for tag, ar in sig:
                if self.useful(self.specialize(rows, fam, tag, ar), [None] * ar + q[1:]):
                    return True
            return False
        return self.useful(self.default(rows), q[1:])

    def show_pat(self, p, ctx=0):
        """ctx: 0 top, 1 constructor argument or cons head."""
        if p is None:
            return "_"
        fam, tag, args = p
        kind = fam[0]
        if kind == "int":
            return str(tag)
        if kind == "string":
            return '"' + tag + '"'
        if kind == "bool":
            return "true" if tag == 1 else "false"
        if kind == "unit":
            return "()"
        if kind == "tuple":
            return "(" + ", ".join(self.show_pat(a) for a in args) + ")"
        if kind == "list":
            if tag == 0:
                return "[]"
            s = self.show_pat(args[0], 1) + " :: " + self.show_pat(args[1])
            return f"({s})" if ctx >= 1 else s
        if kind == "record":
            info = fam[1]
            return "{" + "; ".join(f"{fn} = {self.show_pat(a)}"
                                   for fn, a in zip(info.fields, args)) + "}"
        name = fam[1].ctors[tag]
        if not args:
            return name
        if len(args) == 1:
            s = name + " " + self.show_pat(args[0], 1)
        else:
            s = name + " (" + ", ".join(self.show_pat(a) for a in args) + ")"
        return f"({s})" if ctx >= 1 else s

    def match_warnings(self, rows, span):
        matrix = [[sp] for sp, guarded, _ in rows if not guarded]
        w = self.missing(matrix, 1)
        if w is not None:
            self.warn(span, 8, "this pattern-matching is not exhaustive",
                      ["here is an example of a case that is not matched: " + self.show_pat(w[0])])
        prev = []
        for sp, guarded, pspan in rows:
            if not self.useful(prev, [sp]):
                self.warn(pspan, 11, "this match case is unused")
            if not guarded:
                prev.append([sp])

    def exhaustive_one(self, p, span):
        w = self.missing([[self.simple(p)]], 1)
        if w is not None:
            self.warn(span, 8, "this pattern-matching is not exhaustive",
                      ["here is an example of a case that is not matched: " + self.show_pat(w[0])])

    # ---- items

    def run(self, items):
        for item in items:
            self.records = []
            self.ann_vars = {}
            mark = len(self.env)
            ok = True
            try:
                if item.kind == "type":
                    self.declare_types(item)
                    for d in item.decls:
                        ps = [f"'{n}" for n, _ in d.params]
                        if len(ps) == 1:
                            pre = ps[0] + " "
                        elif ps:
                            pre = "(" + ", ".join(ps) + ") "
                        else:
                            pre = ""
                        self.out.append(f"type {pre}{d.name}")
                else:
                    self.level = 0
                    names = self.top_let(item)
                    for nm, t in names:
                        self.out.append(f"val {nm} : {self.show([t])[0]}")
            except Diag as d:
                ok = False
                self.emit(d)
                self.level = 0
                del self.env[mark:]
                if item.kind == "let":
                    for nm in self.pat_names(item):
                        self.bind(nm, self.generic_var())
            self.items.append((item.span, ok, self.records))

    def top_let(self, item):
        mark = len(self.env)
        self.let_bindings(item.binds, item.flag)
        out = []
        for name, t, bid in self.env[mark:]:
            out.append((name, t))
        return out

    def pat_names(self, item):
        names = []

        def walk(p):
            if p.kind == "pvar":
                names.append(p.name)
            for x in p.kids:
                walk(x)
            for _, _, fp in p.fields:
                walk(fp)
        for b in item.binds:
            walk(b.pat)
        return names

    def hover(self, line, col):
        for span, ok, recs in self.items:
            if not inside(span, line, col):
                continue
            if not ok:
                return f"{line}:{col}: no type (this item has an error)"
            best = None
            for sp, t in recs:
                if inside(sp, line, col) and (best is None or sp.eo - sp.so < best[0].eo - best[0].so):
                    best = (sp, t)
            if best is None:
                break
            sp, t = best
            return f"{sp.sl}:{sp.sc}-{sp.el}:{sp.ec}: {self.show([t])[0]}"
        return f"{line}:{col}: nothing here"


def inside(sp, line, col):
    return (sp.sl, sp.sc) <= (line, col) < (sp.el, sp.ec)


# ------------------------------------------------------------------ driver


def analyse(fname, src):
    c = Checker(fname, src)
    try:
        items = Parser(lex(src)).program()
    except Diag as d:
        c.emit(d)
        return c, False
    c.run(items)
    return c, True


def unescape(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append({"n": "\n", "t": "\t", "\\": "\\"}.get(s[i + 1], s[i + 1]))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def job(line):
    out = [f"$ {line}"]
    words = line.split(" ")
    mode = words[0]
    if mode == "snip":
        src = unescape(line[len("snip "):])
        c, _ = analyse("snip.ml", src)
        out += c.out
    elif mode == "check":
        with open(os.path.join("data", words[1]), encoding="utf-8") as fh:
            src = fh.read()
        c, _ = analyse(words[1], src)
        out += c.out
    elif mode == "hover":
        with open(os.path.join("data", words[1]), encoding="utf-8") as fh:
            src = fh.read()
        c, parsed = analyse(words[1], src)
        for pos in words[2:]:
            l, col = pos.split(":")
            if not parsed:
                out.append(f"{pos}: no type (the file does not parse)")
            else:
                out.append(c.hover(int(l), int(col)))
    else:
        out.append(f"unknown job {mode}")
    return "\n".join(out) + "\n"


def main():
    with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as fh:
        jobs = [l.rstrip("\r") for l in fh.read().split("\n") if l.strip()]
    sys.stdout.write("".join(job(j) for j in jobs))


if __name__ == "__main__":
    main()
