#!/usr/bin/env python3
"""Python 3.13's re over data/cases.tsv: writes expected.out's text to
stdout. Run mk.py first."""
import re

FLAGS = {"i": re.I, "m": re.M, "s": re.S, "x": re.X, "a": re.A}


def unescape(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] in "nt\\":
            out.append({"n": "\n", "t": "\t", "\\": "\\"}[s[i + 1]])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def subject(s):
    if s.startswith("@"):
        with open("data/" + s[1:], encoding="utf-8", newline="") as f:
            return f.read()
    return unescape(s)


def show_match(m):
    if m is None:
        print("  None")
        return
    print("  span=%r match=%r" % (m.span(), m.group(0)))
    if m.re.groups:
        print("  groups=%r" % (m.groups(),))
        print("  spans=%r" % ([m.span(i) for i in range(1, m.re.groups + 1)],))
    if m.re.groupindex:
        print("  named=%r" % (m.groupdict(),))


def run(f):
    op, pat, fl = f[0], f[1], f[2]
    flags = 0
    for ch in fl if fl != "-" else "":
        flags |= FLAGS[ch]
    r = re.compile(pat, flags)
    s = subject(f[3])
    if op == "compile":
        print("  groups=%d groupindex=%r" % (r.groups, dict(r.groupindex)))
    elif op in ("search", "match", "fullmatch"):
        show_match(getattr(r, op)(s))
    elif op == "findall":
        print("  %r" % (r.findall(s),))
    elif op == "finditer":
        for m in r.finditer(s):
            if r.groupindex:
                print("  %r %r" % (m.span(), m.groupdict()))
            else:
                print("  %r %r %r" % (m.span(), m.group(0), m.groups()))
    elif op == "sub":
        count = int(f[5]) if len(f) > 5 else 0
        print("  %r" % (r.subn(f[4], s, count=count),))
    elif op == "split":
        maxsplit = int(f[4]) if len(f) > 4 else 0
        print("  %r" % (r.split(s, maxsplit=maxsplit),))
    elif op == "tokens":
        line = 1
        for m in r.finditer(s):
            kind = m.lastgroup
            if kind == "NEWLINE":
                line += 1
            elif kind not in ("SKIP", "COMMENT"):
                print("  %d %s %r lastindex=%d" % (line, kind, m.group(), m.lastindex))


def main():
    with open("data/cases.tsv", encoding="utf-8") as f:
        cases = f.read().split("\n")[:-1]
    for case in cases:
        f = case.split("\t")
        print("== " + " | ".join(f))
        try:
            run(f)
        except re.error as e:
            print("  error: %s" % e)
        except Exception as e:
            print("  %s: %s" % (type(e).__name__, e))


main()
