# Runs data/jobs.tsv through sexpdata itself (vendor/sexpdata.py,
# unchanged) and prints what each job gives; expected.out is this output.
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True

import sexpdata  # noqa: E402
from sexpdata import Symbol, String, Quoted, Brackets, car, cdr, dumps, loads, parse  # noqa: E402

DATA = os.path.join(HERE, "data")
# what ${VAR} in a KiCad library table expands to
KICAD_ENV = {"KICAD8_FOOTPRINT_DIR": "/usr/share/kicad/footprints", "KIPRJMOD": "/home/dev/usb-power"}


def show(text):
    out = []
    for c in text:
        if c == "\r":
            out.append("<CR>")
        elif (c < " " and c not in "\t\n") or c == "\x7f":
            out.append("<x%02x>" % ord(c))
        else:
            out.append(c)
    return "".join(out)


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return f.read()


def options(args):
    kw = {}
    for a in args:
        if a == "pretty_print":
            kw["pretty_print"] = True
        else:
            k, v = a.split("=", 1)
            v = v.replace("\\t", "\t")
            if k == "string_to":
                v = {"Symbol": Symbol, "String": String}[v]
            kw[k] = v
    return kw


def parse_job(args):
    try:
        items = parse(read(args[0]), **options(args[1:]))
    except Exception as e:
        print(err(e))
        return
    print("%d items" % len(items))
    for i, x in enumerate(items):
        print(show("[%d] %r" % (i, x)))


def loads_job(args):
    try:
        print(show(repr(loads(read(args[0])))))
    except Exception as e:
        print(err(e))


def roundtrip_job(args):
    kw = options(args[1:])
    for x in parse(read(args[0])):
        try:
            print(show(dumps(x, **kw)))
        except Exception as e:
            print(err(e))


def dumps_job(args):
    v = json.loads(read(args[0]))
    try:
        print(show(dumps(v, **options(args[1:]))))
    except Exception as e:
        print(err(e))


def carcdr_job(args):
    for top in parse(read(args[0])):
        for x in cdr(top) if args[0].startswith("emacs") else top:
            print(show("car %r" % (car(x),)))
            print(show("cdr %r" % (cdr(x),)))


# --- programs over the trees

def items_named(tree, name):
    return [x for x in tree if isinstance(x, list) and x and x[0] == Symbol(name)]


def first(tree, name):
    found = items_named(tree, name)
    return found[0] if found else None


def bom_job(args):
    sch = loads(read(args[0]))
    tb = first(sch, "title_block")
    print("%s rev %s (%s)" % (first(tb, "title")[1], first(tb, "rev")[1], first(tb, "date")[1]))
    groups = {}
    for sym in items_named(sch, "symbol"):
        if first(sym, "lib_id") is None:
            continue
        props = dict((p[1], p[2]) for p in items_named(sym, "property"))
        if first(sym, "in_bom")[1] != Symbol("yes"):
            print("skip %s (not in BOM)" % props.get("Reference"))
            continue
        key = (props.get("Value", ""), props.get("Footprint", ""), first(sym, "lib_id")[1])
        groups.setdefault(key, []).append(props["Reference"])
        if "Description" in props:
            print("note %s: %s" % (props["Reference"], props["Description"]))
    for key in sorted(groups):
        refs = sorted(groups[key])
        print("%d x %s  %s  %s  [%s]" % (len(refs), ",".join(refs), key[0], key[1], key[2]))
    wires = items_named(sch, "wire")
    print("%d wire(s); first runs %s" % (len(wires), dumps(first(wires[0], "pts")[1:])))


def libs_job(args):
    table = loads(read(args[0]))
    print("version %s" % first(table, "version")[1])
    for lib in items_named(table, "lib"):
        name = first(lib, "name")[1]
        uri = first(lib, "uri")[1]
        for k, v in KICAD_ENV.items():
            uri = uri.replace("${%s}" % k, v)
        state = "disabled" if first(lib, "disabled") is not None else "enabled"
        print("%s: %s (%s, %s) %s" % (name, uri, first(lib, "type")[1], state, dumps(first(lib, "descr")[1])))


def deps_job(args):
    for stanza in parse(read(args[0])):
        kind = stanza[0]
        rest = stanza[1:]
        if kind == Symbol("library"):
            print("library %s (%s)" % (first(rest, "name")[1], first(rest, "public_name")[1]))
            print("  libraries: " + " ".join(str(x) for x in cdr(first(rest, "libraries"))))
            print("  ppx: " + " ".join(str(x) for x in cdr(first(first(rest, "preprocess"), "pps"))))
            print("  flags: " + dumps(cdr(first(rest, "flags"))))
        elif kind == Symbol("package"):
            print("package %s: %s" % (first(rest, "name")[1], first(rest, "synopsis")[1]))
            for dep in cdr(first(rest, "depends")):
                print("  depends %s %s" % (car(dep), dumps(cdr(dep))))
        elif len(rest) == 1 and not isinstance(rest[0], list):
            print("%s = %s" % (kind, dumps(rest[0])))
        else:
            print("%s %s" % (kind, dumps(rest)))


def packages_job(args):
    contents = loads(read(args[0]))
    print("archive format %s" % car(contents))
    for entry in cdr(contents):
        name = car(entry)
        desc = cdr(entry).I
        version = ".".join(str(n) for n in desc[0])
        reqs = desc[1] or []
        deps = ", ".join("%s %s" % (car(r), ".".join(str(n) for n in r[1])) for r in reqs)
        extras = dict((car(e), cdr(e)) for e in desc[4])
        print("%s %s [%s] %s" % (name, version, desc[3], desc[2]))
        print("  needs: " + (deps if deps else "-"))
        print("  url: %s" % extras.get(Symbol(":url")))
        if Symbol(":keywords") in extras:
            print("  keywords: " + dumps(extras[Symbol(":keywords")]))


def customs_job(args):
    for form in parse(read(args[0])):
        print("%s:" % car(form))
        for q in cdr(form):
            setting = q.x
            print("  %s = %s" % (car(setting), dumps(setting[1])))


def smt_job(args):
    for cmd in parse(read(args[0])):
        head = car(cmd)
        if head == Symbol("declare-fun"):
            print("declare %s : %s -> %s" % (cmd[1], dumps(cmd[2]), cmd[3]))
        elif head == Symbol("assert"):
            print("assert " + dumps(cmd[1], pretty_print=True).replace("\n", " "))
        else:
            print("%s %s" % (head, dumps(cmd[1:])))


JOBS = {
    "parse": parse_job, "loads": loads_job, "roundtrip": roundtrip_job, "dumps": dumps_job,
    "carcdr": carcdr_job, "bom": bom_job, "libs": libs_job, "deps": deps_job,
    "packages": packages_job, "customs": customs_job, "smt": smt_job,
}


def main():
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
        jobs = [line.rstrip("\n").split("\t") for line in f]
    for job in jobs:
        print("== " + show(" ".join(job)))
        JOBS[job[0]](job[1:])


main()
