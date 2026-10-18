#!/usr/bin/env python3
"""Python 3.13's plistlib over data/jobs.tsv: writes expected.out's text to
stdout. Run mk.py first."""
import plistlib


def read(name):
    with open("data/" + name, "rb") as f:
        return f.read()


def options(fields):
    kw = {}
    for f in fields:
        k, _, v = f.partition("=")
        kw[k] = v == "1"
    return kw


def fmt_name(data):
    if data[:8] == b"bplist00":
        return "binary"
    return "xml"


def hexdump(b):
    for i in range(0, len(b), 16):
        chunk = b[i:i + 16]
        print("  %06x  %s" % (i, " ".join("%02x" % c for c in chunk)))


def get(value, path):
    where = ""
    for p in path:
        if isinstance(value, dict):
            if p not in value:
                return "no key %r in %s" % (p, where or "the root")
            value = value[p]
        elif isinstance(value, list):
            i = int(p)
            if i >= len(value):
                return "index %d out of range in %s (%d items)" % (i, where or "the root", len(value))
            value = value[i]
        else:
            return "%s is a %s, not a container" % (where or "the root", type(value).__name__)
        where += "/" + p
    return repr(value)


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        jobs = f.read().splitlines()
    for job in jobs:
        f = job.split("\t")
        print("== " + " | ".join(f))
        data = read(f[1])
        try:
            value = plistlib.loads(data)
        except Exception as e:
            print("  %s: %s" % (type(e).__name__, e))
            continue
        try:
            if f[0] == "load":
                print("  %s %s" % (fmt_name(data), repr(value)))
            elif f[0] == "xml":
                out = plistlib.dumps(value, **options(f[2:]))
                for line in out.decode("utf-8").split("\n"):
                    print("  |" + line)
            elif f[0] == "bin":
                out = plistlib.dumps(value, fmt=plistlib.FMT_BINARY, **options(f[2:]))
                print("  %d bytes" % len(out))
                hexdump(out)
            elif f[0] == "roundtrip":
                x = plistlib.dumps(value)
                b = plistlib.dumps(value, fmt=plistlib.FMT_BINARY)
                vx = plistlib.loads(x)
                vb = plistlib.loads(b)
                print("  xml %d bytes, equal %s; binary %d bytes, equal %s; xml again same %s"
                      % (len(x), vx == value, len(b), vb == value, plistlib.dumps(vb) == x))
            elif f[0] == "get":
                print("  " + get(value, f[2:]))
        except Exception as e:
            print("  %s: %s" % (type(e).__name__, e))


main()
