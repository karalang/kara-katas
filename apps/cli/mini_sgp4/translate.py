#!/usr/bin/env python3
"""Translates the numeric core of the vendored sgp4/propagation.py (_dpper,
_dscom, _dsinit, _dspace, _initl, sgp4init, sgp4, gstime) into Kara and splices
it into mini_sgp4.kara between the BEGIN/END markers. The translation is
statement for statement and keeps Python's evaluation order:

- every local is declared once at the top of its function (Python scoping);
  a parameter the body reassigns is copied into a local of the same name;
- a function returning a tuple returns a struct named <Fn>Out instead, and a
  tuple assignment from it unpacks the struct field by field;
- `a % b` is pmod() (Python's sign rule) and `a // b` is floordiv();
- an int mixed into float arithmetic is converted, as Python converts it;
- math.sin & co. become f64 methods, `pow` is f64.pow (both are C pow()).

The handful of statements with no numeric meaning (the gravity-model unpack,
the isinstance() test, the `error_message` strings) have fixed translations
below. The satellite record (struct Sat) is generated from Satrec.__slots__ in
model.py; getgravconst and everything outside propagation.py is written by
hand.
Run: python3 -I -B translate.py"""
import ast
import sys

SRC = "vendor/sgp4/propagation.py"
KARA = "mini_sgp4.kara"
BEGIN = "// BEGIN translated from vendor/sgp4/propagation.py by translate.py\n"
END = "// END translated\n"

FUNCS = ["_dpper", "_dscom", "_dsinit", "_dspace", "_initl", "sgp4init", "sgp4", "gstime"]

# Satellite-record fields that are not f64.
SAT_INT = {"irez", "isimp", "error", "epochyr", "ephtype", "elnum", "revnum"}
SAT_STR = {"method", "init", "operationmode", "satnum_str", "classification", "error_message",
           "intldesg"}
# What the port keeps beside Satrec's __slots__: which API built the record
# (the 1.x Satellite keeps ephtype and revnum as text and has an epoch
# datetime), and whether a TLE filled in the TLE-only attributes.
EXTRA = [("legacy", "bool", "false"), ("has_tle", "bool", "false"),
         ("ephtype_s", "String", '"".to_string()'), ("revnum_s", "String", '"".to_string()'),
         ("epoch_repr", "String", '"".to_string()')]
FIELD_RENAME = {"Om": "big_om"}

STR_PARAMS = {"init", "method", "opsmode", "satn"}
INT_PARAMS = {"irez"}
GLOBALS = {"pi": "PI", "twopi": "TWOPI", "deg2rad": "DEG2RAD"}
MATH1 = {"sin": "sin", "cos": "cos", "sqrt": "sqrt", "fabs": "abs"}


def die(node, msg):
    sys.exit("translate.py: line %d: %s: %s" % (node.lineno, msg, ast.unparse(node)))


class Fn:
    def __init__(self, node):
        self.node = node
        self.name = node.name.lstrip("_")
        self.params = [a.arg for a in node.args.args]
        self.types = {}          # name -> "f" | "i" | "s" | "t3"
        self.assigned = set()
        self.ret = None          # list of (field, type) for a struct return
        self.ret_kind = None     # "struct", "scalar", "rv", "none"


def ptype(fn, p):
    if p == "satrec":
        return "sat"
    if p == "whichconst":
        return "grav"
    if p in STR_PARAMS:
        return "s"
    if p in INT_PARAMS:
        return "i"
    return "f"


def field_type(attr):
    if attr in SAT_INT:
        return "i"
    if attr in SAT_STR:
        return "s"
    return "f"


