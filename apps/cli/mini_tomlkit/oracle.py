# Runs data/jobs.jsonl and the two programs through tomlkit 0.13.2
# itself (the copy in tomlkit/, unchanged) and prints what
# mini_tomlkit.kara must print.
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(write_through=True)
os.chdir(HERE)

import tomlkit  # noqa: E402
from tomlkit._utils import parse_rfc3339  # noqa: E402
from tomlkit.container import Container, OutOfOrderTableProxy  # noqa: E402
from tomlkit.items import AoT, Comment, InlineTable, Item, Table, Whitespace  # noqa: E402
from tomlkit.exceptions import InvalidStringError  # noqa: E402
from tomlkit.toml_file import TOMLFile  # noqa: E402

assert tomlkit.__file__.startswith(HERE), tomlkit.__file__


# --- showing values -----------------------------------------------------

def show(v):
    """repr() for plain values, with dates written as isoformat()."""
    if isinstance(v, dict):
        return "{" + ", ".join(f"{show(k)}: {show(x)}" for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    if isinstance(v, dt.datetime):
        return f"datetime({v.isoformat()})"
    if isinstance(v, dt.date):
        return f"date({v.isoformat()})"
    if isinstance(v, dt.time):
        return f"time({v.isoformat()})"
    return repr(v)


def plain(x):
    if isinstance(x, (Item, Container, OutOfOrderTableProxy)):
        return x.unwrap()
    return x


def esc(line):
    return line.replace("\r", "\\r").replace("\t", "\\t")


def text(s):
    lines = s.split("\n")
    if lines[-1] == "":
        lines.pop()
        tail = None
    else:
        tail = "  (no newline at end)"
    for line in lines:
        print(f"  |{esc(line)}|")
    if tail and s:
        print(tail)


def kind(x):
    return type(x).__name__


# --- the job runner -----------------------------------------------------

def call(name, args):
    kw = {}
    if args and isinstance(args[-1], dict) and "$kw" in args[-1]:
        kw = {k: ev(v) for k, v in args[-1]["$kw"].items()}
        args = args[:-1]
    args = [ev(a) for a in args]
    if name == "item":
        return tomlkit.item(*args, **kw)
    return getattr(tomlkit, name)(*args, **kw)


ENV = {}


def ev(x):
    if isinstance(x, dict):
        if len(x) == 1:
            (k, v), = x.items()
            if k == "$v":
                return ENV[v]
            if k == "$f":
                return float(v)
            if k in ("$dt", "$date", "$time"):
                return parse_rfc3339(v)
            if k == "$call":
                return call(v[0], v[1:])
            if k == "$key":
                return tomlkit.key(v)
        return {k: ev(v) for k, v in x.items()}
    if isinstance(x, list):
        return [ev(v) for v in x]
    return x


def walk(base, keys):
    x = ENV[base]
    for k in keys:
        x = x[ev(k)]
    return x


def body(c, depth):
    pad = "  " * depth
    for k, v in c.body:
        name = "-" if k is None else k.as_string()
        if k is not None and k.is_dotted():
            name += " (dotted)"
        if isinstance(v, Whitespace):
            print(f"  {pad}{name} Whitespace {v.s!r}")
        elif isinstance(v, Comment):
            print(f"  {pad}{name} Comment {v.as_string()!r}")
        elif isinstance(v, (Table, InlineTable)):
            print(f"  {pad}{name} {kind(v)}")
            body(v.value, depth + 1)
        elif isinstance(v, AoT):
            print(f"  {pad}{name} AoT")
            for t in v.body:
                print(f"  {pad}  [[]] Table")
                body(t.value, depth + 2)
        else:
            print(f"  {pad}{name} {kind(v)} {v.as_string()!r}")


def step(op):
    o = op[0]
    if o == "parse":
        with open(f"data/docs/{op[2]}.toml", newline="", encoding="utf-8") as f:
            ENV[op[1]] = tomlkit.parse(f.read())
    elif o == "parses":
        ENV[op[1]] = tomlkit.parse(op[2])
    elif o == "check":
        print("  " + show(tomlkit.parse(op[1]).unwrap()))
    elif o == "rt":
        with open(f"data/docs/{op[1]}.toml", newline="", encoding="utf-8") as f:
            src = f.read()
        out = tomlkit.parse(src).as_string()
        if out == src:
            print(f"  rt {op[1]}: ok")
        else:
            print(f"  rt {op[1]}: differs")
            text(out)
    elif o == "let":
        ENV[op[1]] = ev(op[2])
    elif o == "get":
        ENV[op[1]] = walk(op[2], op[3:])
    elif o == "text":
        text(walk(op[1], op[2:]).as_string())
    elif o == "show":
        print("  " + show(plain(walk(op[1], op[2:]))))
    elif o == "print":
        x = walk(op[1], op[2:])
        print(f"  {kind(x)} {show(plain(x))}")
    elif o == "raw":
        x = walk(op[1], op[2:])
        print(f"  {kind(x)} {x.as_string()!r}")
    elif o == "body":
        x = walk(op[1], op[2:])
        body(x if isinstance(x, Container) else x.value, 0)
    elif o == "set":
        walk(op[1], op[2:-2])[ev(op[-2])] = ev(op[-1])
    elif o == "del":
        x = walk(op[1], op[2:-1])
        del x[ev(op[-1])]
    elif o == "append":
        ENV[op[1]].append(ev(op[2]), ev(op[3]))
    elif o == "add":
        ENV[op[1]].add(*[ev(a) for a in op[2:]])
    elif o == "push":
        ENV[op[1]].append(ev(op[2]))
    elif o == "insert":
        ENV[op[1]].insert(op[2], ev(op[3]))
    elif o == "multiline":
        ENV[op[1]].multiline(op[2])
    elif o == "add_line":
        kw = {k: ev(v) for k, v in op[3].items()} if len(op) > 3 else {}
        ENV[op[1]].add_line(*[ev(a) for a in op[2]], **kw)
    elif o == "clear":
        ENV[op[1]].clear()
    elif o == "comment":
        ENV[op[1]].comment(op[2])
    elif o == "indent":
        ENV[op[1]].indent(op[2])
    elif o == "setdefault":
        r = ENV[op[1]].setdefault(op[2], ev(op[3]))
        print(f"  {kind(r)} {show(plain(r))}")
    elif o == "pop":
        r = ENV[op[1]].pop(op[2])
        print(f"  {kind(r)} {show(plain(r))}")
    elif o == "update":
        ENV[op[1]].update(ev(op[2]))
    elif o == "len":
        print(f"  {len(walk(op[1], op[2:]))}")
    elif o == "keys":
        print(f"  {show(list(walk(op[1], op[2:])))}")
    elif o == "in":
        print(f"  {ev(op[2]) in ENV[op[1]]}")
    elif o == "super":
        print(f"  {walk(op[1], op[2:]).is_super_table()}")
    elif o == "dumps":
        text(tomlkit.dumps(ev(op[1]), sort_keys=op[2]))
    elif o == "kv":
        k, v = tomlkit.key_value(op[1])
        print(f"  {k.as_string()!r} {kind(v)} {v.as_string()!r} {show(plain(v))}")
    elif o == "value":
        v = tomlkit.value(op[1])
        print(f"  {kind(v)} {v.as_string()!r} {show(plain(v))}")
    elif o == "fread":
        f = TOMLFile(f"data/docs/{op[2]}.toml")
        ENV[op[1]] = f.read()
        ENV[op[1] + ".file"] = f
        print(f"  linesep {f._linesep!r}")
    elif o == "fwrite":
        f = ENV[op[1] + ".file"]
        f._path = f"data/out/{op[2]}"
        f.write(ENV[op[1]])
        with open(f._path, "rb") as g:
            text(g.read().decode("utf-8"))
    else:
        raise SystemExit(f"unknown op {o}")


def run_jobs():
    with open("data/jobs.jsonl", encoding="utf-8") as f:
        jobs = [json.loads(line) for line in f]
    for job in jobs:
        print(f"== {job['name']}")
        ENV.clear()
        for op in job["steps"]:
            print(f"> {' '.join(json.dumps(a, ensure_ascii=False) for a in op)}")
            try:
                step(op)
            except Exception as e:  # noqa: BLE001
                msg = str(e)
                if isinstance(e, InvalidStringError):
                    # The rest names a set, which prints in hash order.
                    msg = msg.split(" The character sequences")[0]
                print(f"  ! {type(e).__name__}: {msg}")



# --- program 1: a release script ------------------------------------------
#
# Reads data/repo/release.toml, sets the new version in each manifest it
# lists, keeps the version requirement of every path dependency in step,
# adds the release to CHANGELOG.toml, and writes the results to
# data/out/repo/ with their formatting and comments kept.

def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def bump_requirement(old, new):
    i = 0
    while i < len(old) and not old[i].isdigit():
        i += 1
    return old[:i] + new


def bump_path_deps(deps, section, new, crates, changes):
    for name, dep in deps.items():
        if name in crates and isinstance(dep, (Table, InlineTable)) \
                and "path" in dep and "version" in dep:
            old = str(dep["version"])
            dep["version"] = bump_requirement(old, new)
            changes.append(f"{section}.{name}.version: {old} -> {dep['version']}")


def release():
    print("== release")
    plan = tomlkit.parse(read("data/repo/release.toml"))
    rel = plan["release"]
    new = str(rel["version"])
    crates = [str(c) for c in rel["crates"]]
    print(f"  version {new}, dated {rel['date'].isoformat()}")
    for f in rel["files"]:
        path = str(f["path"])
        doc = tomlkit.parse(read(f"data/repo/{path}"))
        changes = []
        k = f["kind"]
        if k == "cargo-workspace":
            pkg = doc["workspace"]["package"]
            changes.append(f"workspace.package.version: {pkg['version']} -> {new}")
            pkg["version"] = new
            bump_path_deps(doc["workspace"]["dependencies"],
                           "workspace.dependencies", new, crates, changes)
        elif k == "cargo":
            pkg = doc["package"]
            v = pkg["version"]
            if isinstance(v, str):
                changes.append(f"package.version: {v} -> {new}")
                pkg["version"] = new
            else:
                changes.append("package.version: from the workspace")
            for section in ("dependencies", "dev-dependencies"):
                if section in doc:
                    bump_path_deps(doc[section], section, new, crates, changes)
        elif k == "poetry":
            p = doc["tool"]["poetry"]
            changes.append(f"tool.poetry.version: {p['version']} -> {new}")
            p["version"] = new
        elif k == "pep621":
            p = doc["project"]
            changes.append(f"project.version: {p['version']} -> {new}")
            p["version"] = new
        else:
            changes.append(f"unknown kind {k!r}, left alone")
        out = tomlkit.dumps(doc)
        write(f"data/out/repo/{path}", out)
        print(f"  {path}:")
        for c in changes:
            print(f"    {c}")
        text(read(f"data/out/repo/{path}"))

    log = tomlkit.parse(read("data/repo/CHANGELOG.toml"))
    entry = tomlkit.item({"version": new, "date": rel["date"].unwrap(),
                          "notes": str(rel["notes"])})
    entry.add(tomlkit.nl())
    releases = log["releases"]
    releases.insert(0, entry)
    write("data/out/repo/CHANGELOG.toml", log.as_string())
    print("  CHANGELOG.toml:")
    text(read("data/out/repo/CHANGELOG.toml"))
    again = tomlkit.parse(read("data/out/repo/CHANGELOG.toml"))
    for r in again["releases"]:
        print(f"    {r['version']} {r['date'].isoformat()} {r['notes']}")


# --- program 2: migrating service configs to schema 2 ---------------------
#
# Copies data/etc/ to data/out/etc/ and moves each config there to
# schema 2 in place: the log settings go into a [logging] table, the
# server's *_timeout strings become *_timeout_ms integers, and the
# [[upstreams]] array becomes a table of tables named after each
# upstream. Comments and line endings are kept.

def duration_ms(s):
    total = 0
    num = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c.isdigit():
            num += c
            i += 1
            continue
        unit = c
        if s.startswith("ms", i):
            unit = "ms"
        if not num:
            raise ValueError(f"bad duration {s!r}")
        n = int(num)
        if unit == "ms":
            total += n
        elif unit == "s":
            total += n * 1000
        elif unit == "m":
            total += n * 60000
        elif unit == "h":
            total += n * 3600000
        else:
            raise ValueError(f"bad duration {s!r}")
        num = ""
        i += len(unit)
    if num:
        raise ValueError(f"bad duration {s!r}")
    return total


def migrate_one(name):
    path = f"data/out/etc/{name}"
    f = TOMLFile(path)
    doc = f.read()
    print(f"  {name}:")
    if doc.get("schema") == 2:
        print("    already at schema 2")
        return
    notes = []
    log = tomlkit.table()
    for old, new in (("log_level", "level"), ("log_format", "format")):
        if old in doc:
            it = doc.item(old)
            doc.remove(old)
            log.add(new, it)
            notes.append(f"{old} -> logging.{new}")
    if len(log):
        doc.add("logging", log)
    if "server" in doc:
        srv = doc["server"]
        for k in list(srv):
            v = srv[k]
            if k.endswith("_timeout") and isinstance(v, str):
                try:
                    ms = duration_ms(str(v))
                except ValueError as e:
                    notes.append(f"server.{k}: {e}")
                    continue
                srv.remove(k)
                srv.add(k + "_ms", ms)
                notes.append(f"server.{k} = {v!s} -> server.{k}_ms = {ms}")
    if "upstreams" in doc and isinstance(doc.item("upstreams"), AoT):
        ups = tomlkit.table(True)
        for t in doc["upstreams"]:
            n = str(t["name"])
            nt = tomlkit.table()
            for k, v in t.items():
                if k != "name":
                    nt[k] = v
            ups.append(n, nt)
            notes.append(f"upstreams[{n}] -> upstreams.{n}")
        doc.remove("upstreams")
        doc.append("upstreams", ups)
    if "version" in doc:
        doc.remove("version")
    doc.add("schema", 2)
    notes.append("version 1 -> schema 2")
    f.write(doc)
    for n in notes:
        print(f"    {n}")
    text(read(path))
    print("    " + show(tomlkit.parse(read(path)).unwrap()))


def migrate():
    print("== migrate")
    for name in sorted(os.listdir("data/etc")):
        write(f"data/out/etc/{name}", read(f"data/etc/{name}"))
    for name in sorted(os.listdir("data/out/etc")):
        migrate_one(name)


run_jobs()
release()
migrate()
