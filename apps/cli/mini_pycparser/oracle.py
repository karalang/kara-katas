"""The oracle: runs data/jobs.txt on pycparser 3.0 and prints what
mini_pycparser.kara must print.

  toks <file>          the tokens the parser read, as the lexer classified
                       them (TYPEID for a typedef name in scope)
  show <file>          FileAST.show()
  showx <file>         show(attrnames=True, nodenames=True, showcoord=True)
  repr <file>          repr(FileAST)
  gen <file>           CGenerator().visit(ast)
  genr <file>          CGenerator(reduce_parentheses=True).visit(ast)
  funcs <file>         each function definition and where (func_defs.py)
  calls <file> <name>  each call of <name> and where (func_calls.py)
  explain <file>       each file-scope declaration in words, after cdecl.py
  stats <file>         how many nodes of each kind, by kind name
  round <file>         gen, parse that, gen again: the same text?
  snip <mode> <C>      one of the modes above on the rest of the line, with
                       {NL} and {TAB} standing for a newline and a tab

Each job prints `$ <job>`, its output, and `! <Exception>: <message>` when
the parse fails.

Needs pycparser 3.0.
Run: python3 -I -B oracle.py > expected.out"""
import io
import os
import sys

from pycparser import c_ast, c_generator, c_parser

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def gen(ast, reduce=False):
    return c_generator.CGenerator(reduce_parentheses=reduce).visit(ast)


def ex_param(p):
    if isinstance(p, c_ast.EllipsisParam):
        return "..."
    if isinstance(p, c_ast.ID):
        return p.name
    return ex_type(p)


def ex_type(t):
    if isinstance(t, c_ast.TypeDecl):
        quals = " ".join(t.quals) + " " if t.quals else ""
        return quals + ex_type(t.type)
    if isinstance(t, (c_ast.Typename, c_ast.Decl)):
        return ex_type(t.type)
    if isinstance(t, c_ast.IdentifierType):
        return " ".join(t.names)
    if isinstance(t, c_ast.PtrDecl):
        quals = " ".join(t.quals) + " " if t.quals else ""
        return quals + "pointer to " + ex_type(t.type)
    if isinstance(t, c_ast.ArrayDecl):
        arr = "array"
        if t.dim is not None:
            arr += "[" + gen(t.dim) + "]"
        return arr + " of " + ex_type(t.type)
    if isinstance(t, c_ast.FuncDecl):
        args = ""
        if t.args is not None:
            args = ", ".join(ex_param(p) for p in t.args.params)
        return "function(" + args + ") returning " + ex_type(t.type)
    if isinstance(t, (c_ast.Struct, c_ast.Union)):
        s = "struct" if isinstance(t, c_ast.Struct) else "union"
        if t.name:
            s += " " + t.name
        if t.decls is not None:
            s += " {" + "; ".join(ex_decl(d) for d in t.decls) + "}"
        return s
    if isinstance(t, c_ast.Enum):
        s = "enum"
        if t.name:
            s += " " + t.name
        if t.values is not None:
            items = []
            for e in t.values.enumerators:
                items.append(e.name if e.value is None else e.name + " = " + gen(e.value))
            s += " {" + ", ".join(items) + "}"
        return s
    return type(t).__name__


def ex_decl(d):
    name = d.name if d.name else "(anonymous)"
    if isinstance(d, c_ast.Typedef):
        return name + ": typedef " + ex_type(d.type)
    storage = " ".join(d.storage) + " " if d.storage else ""
    return name + ": " + storage + ex_type(d.type)


class Funcs(c_ast.NodeVisitor):
    def __init__(self, out):
        self.out = out

    def visit_FuncDef(self, node):
        self.out.append(f"{node.decl.name} at {node.decl.coord}")


class Calls(c_ast.NodeVisitor):
    def __init__(self, name, out):
        self.name = name
        self.out = out

    def visit_FuncCall(self, node):
        if isinstance(node.name, c_ast.ID) and node.name.name == self.name:
            self.out.append(f"{self.name} called at {node.name.coord}")
        if node.args is not None:
            self.visit(node.args)


def count(node, tally):
    k = type(node).__name__
    tally[k] = tally.get(k, 0) + 1
    for _, c in node.children():
        count(c, tally)


def run(mode, text, fname, arg, out):
    parser = c_parser.CParser()
    try:
        ast = parser.parse(text, fname)
    except Exception as e:
        if mode == "toks":
            dump_tokens(parser, out)
        msg = str(e)
        out.append(f"! {type(e).__name__}: {msg}" if msg else f"! {type(e).__name__}")
        return
    if mode == "toks":
        dump_tokens(parser, out)
    elif mode in ("show", "showx"):
        buf = io.StringIO()
        if mode == "show":
            ast.show(buf)
        else:
            ast.show(buf, attrnames=True, nodenames=True, showcoord=True)
        out.extend(buf.getvalue().rstrip("\n").split("\n"))
    elif mode == "repr":
        out.extend(repr(ast).split("\n"))
    elif mode in ("gen", "genr"):
        out.extend(gen(ast, mode == "genr").rstrip("\n").split("\n"))
    elif mode == "funcs":
        Funcs(out).visit(ast)
    elif mode == "calls":
        Calls(arg, out).visit(ast)
    elif mode == "explain":
        for ext in ast.ext:
            if isinstance(ext, (c_ast.Decl, c_ast.Typedef)):
                out.append(ex_decl(ext))
            elif isinstance(ext, c_ast.FuncDef):
                out.append(ex_decl(ext.decl) + " (defined)")
    elif mode == "stats":
        tally = {}
        count(ast, tally)
        for k in sorted(tally):
            out.append(f"{k}: {tally[k]}")
        out.append(f"total: {sum(tally.values())}")
    elif mode == "round":
        g1 = gen(ast)
        try:
            g2 = gen(c_parser.CParser().parse(g1, fname))
        except Exception as e:
            out.append(f"round trip: reparse failed: {type(e).__name__}: {e}")
            return
        l1 = g1.split("\n")
        l2 = g2.split("\n")
        if g1 == g2:
            out.append(f"round trip: same, {len(l1) - 1} lines")
        else:
            k = 0
            while k < len(l1) and k < len(l2) and l1[k] == l2[k]:
                k += 1
            out.append(f"round trip: differs at line {k + 1}")
            out.append("  first:  " + (l1[k] if k < len(l1) else "<end>"))
            out.append("  second: " + (l2[k] if k < len(l2) else "<end>"))


def dump_tokens(parser, out):
    for t in parser._tokens._buffer:
        if t is not None:
            out.append(f"{t.lineno}:{t.column} {t.type} {t.value}")


def main():
    with open("data/jobs.txt", encoding="utf-8") as fh:
        jobs = [l.rstrip("\r") for l in fh.read().split("\n") if l.strip()]
    for job in jobs:
        out = [f"$ {job}"]
        words = job.split(" ")
        if words[0] == "snip":
            mode = words[1]
            text = " ".join(words[2:]).replace("{NL}", "\n").replace("{TAB}", "\t")
            run(mode, text, "snip.c", None, out)
        else:
            mode, fname = words[0], words[1]
            arg = words[2] if len(words) > 2 else None
            with open(os.path.join("data", fname), encoding="utf-8", newline="") as fh:
                text = fh.read()
            run(mode, text, fname, arg, out)
        sys.stdout.write("\n".join(out) + "\n")


main()
