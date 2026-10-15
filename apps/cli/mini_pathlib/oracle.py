# The oracle: mini_pathlib written with Python 3.13's pathlib.
from pathlib import PurePosixPath, PureWindowsPath, PurePath
import os

FL = {"posix": PurePosixPath, "win": PureWindowsPath}

def show_path(fl, s):
    p = FL[fl](s)
    print(f"{fl} {s!r}")
    print(f"  str {str(p)!r} {p!r}")
    print(f"  drive {p.drive!r} root {p.root!r} anchor {p.anchor!r}")
    print(f"  parts {p.parts!r}")
    print(f"  name {p.name!r} suffix {p.suffix!r} suffixes {p.suffixes!r} stem {p.stem!r}")
    print(f"  parent {str(p.parent)!r} parents {[str(q) for q in p.parents]!r}")
    print(f"  absolute {p.is_absolute()} posix {p.as_posix()!r}")

def attempt(f):
    try:
        return f()
    except ValueError as e:
        return f"ValueError: {e}"

def op(a):
    name, fl, args = a[0], a[1], a[2:]
    P = FL[fl]
    if name == "join":
        r = repr(str(P(*args)))
    elif name in ("with_name", "with_suffix", "with_stem"):
        r = attempt(lambda: repr(str(getattr(P(args[0]), name)(args[1]))))
    elif name == "relative_to":
        walk = len(args) > 2
        r = attempt(lambda: repr(str(P(args[0]).relative_to(args[1], walk_up=walk))))
    elif name == "is_relative_to":
        r = P(args[0]).is_relative_to(args[1])
    elif name == "match":
        r = attempt(lambda: P(args[0]).match(args[1]))
    elif name == "full_match":
        r = P(args[0]).full_match(args[1])
    elif name == "eq":
        r = P(args[0]) == P(args[1])
    elif name == "lt":
        r = P(args[0]) < P(args[1])
    elif name == "uri":
        r = attempt(lambda: P(args[0]).as_uri())
    elif name == "sort":
        r = [str(p) for p in sorted(P(x) for x in args)]
    print(f"{name} {fl} {args!r} -> {r}")

def walk(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for n in dirnames + filenames:
            out.append((PurePosixPath(dirpath, n).relative_to(root), n in dirnames))
    return out

def main():
    print("== paths")
    for line in open("data/paths.txt").read().splitlines():
        fl, s = line.split("\t")
        show_path(fl, s)
    print("== ops")
    for line in open("data/ops.txt").read().splitlines():
        op(line.split("\t"))
    print("== tree")
    entries = sorted(walk("data/tree"))
    for p, d in entries:
        print(f"{p}{'/' if d else ''}")
    rules = []
    for line in open("data/rules.txt").read().splitlines():
        if line == "" or line.startswith("#"):
            continue
        verb, pat = line.split(" ")
        rules.append((verb, pat))
    print("== select")
    chosen = []
    for p, d in entries:
        if d:
            continue
        keep, why = False, "-"
        for i, (verb, pat) in enumerate(rules):
            if p.full_match(pat):
                keep, why = verb == "include", f"{i + 1}:{verb} {pat}"
        print(f"{'+' if keep else '-'} {p}  ({why})")
        if keep:
            chosen.append(p)
    print("== sdist")
    kinds = {}
    for p in chosen:
        k = "".join(p.suffixes) or "(none)"
        kinds[k] = kinds.get(k, 0) + 1
    for k in sorted(kinds):
        print(f"{k} {kinds[k]}")
    print("== install")
    base = PureWindowsPath("C:/Users/dev/AppData/Local/pkg")
    for p in chosen:
        if p.full_match("src/**/*.py"):
            rel = p.relative_to("src")
            print(f"{p} -> {base / rel}")
            print(f"  {(base / rel).as_uri()}")
            print(f"  {(base / rel).with_suffix('.pyc').relative_to(base / 'pkg', walk_up=True)}")
    print("== objects")
    for p in chosen:
        if p.match("_native/*.c"):
            obj = PurePosixPath("build/obj") / p.relative_to("src").with_suffix(".o")
            print(f"{p} -> {obj} ({obj.parent.relative_to(p.parent, walk_up=True)})")

main()
