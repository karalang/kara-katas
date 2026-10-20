# Runs data/ through Python 3.13's ast module and prints what
# expected.out holds. Run it from the app directory, after mk.py.
import ast
import os
import re


def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [line[:-1] if line.endswith("\n") else line for line in f]


def no_addr(s):
    return re.sub(r" at 0x[0-9a-f]+", "", s)


# ------------------------------------------------------------ jobs

def run_jobs():
    print("== jobs")
    for line in read_lines("data/jobs.tsv"):
        op, lit = line.split("\t")
        src = ast.literal_eval(lit)
        print(op + " " + lit)
        if op == "eval":
            try:
                print("  " + repr(ast.literal_eval(src)))
            except (ValueError, TypeError, SyntaxError) as e:
                print("  ! %s: %s" % (type(e).__name__, no_addr(str(e))))
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            print("  ! %s: %s at %d,%d" % (type(e).__name__, e.msg, e.lineno, e.offset))
            continue
        print("  " + ast.dump(tree, include_attributes=(op == "attrs")))
        if op == "parse":
            for l in ast.unparse(tree).split("\n"):
                print("  | " + l)


# ------------------------------------------------------------ programs

def project_files():
    out = []
    for root, dirs, files in os.walk("data/project"):
        for f in files:
            out.append(os.path.join(root, f))
    return sorted(out)


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        return ast.parse(f.read())


def module_name(path):
    parts = path[len("data/project/"):-len(".py")].split("/")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def package_of(path):
    name = module_name(path)
    if path.endswith("__init__.py"):
        return name
    return name.rpartition(".")[0]


def unparse_files(paths):
    for path in paths:
        print("== unparse " + path)
        tree = parse_file(path)
        text = ast.unparse(tree)
        for l in text.split("\n"):
            print("| " + l)
        again = ast.parse(text)
        print("round trip: " + ("same" if ast.dump(again) == ast.dump(tree) else "DIFFERENT"))


def signature(node):
    return "(" + ast.unparse(node.args) + ")" + (" -> " + ast.unparse(node.returns) if node.returns else "")


# Classes and functions with where they start, their signatures and the
# first line of their docstrings.
def outline(paths):
    print("== outline")
    for path in paths:
        tree = parse_file(path)
        doc = ast.get_docstring(tree)
        print("%s: %s" % (path, doc.split("\n")[0] if doc else "-"))

        def walk(body, prefix, depth):
            for node in body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    kind = {"FunctionDef": "def", "AsyncFunctionDef": "async def", "ClassDef": "class"}[type(node).__name__]
                    decos = "".join("@" + ast.unparse(d) + " " for d in node.decorator_list)
                    if isinstance(node, ast.ClassDef):
                        bases = [ast.unparse(b) for b in node.bases] + [ast.unparse(k) for k in node.keywords]
                        sig = "(" + ", ".join(bases) + ")" if bases else ""
                    else:
                        sig = signature(node)
                    d = ast.get_docstring(node)
                    first = "  # " + d.split("\n")[0] if d else ""
                    print("%s%d:%d %s%s %s%s%s%s" % ("  " * depth, node.lineno, node.col_offset, decos, kind, prefix, node.name, sig, first))
                    walk(node.body, prefix + node.name + ".", depth + 1)
        walk(tree.body, "", 1)


def imported_modules(path, tree):
    pkg = package_of(path).split(".")
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                found.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = pkg[:len(pkg) - (node.level - 1)]
                name = ".".join(base + ([node.module] if node.module else []))
            else:
                name = node.module
            found.add(name)
    return found


def imports(paths):
    print("== imports")
    users = {}
    for path in paths:
        mod = module_name(path)
        found = imported_modules(path, parse_file(path))
        print("%s: %s" % (mod, ", ".join(sorted(found))))
        for f in found:
            users.setdefault(f, set()).add(mod)
    mods = set(module_name(p) for p in paths)
    for m in sorted(users):
        if m in mods:
            print("%s <- %s" % (m, ", ".join(sorted(users[m]))))


# Names an import binds and the module never loads (pyflakes' check,
# without its scopes); names in __all__ count as used.
def unused_imports(paths):
    print("== unused imports")
    for path in paths:
        tree = parse_file(path)
        used = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used.add(node.id)
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id == "__all__" and isinstance(node.value, (ast.List, ast.Tuple)):
                        for e in node.value.elts:
                            if isinstance(e, ast.Constant) and isinstance(e.value, str):
                                used.add(e.value)
        for node in tree.body:
            if isinstance(node, ast.Import):
                for a in node.names:
                    bound = a.asname or a.name.split(".")[0]
                    if bound not in used:
                        print("%s:%d:%d: %r imported but unused" % (path, node.lineno, node.col_offset + 1, a.asname or a.name))
            elif isinstance(node, ast.ImportFrom) and node.module != "__future__":
                for a in node.names:
                    if a.name == "*":
                        continue
                    bound = a.asname or a.name
                    full = (node.module + "." if node.module else "." * node.level) + a.name
                    if bound not in used:
                        print("%s:%d:%d: %r imported but unused" % (path, node.lineno, node.col_offset + 1, full))


DECISIONS = (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.Assert)


# Cyclomatic complexity in the manner of radon: one, plus one for each
# branch point in the function's own body (nested functions and classes
# count for themselves), each comprehension and its ifs, and each extra
# operand of `and` and `or`.
def complexity(paths):
    print("== complexity")
    rows = []

    def score(node):
        n = 0
        stack = list(ast.iter_child_nodes(node))
        while stack:
            c = stack.pop()
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(c, DECISIONS):
                n += 1
            elif isinstance(c, ast.comprehension):
                n += 1 + len(c.ifs)
            elif isinstance(c, ast.BoolOp):
                n += len(c.values) - 1
            stack.extend(ast.iter_child_nodes(c))
        return n

    def walk(path, body, prefix):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                rows.append((path, node.lineno, prefix + node.name, 1 + score(node)))
                walk(path, node.body, prefix + node.name + ".")
            elif isinstance(node, ast.ClassDef):
                walk(path, node.body, prefix + node.name + ".")

    for path in paths:
        walk(path, parse_file(path).body, "")
    rows.sort(key=lambda r: (-r[3], r[0], r[1]))
    for path, line, name, c in rows:
        grade = "A" if c <= 5 else "B" if c <= 10 else "C"
        print("%s %2d %s:%d %s" % (grade, c, path, line, name))


def node_counts(paths):
    print("== node counts")
    counts = {}
    for path in paths:
        for node in ast.walk(parse_file(path)):
            name = type(node).__name__
            counts[name] = counts.get(name, 0) + 1
    for name, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print("%5d %s" % (n, name))


run_jobs()
files = project_files()
unparse_files(files)
outline(files)
imports(files)
unused_imports(files)
complexity(files)
node_counts(files)
