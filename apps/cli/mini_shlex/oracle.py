#!/usr/bin/env python3
"""Runs data/jobs.tsv through Python 3.13's shlex, fnmatch and glob; prints
expected.out. Each job prints `== ` and its fields joined by ` | `, then
its output. In a field, "⏎" is a newline and "⇥" a tab."""
import fnmatch, glob, shlex, sys


def field(s):
    return s.replace("⏎", "\n").replace("⇥", "\t")


def run(f):
    cmd, args = f[0], [field(x) for x in f[1:]]
    if cmd == "split":
        try:
            return repr(shlex.split(args[2], comments=args[1] == "1", posix=args[0] == "1"))
        except ValueError as e:
            return f"ValueError: {e}"
    if cmd == "lex":
        opts = [o for o in args[0].split(",") if o]
        punct = False
        for o in opts:
            if o == "punct":
                punct = True
            elif o.startswith("punct="):
                punct = o[len("punct="):]
        lx = shlex.shlex(args[1], posix="posix" in opts, punctuation_chars=punct)
        if "ws" in opts:
            lx.whitespace_split = True
        if "nocomment" in opts:
            lx.commenters = ""
        try:
            toks = list(lx)
        except ValueError as e:
            return f"ValueError: {e}"
        return f"{toks!r} (line {lx.lineno})"
    if cmd == "quote":
        return repr(shlex.quote(args[0]))
    if cmd == "join":
        return repr(shlex.join(args))
    if cmd == "fnmatch":
        return f"{fnmatch.fnmatch(args[0], args[1])} {fnmatch.fnmatchcase(args[0], args[1])}"
    if cmd == "filter":
        return repr(fnmatch.filter(args[1:], args[0]))
    if cmd == "glob":
        got = sorted(glob.glob(args[0], root_dir="tree", recursive=args[1] == "1",
                               include_hidden=args[2] == "1"))
        return "".join(f"  {p}\n" for p in got) + f"({len(got)} paths)"
    if cmd == "escape":
        return repr(glob.escape(args[0]))
    raise SystemExit(f"unknown job {cmd}")


import os
os.chdir("data")
out = []
with open("jobs.tsv", encoding="utf-8") as fh:
    for line in fh:
        f = line.rstrip("\n").split("\t")
        out.append("== " + " | ".join(f))
        out.append(run(f))
sys.stdout.write("\n".join(out) + "\n")
