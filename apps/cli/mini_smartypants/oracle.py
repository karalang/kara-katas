#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py) through the vendored smartypants and
prints what each step gives: a string as repr() shows it, a rendered post
or the command's output line by line after "  |", the command's standard
error after "  !" and its exit status.

Run: python3 -I -B oracle.py > expected.out"""
import contextlib
import io
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import smartypants  # noqa: E402

DATA = os.path.join(HERE, "data")
DEFAULT_SKIP = list(smartypants.tags_to_skip)


def unesc(t):
    out = []
    k = 0
    while k < len(t):
        c = t[k]
        if c == "\\" and k + 1 < len(t):
            n = t[k + 1]
            out.append({"\\": "\\", "t": "\t", "n": "\n"}.get(n, "\\" + n))
            k += 2
        else:
            out.append(c)
            k += 1
    return "".join(out)


def attr(f):
    return None if f == "-" else int(f)


def lines(w, text, mark):
    if not text:
        return
    for line in text.split("\n"):
        w("  %s%s\n" % (mark, " " + line if line else ""))


def cli(args, w):
    out, err = io.StringIO(), io.StringIO()
    code = 0
    old = os.getcwd()
    os.chdir(DATA)
    sys.argv = ["smartypants"] + args
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            runpy.run_path(os.path.join(HERE, "vendor", "smartypants"), run_name="__main__")
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    finally:
        os.chdir(old)
    lines(w, out.getvalue(), "|")
    lines(w, err.getvalue(), "!")
    w("  exit %d\n" % code)


def main():
    w = sys.stdout.write
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as fh:
        steps = fh.read().split("\n")
    for line in steps:
        if not line:
            continue
        f = line.split("\t")
        op = f[0]
        if op == "job":
            w("== %s\n" % f[1])
        elif op == "sp":
            text, a = unesc(f[1]), attr(f[2])
            w("> smartypants(%r, %r)\n" % (text, a))
            w("  -> %r\n" % smartypants.smartypants(text, a))
        elif op == "fn":
            name = f[1]
            if name == "_tags_to_skip_regex":
                tags = None if f[2] == "-" else f[2].split(",")
                w("> %s(%r)\n" % (name, tags))
                w("  -> %r\n" % smartypants._tags_to_skip_regex(tags).pattern)
                continue
            text = unesc(f[2])
            args = [text] + ([int(f[3])] if len(f) > 3 else [])
            w("> %s(%s)\n" % (name, ", ".join(repr(x) for x in args)))
            w("  -> %r\n" % (getattr(smartypants, name)(*args),))
        elif op == "default":
            smartypants.Attr.default = int(f[1])
            w("> Attr.default = %s\n" % f[1])
        elif op == "skip":
            smartypants.tags_to_skip = DEFAULT_SKIP if f[1] == "-" else f[1].split(",")
            w("> tags_to_skip = %r\n" % (smartypants.tags_to_skip,))
        elif op == "file":
            a = attr(f[2])
            with open(os.path.join(DATA, "posts", f[1]), encoding="utf-8") as src:
                text = src.read()
            w("> file %s attr=%r\n" % (f[1], a))
            lines(w, smartypants.smartypants(text, a), "|")
        elif op == "cli":
            args = ["" if x == "''" else x for x in f[1:]]
            w("> smartypants %s\n" % " ".join(x if x else "''" for x in args))
            cli(args, w)


main()
