# The oracle: data/jobs.txt run against Python's configparser.
import configparser, io

def parser(words):
    kw = {}
    for w in words:
        k, v = w.split("=", 1)
        if k == "interpolation":
            kw["interpolation"] = {"basic": configparser.BasicInterpolation(),
                                   "extended": configparser.ExtendedInterpolation(),
                                   "none": None}[v]
        elif k == "strict":
            kw["strict"] = v == "1"
        elif k == "empty_lines":
            kw["empty_lines_in_values"] = v == "1"
        elif k == "no_value":
            kw["allow_no_value"] = v == "1"
        elif k == "inline":
            kw["inline_comment_prefixes"] = tuple(v)
        elif k == "comments":
            kw["comment_prefixes"] = tuple(v)
        elif k == "delimiters":
            kw["delimiters"] = tuple(v)
        elif k == "default":
            kw["default_section"] = v
    return configparser.ConfigParser(**kw)

def err(e):
    return f"{type(e).__name__}: {e}"

def dump(cp):
    names = [cp.default_section] + cp.sections()
    for s in names:
        print(f"  [{s}]")
        raw = cp.defaults() if s == cp.default_section else dict(cp.items(s, raw=True))
        for k, v in raw.items():
            print(f"    {k} = {v!r}")
            try:
                got = cp.get(s, k)
                if got != v:
                    print(f"      -> {got!r}")
            except Exception as e:
                print(f"      -> {err(e)}")

def run(cp, w):
    cmd = w[0]
    if cmd == "read":
        return cp.read(w[1:])
    if cmd == "sections":
        return cp.sections()
    if cmd in ("get", "getint", "getboolean", "has", "remove-option"):
        s, o = " ".join(w[1:-1]), w[-1]
        if cmd == "get":
            return cp.get(s, o)
        if cmd == "getint":
            return cp.getint(s, o)
        if cmd == "getboolean":
            return cp.getboolean(s, o)
        if cmd == "has":
            return cp.has_option(s, o)
        return cp.remove_option(s, o)
    if cmd == "set":
        cp.set(w[1], w[2], " ".join(w[3:]))
        return cp.get(w[1], w[2], raw=True)
    s = " ".join(w[1:])
    if cmd == "items":
        return cp.items(s)
    if cmd == "add":
        return cp.add_section(s)
    if cmd == "remove-section":
        return cp.remove_section(s)
    raise SystemExit(f"unknown job {cmd}")

cp = None
with open("data/jobs.txt") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        w = line.split()
        if w[0] == "parser":
            print(f"== {line}")
            cp = parser(w[1:])
            continue
        if w[0] == "dump":
            print("-- dump")
            dump(cp)
            continue
        if w[0] == "write":
            print("-- write")
            buf = io.StringIO()
            cp.write(buf)
            for l in buf.getvalue().split("\n")[:-1]:
                print(f"  |{l}")
            continue
        try:
            r = run(cp, w)
            print(f"{line}: {r!r}")
        except Exception as e:
            print(f"{line}: {err(e)}")