class Translator:
    def __init__(self, tree):
        self.fns = {}
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in FUNCS:
                self.fns[node.name] = Fn(node)
        self.tmp = 0

    # ---------------------------------------------------------------- types
    def etype(self, fn, e):
        if isinstance(e, ast.Constant):
            if isinstance(e.value, bool):
                return "b"
            if isinstance(e.value, int):
                return "i"
            if isinstance(e.value, float):
                return "f"
            if isinstance(e.value, str):
                return "s"
            if e.value is None:
                return "s"
        if isinstance(e, ast.Name):
            if e.id in fn.types:
                return fn.types[e.id]
            if e.id in GLOBALS:
                return "f"
            if e.id == "false":
                return "t3"
            return None
        if isinstance(e, ast.Attribute):
            return field_type(e.attr)
        if isinstance(e, ast.BinOp):
            a, b = self.etype(fn, e.left), self.etype(fn, e.right)
            if a is None or b is None:
                return None
            if isinstance(e.op, ast.Div) or "f" in (a, b):
                return "f"
            return "i"
        if isinstance(e, ast.UnaryOp):
            return self.etype(fn, e.operand)
        if isinstance(e, ast.IfExp):
            a, b = self.etype(fn, e.body), self.etype(fn, e.orelse)
            return "f" if "f" in (a, b) else a
        if isinstance(e, ast.Call):
            f = ast.unparse(e.func)
            if f in MATH1 or f in ("atan2", "pow", "_gstime"):
                return "f"
            if f.endswith(".format"):
                return "s"
            return None
        if isinstance(e, ast.Tuple):
            return "t3"
        if isinstance(e, (ast.Compare, ast.BoolOp)):
            return "b"
        die(e, "no type rule")

    def infer(self, fn):
        for p in fn.params:
            fn.types[p] = ptype(fn, p)
        stmts = list(ast.walk(fn.node))
        for _ in range(8):
            for s in stmts:
                if isinstance(s, ast.Assign):
                    tgt = s.targets[0]
                    if isinstance(tgt, ast.Tuple) and isinstance(s.value, ast.Call):
                        callee = self.fns[s.value.func.id]
                        for t, (_, ty) in zip(tgt.elts, callee.ret):
                            if isinstance(t, ast.Name):
                                self.note(fn, t.id, ty)
                    elif isinstance(tgt, ast.Name):
                        self.note(fn, tgt.id, self.etype(fn, s.value))
                elif isinstance(s, ast.AugAssign) and isinstance(s.target, ast.Name):
                    self.note(fn, s.target.id, self.etype(fn, s.value))
                elif isinstance(s, ast.For):
                    self.note(fn, s.target.id, "i")
        for s in stmts:
            if isinstance(s, (ast.Assign, ast.AugAssign, ast.For)):
                tgts = s.targets if isinstance(s, ast.Assign) else [s.target]
                for t in tgts:
                    for n in (t.elts if isinstance(t, ast.Tuple) else [t]):
                        if isinstance(n, ast.Name):
                            fn.assigned.add(n.id)
        fn.assigned.discard("satn")  # only in the isinstance() branch
        # what the function returns
        rets = [s for s in stmts if isinstance(s, ast.Return)]
        last = rets[-1].value if rets else None
        if fn.name == "sgp4":
            fn.ret_kind = "rv"
        elif fn.name == "sgp4init":
            fn.ret_kind = "none"
        elif isinstance(last, ast.Tuple):
            fn.ret_kind = "struct"
            fn.ret = [(n.id, fn.types[n.id]) for n in last.elts]
        else:
            fn.ret_kind = "scalar"

    def note(self, fn, name, ty):
        if ty is None:
            return
        old = fn.types.get(name)
        if old is None or (old == "i" and ty == "f"):
            fn.types[name] = ty
        elif old != ty and not (old == "f" and ty == "i"):
            sys.exit("translate.py: %s: %s is both %s and %s" % (fn.name, name, old, ty))

    # ----------------------------------------------------------- emission
    def kty(self, ty):
        return {"f": "f64", "i": "i64", "s": "String", "t3": "(f64, f64, f64)"}[ty]

    def default(self, ty):
        return {"f": "0.0", "i": "0", "s": '"".to_string()', "t3": "nan3()"}[ty]

    def lit(self, v, want):
        if isinstance(v, float) or want == "f":
            r = repr(float(v))
            return r
        return str(v)

    def ex(self, fn, e, want=None):
        """Kara text for expression e; want="f" converts an int to f64."""
        ty = self.etype(fn, e)
        if isinstance(e, ast.Constant):
            if isinstance(e.value, str):
                return '"%s".to_string()' % e.value
            if e.value is None:
                return '"".to_string()'
            return self.lit(e.value, want)
        if isinstance(e, ast.Name):
            if e.id in fn.types:
                txt = e.id
            elif e.id in GLOBALS:
                txt = GLOBALS[e.id]
            elif e.id == "false":
                txt = "nan3()"
            else:
                die(e, "unknown name")
            if want == "f" and ty == "i":
                return "(%s as f64)" % txt
            return txt
        if isinstance(e, ast.Attribute):
            if not (isinstance(e.value, ast.Name) and e.value.id in ("satrec", "whichconst")):
                die(e, "attribute")
            txt = "%s.%s" % (e.value.id, FIELD_RENAME.get(e.attr, e.attr))
            if want == "f" and ty == "i":
                return "(%s as f64)" % txt
            return txt
        if isinstance(e, ast.BinOp):
            w = "f" if ty == "f" else None
            a = self.ex(fn, e.left, w)
            b = self.ex(fn, e.right, w)
            if isinstance(e.op, ast.Mod):
                return "pmod(%s, %s)" % (a, b)
            if isinstance(e.op, ast.FloorDiv):
                return "floordiv(%s, %s)" % (a, b)
            op = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}.get(type(e.op))
            if op is None:
                die(e, "operator")
            if isinstance(e.left, (ast.BinOp, ast.UnaryOp)) and not a.startswith("pmod("):
                a = "(%s)" % a
            if isinstance(e.right, (ast.BinOp, ast.UnaryOp)) and not b.startswith("pmod("):
                b = "(%s)" % b
            return "%s %s %s" % (a, op, b)
        if isinstance(e, ast.UnaryOp):
            if not isinstance(e.op, ast.USub):
                die(e, "unary")
            inner = self.ex(fn, e.operand, want)
            if isinstance(e.operand, (ast.Name, ast.Constant, ast.Attribute, ast.Call)):
                return "-%s" % inner
            return "-(%s)" % inner
        if isinstance(e, ast.Compare):
            if len(e.ops) != 1:
                # a < b < c is (a < b) and (b < c); b is a plain value here.
                left = e.left
                parts = []
                for op, right in zip(e.ops, e.comparators):
                    parts.append(ast.Compare(left=left, ops=[op], comparators=[right]))
                    left = right
                return self.ex(fn, ast.BoolOp(op=ast.And(), values=parts))
            lt, rt = self.etype(fn, e.left), self.etype(fn, e.comparators[0])
            w = "f" if "f" in (lt, rt) else None
            op = {ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=",
                  ast.Eq: "==", ast.NotEq: "!="}[type(e.ops[0])]
            a = self.ex(fn, e.left, w)
            b = self.ex(fn, e.comparators[0], w)
            if lt == "s" or rt == "s":
                b = '"%s"' % e.comparators[0].value
            return "%s %s %s" % (a, op, b)
        if isinstance(e, ast.BoolOp):
            op = " and " if isinstance(e.op, ast.And) else " or "
            return op.join("(%s)" % self.ex(fn, v) for v in e.values)
        if isinstance(e, ast.IfExp):
            w = "f" if ty == "f" else None
            return "if %s { %s } else { %s }" % (self.ex(fn, e.test), self.ex(fn, e.body, w),
                                                self.ex(fn, e.orelse, w))
        if isinstance(e, ast.Call):
            f = ast.unparse(e.func)
            args = e.args
            if f in MATH1:
                return "%s.%s()" % (self.recv(fn, args[0]), MATH1[f])
            if f == "atan2":
                return "%s.atan2(%s)" % (self.recv(fn, args[0]), self.ex(fn, args[1], "f"))
            if f == "pow":
                return "%s.pow(%s)" % (self.recv(fn, args[0]), self.ex(fn, args[1], "f"))
            if f.endswith(".format"):
                fmt = e.func.value.value
                head, tail = fmt.split("{0:f}")
                return 'f"%s{ffmt(%s)}%s"' % (head, self.ex(fn, args[0]), tail)
            if f == "_gstime":
                f = "gstime"
            name = f.lstrip("_")
            if f in self.fns:
                callee = self.fns[f]
                out = []
                for p, a in zip(callee.params, args):
                    pt = ptype(callee, p)
                    if pt in ("sat", "grav", "s"):
                        out.append(self.ex(fn, a))
                    else:
                        out.append(self.ex(fn, a, "f" if pt == "f" else None))
                return "%s(%s)" % (name, ", ".join(out))
            die(e, "call")
        if isinstance(e, ast.Tuple):
            return "(%s)" % ", ".join(self.ex(fn, x, "f") for x in e.elts)
        die(e, "expression")

    def recv(self, fn, e):
        t = self.ex(fn, e, "f")
        if isinstance(e, (ast.Name, ast.Attribute)) and " as " not in t:
            return t
        return "(%s)" % t

    def target(self, fn, t):
        if isinstance(t, ast.Name):
            return t.id
        if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == "satrec":
            return "satrec.%s" % FIELD_RENAME.get(t.attr, t.attr)
        die(t, "target")

    def ttype(self, fn, t):
        if isinstance(t, ast.Name):
            return fn.types[t.id]
        return field_type(t.attr)

    def stmt(self, fn, s, ind):
        p = "    " * ind
        out = []
        src = ast.unparse(s)
        if isinstance(s, ast.Expr):
            if isinstance(s.value, ast.Constant):
                return []
            if isinstance(s.value, ast.Call) and ast.unparse(s.value.func) == "sgp4":
                return [p + "let _ = sgp4(mut satrec, 0.0);"]
            die(s, "expression statement")
        if isinstance(s, ast.If) and src.startswith("if isinstance(satn, int)"):
            return [p + "// isinstance(satn, int): the caller passes satn as text already"]
        if isinstance(s, ast.Assign):
            tgt = s.targets[0]
            if isinstance(tgt, ast.Tuple) and isinstance(s.value, ast.Name) and s.value.id == "whichconst":
                for t in tgt.elts:
                    out.append(p + "satrec.%s = whichconst.%s;" % (t.attr, t.attr))
                return out
            if isinstance(tgt, ast.Tuple):
                callee = self.fns[s.value.func.id]
                self.tmp += 1
                v = "o%d" % self.tmp
                out.append(p + "let %s = %s;" % (v, self.ex(fn, s.value)))
                for t, (field, _) in zip(tgt.elts, callee.ret):
                    out.append(p + "%s = %s.%s;" % (self.target(fn, t), v, field))
                return out
            ty = self.ttype(fn, tgt)
            val = self.ex(fn, s.value, "f" if ty == "f" else None)
            if ty == "s" and isinstance(s.value, ast.Name):
                val += ".clone()"
            out.append(p + "%s = %s;" % (self.target(fn, tgt), val))
            return out
        if isinstance(s, ast.AugAssign):
            t = self.target(fn, s.target)
            fake = ast.BinOp(left=s.target, op=s.op, right=s.value)
            ast.copy_location(fake, s)
            fake.left = ast.Name(id=s.target.id, ctx=ast.Load()) if isinstance(s.target, ast.Name) else s.target
            ty = self.ttype(fn, s.target)
            return [p + "%s = %s;" % (t, self.ex(fn, fake, "f" if ty == "f" else None))]
        if isinstance(s, ast.If):
            out.append(p + "if %s {" % self.ex(fn, s.test))
            for b in s.body:
                out += self.stmt(fn, b, ind + 1)
            orelse = s.orelse
            while len(orelse) == 1 and isinstance(orelse[0], ast.If):
                s2 = orelse[0]
                out.append(p + "} else if %s {" % self.ex(fn, s2.test))
                for b in s2.body:
                    out += self.stmt(fn, b, ind + 1)
                orelse = s2.orelse
            if orelse:
                out.append(p + "} else {")
                for b in orelse:
                    out += self.stmt(fn, b, ind + 1)
            out.append(p + "}")
            return out
        if isinstance(s, ast.While):
            out.append(p + "while %s {" % self.ex(fn, s.test))
            for b in s.body:
                out += self.stmt(fn, b, ind + 1)
            out.append(p + "}")
            return out
        if isinstance(s, ast.For):
            vals = ", ".join(str(c.value) for c in s.iter.elts)
            out.append(p + "for %s_v in [%s] {" % (s.target.id, vals))
            out.append(p + "    %s = %s_v;" % (s.target.id, s.target.id))
            for b in s.body:
                out += self.stmt(fn, b, ind + 1)
            out.append(p + "}")
            return out
        if isinstance(s, ast.Return):
            if fn.ret_kind == "none":
                return []
            if fn.ret_kind == "struct":
                fields = ", ".join("%s: %s" % (f, f) for f, _ in fn.ret)
                return [p + "return %sOut { %s };" % (self.sname(fn), fields)]
            return [p + "return %s;" % self.ex(fn, s.value, "f")]
        die(s, "statement")

    def sname(self, fn):
        return fn.name[0].upper() + fn.name[1:]

    def function(self, fn):
        out = []
        if fn.ret_kind == "struct":
            out.append("struct %sOut {" % self.sname(fn))
            for f, ty in fn.ret:
                out.append("    %s: %s," % (f, self.kty(ty)))
            out.append("}")
            out.append("")
        params = []
        for prm in fn.params:
            pt = ptype(fn, prm)
            if pt == "grav" and fn.name == "sgp4":
                continue
            nm = "p_" + prm if (prm in fn.assigned) else prm
            if pt == "sat":
                params.append("%s: %s Sat" % (nm, "ref" if fn.name == "dpper" else "mut ref"))
            elif pt == "grav":
                params.append("%s: ref Grav" % nm)
            elif pt == "s":
                params.append("%s: ref String" % nm)
            else:
                params.append("%s: %s" % (nm, self.kty(pt)))
        ret = {"struct": " -> %sOut" % self.sname(fn), "scalar": " -> f64",
               "rv": " -> ((f64, f64, f64), (f64, f64, f64))", "none": ""}[fn.ret_kind]
        out.append("fn %s(%s)%s {" % (fn.name, ", ".join(params), ret))
        for prm in fn.params:
            if prm in fn.assigned:
                pt = ptype(fn, prm)
                cl = ".clone()" if pt == "s" else ""
                out.append("    let mut %s = p_%s%s;" % (prm, prm, cl))
        for name in sorted(fn.types):
            if name in fn.params:
                continue
            out.append("    let mut %s: %s = %s;" % (name, self.kty(fn.types[name]),
                                                    self.default(fn.types[name])))
        for s in fn.node.body:
            out += self.stmt(fn, s, 1)
        out.append("}")
        return "\n".join(out) + "\n"

    def run(self):
        text = []
        for name in FUNCS:
            self.infer(self.fns[name])
        for name in FUNCS:
            text.append(self.function(self.fns[name]))
        return "\n".join(text)


