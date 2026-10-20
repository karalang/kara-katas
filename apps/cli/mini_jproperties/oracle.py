# Runs data/jobs.tsv through jproperties itself (vendor/, unchanged) and
# prints what each job gives; expected.out is this output.
import contextlib
import io
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True

import jproperties  # noqa: E402

DATA = os.path.join(HERE, "data")
# The tool prints the time; the jobs run with the clock stopped here.
FIXED = time.struct_time((2024, 3, 9, 14, 5, 7, 5, 69, 0))


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


def unesc(s):
    return s.replace("\\r", "\r").replace("\\n", "\n")


def load(name, enc, flags):
    p = jproperties.Properties("noescape" not in flags)
    with open(os.path.join(DATA, name), "rb") as f:
        p.load(f, enc, metadoc="metadoc" in flags)
    return p


def print_props(p):
    for k in p:
        print(show("%r = %r" % (k, p[k].data)))
        m = p.getmeta(k)
        if m:
            print(show("  meta %r" % (m,)))


def load_job(args):
    name, enc, flags = args[0], args[1], args[2:]
    p = jproperties.Properties("noescape" not in flags)
    try:
        with open(os.path.join(DATA, name), "rb") as f:
            p.load(f, enc, metadoc="metadoc" in flags)
    except Exception as e:
        print(err(e))
    print("%d properties" % len(p))
    print_props(p)


def dump(p, enc, strict, strip_meta, comments=None):
    buf = io.BytesIO()
    try:
        p.store(buf, comments, enc, strict, strip_meta, timestamp=False)
    except Exception as e:
        print(err(e))
    b = buf.getvalue()
    print("%d bytes" % len(b))
    for line in b.decode(enc).split("\n"):
        print("| " + show(line))


def store_job(args):
    name, in_enc, out_enc, mode, flags = args[0], args[1], args[2], args[3], args[4:]
    comments = None
    for fl in flags:
        if fl.startswith("comments="):
            comments = unesc(fl[len("comments="):])
    p = load(name, in_enc, flags)
    dump(p, out_enc, mode == "strict", "meta" not in flags, comments)


def edit_job(args):
    p = load(args[0], "utf-8", [])
    try:
        for op in args[1:]:
            kind, rest = op.split(":", 1)
            if kind == "set":
                k, v = rest.split("=", 1)
                p[k] = v
            elif kind == "del":
                del p[rest]
            else:
                k, pairs = rest.split(":", 1)
                m = {}
                for pair in pairs.split(","):
                    a, b = pair.split("=", 1)
                    m[a] = b
                p.setmeta(k, m)
    except Exception as e:
        print(err(e))
    dump(p, "utf-8", False, False)


class Out:
    def __init__(self):
        self.buffer = io.BytesIO()

    def write(self, s):
        self.buffer.write(s.encode("utf-8"))

    def flush(self):
        pass


def tool_job(args):
    out = Out()
    errs = io.StringIO()
    old = sys.argv, sys.stdout, time.gmtime
    sys.argv = ["jproperties"] + args
    time.gmtime = lambda: FIXED
    cwd = os.getcwd()
    os.chdir(DATA)
    try:
        with contextlib.redirect_stderr(errs):
            sys.stdout = out
            code = jproperties.main()
    finally:
        sys.argv, sys.stdout, time.gmtime = old
        os.chdir(cwd)
    enc = args[2] if len(args) > 2 else "utf-8"
    b = out.buffer.getvalue()
    if b:
        print("stdout %d bytes" % len(b))
        for line in b.decode(enc).split("\n"):
            print("| " + show(line))
    e = errs.getvalue()
    if e:
        for line in e[:-1].split("\n"):
            print("! " + line)
    print("exit %d" % code)


def main():
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
        jobs = [line.rstrip("\n").split("\t") for line in f]
    for job in jobs:
        print("== " + show(" ".join(job)))
        {"load": load_job, "store": store_job, "edit": edit_job, "tool": tool_job}[job[0]](job[1:])
        sys.stdout.flush()


main()
