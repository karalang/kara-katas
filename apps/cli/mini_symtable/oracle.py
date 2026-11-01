"""The oracle for mini_symtable: runs data/jobs.txt through CPython's own
`symtable` module and prints what each job reports.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import symtable

DATA = "data"
FLAGS = ("referenced", "assigned", "parameter", "global", "declared_global",
         "local", "free", "nonlocal", "imported", "annotated", "namespace")

with open(os.path.join(DATA, "builtins.txt"), encoding="utf-8") as fh:
    BUILTINS = set(fh.read().split())


def scope(sym):
    return sym._scope_str()


def sorted_symbols(table):
    return [table.lookup(n) for n in sorted(table.get_identifiers())]


def tables(table, out, depth=0):
    pad = "  " * depth
    head = f"{pad}{table.get_type()} {table.get_name()} line {table.get_lineno()}"
    if table.is_nested():
        head += " nested"
    if table.is_optimized():
        head += " optimized"
    out.append(head)
    if table.get_type() == "function":
        out.append(f"{pad}  params: {', '.join(table.get_parameters()) or '-'}")
        for label, names in (("locals", table.get_locals()), ("frees", table.get_frees()),
                             ("globals", table.get_globals()),
                             ("nonlocals", table.get_nonlocals())):
            if names:
                out.append(f"{pad}  {label}: {', '.join(sorted(names))}")
    if table.get_type() == "class":
        methods = table.get_methods()
        if methods:
            out.append(f"{pad}  methods: {', '.join(methods)}")
    for sym in sorted_symbols(table):
        flags = [f for f in FLAGS if getattr(sym, "is_" + f)()]
        ns = len(sym.get_namespaces())
        extra = f" ({ns} namespaces)" if ns > 1 else ""
        out.append(f"{pad}  {sym.get_name()}: {' '.join(flags) or '-'}{extra}")
    for child in table.get_children():
        tables(child, out, depth + 1)


def dump(table, filename, out, level=0):
    # `python -m symtable`, with each table's symbols sorted by name.
    indent = "    " * level
    nested = "nested " if table.is_nested() else ""
    if table.get_type() == "module":
        what = f"from file {filename!r}"
    else:
        what = f"{table.get_name()!r}"
    out.append(f"{indent}symbol table for {nested}{table.get_type()} {what}:")
    for sym in sorted_symbols(table):
        flags = ", ".join(sym._flags_str()).lower()
        out.append(f"    {indent}{scope(sym).lower()} symbol {sym.get_name()!r}: {flags}")
    out.append("")
    for child in table.get_children():
        dump(child, filename, out, level + 1)


def walk(table, parents=()):
    yield table, parents
    for child in table.get_children():
        yield from walk(child, parents + (table,))


def frees_below(table):
    names = set()
    for child in table.get_children():
        for t, _ in walk(child):
            for sym in t.get_symbols():
                if sym.is_free():
                    names.add(sym.get_name())
    return names


def where(table):
    if table.get_type() == "module":
        return "the module"
    return f"{table.get_type()} '{table.get_name()}'"


def lint(top, filename):
    problems = []
    module_bound = {s.get_name() for s in top.get_symbols()
                    if s.is_assigned() or s.is_imported()}
    for t, _ in walk(top):
        for s in t.get_symbols():
            if s.is_declared_global() and s.is_assigned():
                module_bound.add(s.get_name())
    for t, parents in walk(top):
        line = t.get_lineno()
        kind = t.get_type()
        below = frees_below(t)
        for s in sorted_symbols(t):
            name = s.get_name()
            if name.startswith("."):
                continue
            if (kind == "function" and scope(s) == "LOCAL" and not s.is_referenced()
                    and not s.is_parameter() and not name.startswith("_")
                    and name not in below):
                what = "import" if s.is_imported() else "local"
                problems.append((line, f"unused {what} '{name}' in {where(t)}"))
            if (s.is_referenced() and scope(s) == "GLOBAL_IMPLICIT"
                    and name not in module_bound and name not in BUILTINS):
                problems.append((line, f"undefined name '{name}' in {where(t)}"))
            if kind == "function" and s.is_declared_global() and not s.is_assigned():
                problems.append((line, f"'{name}' is declared global in {where(t)} "
                                       "but never assigned there"))
            if (kind == "function" and (s.is_parameter() or s.is_assigned())
                    and s.is_local() and name in BUILTINS):
                problems.append((line, f"'{name}' shadows a builtin in {where(t)}"))
            if (kind == "function" and parents and parents[-1].get_type() == "class"
                    and s.is_referenced() and scope(s) == "GLOBAL_IMPLICIT"):
                cls = parents[-1]
                if name in cls.get_identifiers() and cls.lookup(name).is_assigned():
                    problems.append((line, f"{where(t)} reads global '{name}', not "
                                           f"class attribute {cls.get_name()}.{name}"))
    problems.sort()
    out = [f"{filename}:{line}: {msg}" for line, msg in problems]
    out.append(f"{len(problems)} problems")
    return out


def run(mode, source, filename):
    out = []
    try:
        top = symtable.symtable(source, filename, "exec")
    except SyntaxError as e:
        return [f"! SyntaxError: {e.msg} at {e.lineno}:{e.offset}-{e.end_lineno}:{e.end_offset}"]
    if mode in ("tables", "error"):
        tables(top, out)
    elif mode == "dump":
        dump(top, filename, out)
    elif mode == "lint":
        out.extend(lint(top, filename))
    return out


def main():
    with open(os.path.join(DATA, "jobs.txt"), encoding="utf-8") as fh:
        jobs = fh.read().splitlines()
    for job in jobs:
        print(f"$ {job}")
        mode, rest = job.split(" ", 1)
        if mode == "snip":
            mode, src = rest.split(" ", 1)
            source = src.replace("\\n", "\n").replace("\\t", "\t") + "\n"
            lines = run(mode, source, "snip.py")
        else:
            with open(os.path.join(DATA, rest), encoding="utf-8") as fh:
                source = fh.read()
            lines = run(mode, source, rest)
        for line in lines:
            print(line)


main()