def record():
    """struct Sat, new_sat() and full_attrs(), from Satrec.__slots__ in model.py."""
    with open("vendor/sgp4/model.py", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    slots = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and ast.unparse(node.targets[0]) == "__slots__" and \
                isinstance(node.value, ast.Tuple) and len(node.value.elts) > 10:
            slots = [e.value for e in node.value.elts]
    out = ["struct Sat {"]
    init = ["fn new_sat() -> Sat {", "    Sat {"]
    attrs = ["// The float attributes in __slots__ order, as oracle.py prints them.",
             "fn full_attrs(s: ref Sat, items: mut ref Vec[String]) {"]
    for a in slots:
        if a == "epoch":
            continue
        ty = field_type(a)
        k = {"f": "f64", "i": "i64", "s": "String"}[ty]
        f = FIELD_RENAME.get(a, a)
        out.append("    %s: %s," % (f, k))
        init.append("        %s: %s," % (f, {"f": "0.0", "i": "0", "s": '"".to_string()'}[ty]))
        if ty == "f":
            attrs.append('    items.push(f"%s={fmt(s.%s)}");' % (a, f))
    for f, k, v in EXTRA:
        out.append("    %s: %s," % (f, k))
        init.append("        %s: %s," % (f, v))
    out.append("}")
    init += ["    }", "}"]
    attrs.append("}")
    return "\n".join(out + [""] + init + [""] + attrs) + "\n"


def main():
    with open(SRC, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    body = record() + "\n" + Translator(tree).run()
    with open(KARA, encoding="utf-8") as fh:
        src = fh.read()
    a = src.index(BEGIN) + len(BEGIN)
    b = src.index(END)
    src = src[:a] + "\n" + body + "\n" + src[b:]
    with open(KARA, "w", encoding="utf-8") as fh:
        fh.write(src)


main()
