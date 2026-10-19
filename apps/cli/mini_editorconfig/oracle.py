# The reference run for mini_editorconfig: the same jobs through the real
# EditorConfig Python core 0.17.1 on Python 3.13. An `ec` job runs the
# library's own command line (editorconfig/__main__.py) with data/root
# standing in for /, and a `glob` job runs its fnmatch module on a
# section pattern and some names.
import json
import os
import sys

import editorconfig.__main__ as cli
from editorconfig import fnmatch as ecf

D = "data"
R = os.path.abspath(os.path.join(D, "root"))
OUT = []


def say(s=""):
    OUT.append(s)


class Capture:
    def __init__(self, tag, sink):
        self.tag = tag
        self.sink = sink
        self.buf = ""

    def write(self, s):
        self.buf += s
        while "\n" in self.buf:
            line, self.buf = self.buf.split("\n", 1)
            self.sink.append((self.tag, line))

    def flush(self):
        pass


def ec(args):
    say("== $ editorconfig " + " ".join(args))
    lines = []
    out, err = Capture("", lines), Capture("stderr: ", lines)
    real = [R + a if a.startswith("/") else a for a in args]
    saved = sys.stdout, sys.stderr, sys.argv
    sys.stdout, sys.stderr, sys.argv = out, err, ["editorconfig"] + real
    code = 0
    try:
        cli.main()
    except SystemExit as e:
        if e.code is None:
            code = 0
        elif isinstance(e.code, int):
            code = e.code
        else:
            err.write(str(e.code) + "\n")
            code = 1
    except Exception as e:
        lines.append(("", "uncaught %s: %s" % (type(e).__name__, e)))
        code = 1
    finally:
        sys.stdout, sys.stderr, sys.argv = saved
    for tag, line in lines:
        say(tag + line.replace(R, ""))
    if code:
        say("exit %d" % code)


def glob(pat, names):
    say("== glob " + json.dumps(pat, ensure_ascii=False))
    res, groups = ecf.translate(pat)
    say("regex: " + res)
    if groups:
        say("ranges: " + " ".join("%d..%d" % g for g in groups))
    hits = []
    for n in names:
        try:
            r = "yes" if ecf.fnmatch(n, pat) else "no"
        except Exception as e:
            r = "%s: %s" % (type(e).__name__, e)
        if len(names) <= 8:
            say("  %s -> %s" % (json.dumps(n, ensure_ascii=False), r))
        elif r != "no":
            hits.append(n if r == "yes" else "%s (%s)" % (n, r))
    if len(names) > 8:
        say("  %d of %d match" % (len(hits), len(names)) + "".join(("; " if i else ": ") + h for i, h in enumerate(hits)))


with open(os.path.join(D, "jobs.jsonl"), encoding="utf-8") as f:
    jobs = [json.loads(l) for l in f if l.strip()]
for j in jobs:
    if j[0] == "ec":
        ec(j[1])
    else:
        glob(j[1], j[2])
sys.stdout.write("\n".join(OUT) + "\n")
