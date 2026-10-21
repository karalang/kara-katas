"""Runs data/jobs.txt through the vendored vobject 0.9.8 and prints what
mini_vobject.kara must print. Run from this directory:
    python3 -s -P -B oracle.py > expected.out
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import vobject  # noqa: E402
from vobject.base import ContentLine, Component, ParseError, readComponents  # noqa: E402

DATA = os.path.join(HERE, "data")


def read_text(name):
    with open(os.path.join(DATA, name), "rb") as f:
        return f.read().decode("utf-8")


def esc(s):
    if not isinstance(s, str):
        s = str(s)
    out = []
    for c in s:
        o = ord(c)
        if c == "\\":
            out.append("\\\\")
        elif c == "\n":
            out.append("\\n")
        elif c == "\t":
            out.append("\\t")
        elif c == "\r":
            out.append("\\r")
        elif 32 <= o < 127:
            out.append(c)
        else:
            out.append("\\u%04x" % o)
    return "".join(out)


def components(name, transform=True):
    return list(readComponents(read_text(name), transform=transform,
                               ignoreUnreadable=False))


def param_str(params):
    bits = []
    for k in sorted(params.keys()):
        bits.append("%s=%s" % (k, ",".join(esc(v) for v in params[k])))
    return ";".join(bits)


def value_repr(line):
    v = line.value
    if isinstance(v, bytes):
        return "<%d bytes>" % len(v)
    if hasattr(v, "family"):  # Name
        return "Name(family=%s given=%s additional=%s prefix=%s suffix=%s)" % (
            esc(Name_s(v.family)), esc(Name_s(v.given)), esc(Name_s(v.additional)),
            esc(Name_s(v.prefix)), esc(Name_s(v.suffix)))
    if hasattr(v, "street"):  # Address
        return "Address(box=%s extended=%s street=%s city=%s region=%s code=%s country=%s)" % (
            esc(Name_s(v.box)), esc(Name_s(v.extended)), esc(Name_s(v.street)),
            esc(Name_s(v.city)), esc(Name_s(v.region)), esc(Name_s(v.code)),
            esc(Name_s(v.country)))
    if isinstance(v, list):
        return "[" + ", ".join(esc(x) for x in v) + "]"
    return esc(v)


def Name_s(val):
    if isinstance(val, (list, tuple)):
        return " ".join(val)
    return val


def dump_component(comp, level=0):
    pre = "  " * (level + 1)
    print("%s%s" % (pre, comp.name))
    for child in comp.getSortedChildren():
        if isinstance(child, Component):
            dump_component(child, level + 1)
        else:
            ps = param_str(child.params)
            group = (child.group + ".") if child.group else ""
            tail = (" {%s}" % ps) if ps else ""
            print("%s  %s%s%s = %s" % (pre, group, child.name, tail, value_repr(child)))


def job_count(name, ext):
    transform = not name.endswith(".ics")
    try:
        comps = components(name, transform=transform)
        print("  %d component(s)" % len(comps))
        for c in comps:
            print("    %s with %d line(s)" % (c.name or "(unnamed)",
                                              sum(1 for _ in c.lines())))
    except ParseError as e:
        print("  ParseError: %s" % esc(str(e)))


def job_dump(name):
    transform = not name.endswith(".ics")
    for c in components(name, transform=transform):
        dump_component(c)


def job_fields(name):
    for i, c in enumerate(components(name)):
        fn = c.getChildValue("fn")
        n = c.contents.get("n")
        print("  card %d: FN=%s" % (i, esc(fn) if fn else "-"))
        for key in ("email", "tel", "adr", "org", "categories", "title", "url", "bday"):
            vals = c.contents.get(key)
            if not vals:
                continue
            for v in vals:
                print("    %s = %s" % (v.name, value_repr(v)))


def job_struct(name):
    for i, c in enumerate(components(name)):
        print("  card %d" % i)
        for n in c.contents.get("n", []):
            v = n.value
            print("    name given=%s family=%s" % (esc(Name_s(v.given)), esc(Name_s(v.family))))
        for a in c.contents.get("adr", []):
            v = a.value
            print("    addr %s / %s %s / %s" % (
                esc(Name_s(v.street)), esc(Name_s(v.city)), esc(Name_s(v.code)),
                esc(Name_s(v.country))))
        for o in c.contents.get("org", []):
            print("    org %s" % value_repr(o))


def job_roundtrip(name):
    transform = not name.endswith(".ics")
    comps = components(name, transform=transform)
    for i, c in enumerate(comps):
        out = c.serialize()
        reparsed = list(readComponents(out, transform=transform))
        print("  card %d serialized %d bytes, reparses to %d component(s)" % (
            i, len(out), len(reparsed)))
        for line in out.split("\r\n"):
            if line:
                print("  | " + esc(line))


def job_parse(name):
    transform = not name.endswith(".ics")
    try:
        comps = components(name, transform=transform)
        print("  parsed %d component(s)" % len(comps))
        for c in comps:
            print("    %s" % (c.name or "(unnamed)"))
    except ParseError as e:
        print("  ParseError: %s" % esc(str(e)))


def job_qp(name):
    c = components(name)[0]
    note = c.getChildValue("note")
    print("  decoded note: %s" % esc(note))
    for cc in components(name):
        n = cc.contents.get("n")
        if n:
            print("  N value: %s" % value_repr(n[0]))


def job_photo(name):
    c = components(name)[0]
    photo = c.contents.get("photo")
    if photo:
        p = photo[0]
        print("  photo encoding=%s bytes=%d" % (
            esc(p.params.get("ENCODING", ["-"])[0]), len(p.value)))


def job_build(kind):
    j = vobject.vCard()
    j.add("fn")
    if kind == "simple":
        j.fn.value = "Jordan Pat"
        j.add("email")
        j.email.value = "jordan@example.org"
        j.email.type_param = "INTERNET"
    else:
        j.fn.value = "Dr. Lin Wei"
        n = j.add("n")
        n.value = vobject.vcard.Name(family="Lin", given="Wei", prefix="Dr.")
        a = j.add("adr")
        a.value = vobject.vcard.Address(street="2 Garden Road", city="Singapore",
                                        code="049908", country="Singapore")
        o = j.add("org")
        o.value = ["Lin Wei Consulting", "Advisory"]
    out = j.serialize()
    for line in out.split("\r\n"):
        if line:
            print("  | " + esc(line))


def job_fold(width):
    from vobject.base import foldOneLine
    import io
    buf = io.StringIO()
    text = ("FN:" + "x" * 40 + " " + "y" * 40)
    foldOneLine(buf, text, int(width))
    for line in buf.getvalue().split("\r\n"):
        if line:
            print("  | " + esc(line))


def job_escape():
    from vobject.base import backslashEscape
    for s in ["a,b;c", "line\r\none\ntwo", "back\\slash", "plain"]:
        print("  %s -> %s" % (esc(s), esc(backslashEscape(s))))


def main():
    with open(os.path.join(DATA, "jobs.txt")) as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    for line in lines:
        words = line.split()
        print("== " + line)
        cmd = words[0]
        arg = words[1] if len(words) > 1 else ""
        if cmd == "count":
            job_count(arg, None)
        elif cmd == "dump":
            job_dump(arg)
        elif cmd == "fields":
            job_fields(arg)
        elif cmd == "struct":
            job_struct(arg)
        elif cmd == "roundtrip":
            job_roundtrip(arg)
        elif cmd == "parse":
            job_parse(arg)
        elif cmd == "qp":
            job_qp(arg)
        elif cmd == "photo":
            job_photo(arg)
        elif cmd == "build":
            job_build(arg)
        elif cmd == "fold":
            job_fold(arg)
        elif cmd == "escape":
            job_escape()


main()
