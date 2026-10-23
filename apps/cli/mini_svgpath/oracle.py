#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py) through the vendored svg.path and
prints what each step gives: values as repr() shows them, an exception as
"error <class>: <message>". The plotter writes its G-code under data/out/
and prints each file back after "  |".

Run: python3 -I -B oracle.py > expected.out"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
from svg.path import Move, parse_path  # noqa: E402
from svg.path.parser import _tokenize_path  # noqa: E402

DATA = os.path.join(HERE, "data")


def unesc(t):
    out = []
    k = 0
    while k < len(t):
        c = t[k]
        if c == "\\" and k + 1 < len(t):
            n = t[k + 1]
            out.append({"\\": "\\", "t": "\t", "n": "\n", "r": "\r"}.get(n, "\\" + n))
            k += 2
        else:
            out.append(c)
            k += 1
    return "".join(out)


def num(f):
    if "." in f or "e" in f or "E" in f:
        return float(f)
    return int(f)


def svg_paths(text):
    """Every <path> element's attributes, in order: a small scanner for
    name="value" and name='value' pairs, enough for the drawings here."""
    out = []
    k = text.find("<path")
    while k >= 0:
        k += 5
        if k < len(text) and text[k] not in " \t\r\n/>":
            k = text.find("<path", k)
            continue
        attrs = {}
        while k < len(text):
            while k < len(text) and text[k] in " \t\r\n":
                k += 1
            if k >= len(text) or text[k] in "/>":
                break
            s = k
            while k < len(text) and text[k] not in " \t\r\n=/>":
                k += 1
            name = text[s:k]
            while k < len(text) and text[k] in " \t\r\n":
                k += 1
            if k >= len(text) or text[k] != "=":
                attrs[name] = ""
                continue
            k += 1
            while k < len(text) and text[k] in " \t\r\n":
                k += 1
            q = text[k]
            e = text.find(q, k + 1)
            attrs[name] = text[k + 1:e]
            k = e + 1
        out.append(attrs)
        k = text.find("<path", k)
    return out


def plot(w, name, out_name):
    w("> plot svg/%s\n" % name)
    with open(os.path.join(DATA, "svg", name), encoding="utf-8") as f:
        text = f.read()
    lines = ["; %s, drawn by svg.path\n" % name]
    total = 0.0
    for n, attrs in enumerate(svg_paths(text), 1):
        pid = attrs.get("id", "path%d" % n)
        if "d" not in attrs:
            w("  %s: no d attribute\n" % pid)
            lines.append("; %s: no d\n" % pid)
            continue
        try:
            p = parse_path(attrs["d"])
            length = p.length(error=1e-6)
            box = p.boundingbox()
            gcode = []
            for seg in p:
                if isinstance(seg, Move):
                    gcode.append("G0 X%.3f Y%.3f\n" % (seg.end.real, seg.end.imag))
                    continue
                steps = max(1, min(24, math.ceil(seg.length(error=1e-6) / 4)))
                for k in range(1, steps + 1):
                    q = seg.point(k / steps)
                    gcode.append("G1 X%.3f Y%.3f\n" % (q.real, q.imag))
        except Exception as e:
            w("  %s: error %s: %s\n" % (pid, type(e).__name__, e))
            lines.append("; %s: skipped\n" % pid)
            continue
        total += length
        w("  %s: %d segments, length %r, bbox %r\n" % (pid, len(p), length, box))
        lines.append("; %s\n" % pid)
        lines.extend(gcode)
    lines.append("; total length %.3f\n" % total)
    os.makedirs(os.path.join(DATA, "out"), exist_ok=True)
    path = os.path.join(DATA, "out", out_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    with open(path, encoding="utf-8") as f:
        back = f.read()
    w("  wrote out/%s (%d lines, total length %r)\n" % (out_name, len(lines), total))
    for line in back.split("\n")[:-1]:
        w("  | %s\n" % line)


def run(w, st, f):
    op = f[0]
    cur = st.get("cur")
    if op == "parse":
        d = unesc(f[1])
        w("> parse_path(%r)\n" % d)
        st["cur"] = None
        p = parse_path(d)
        st["cur"] = p
        w("  -> %r\n" % p)
        w("  d: %s\n" % p.d())
    elif op == "tokens":
        d = unesc(f[1])
        w("> _tokenize_path(%r)\n" % d)
        for t in _tokenize_path(d):
            w("  - %r\n" % (t,))
    elif op == "point":
        w("> point(%s)\n" % f[1])
        w("  -> %r\n" % cur.point(num(f[1])))
    elif op == "tangent":
        w("> tangent(%s)\n" % f[1])
        w("  -> %r\n" % cur.tangent(num(f[1])))
    elif op == "length":
        if len(f) == 1:
            w("> length()\n")
            w("  -> %r\n" % cur.length())
        elif len(f) == 2:
            w("> length(error=%s)\n" % f[1])
            w("  -> %r\n" % cur.length(error=num(f[1])))
        else:
            w("> length(error=%s, min_depth=%s)\n" % (f[1], f[2]))
            w("  -> %r\n" % cur.length(error=num(f[1]), min_depth=num(f[2])))
    elif op == "bbox":
        w("> boundingbox()\n")
        w("  -> %r\n" % cur.boundingbox())
    elif op == "seg":
        i, what = int(f[1]), f[2]
        if len(f) > 3:
            w("> [%d].%s(%s)\n" % (i, what, f[3]))
        else:
            w("> [%d].%s()\n" % (i, what))
        seg = cur[i]
        if what == "repr":
            w("  -> %r\n" % seg)
        elif what == "point":
            w("  -> %r\n" % seg.point(num(f[3])))
        elif what == "tangent":
            w("  -> %r\n" % seg.tangent(num(f[3])))
        elif what == "length":
            w("  -> %r\n" % seg.length())
        elif what == "bbox":
            w("  -> %r\n" % seg.boundingbox())
    elif op == "keep":
        st["saved"][f[1]] = cur
        w("> keep as %s\n" % f[1])
    elif op == "use":
        st["cur"] = st["saved"][f[1]]
        w("> use %s\n" % f[1])
    elif op == "eq":
        other = st["saved"][f[1]]
        w("> == %s, != %s\n" % (f[1], f[1]))
        w("  -> %r %r\n" % (cur == other, cur != other))
    elif op in ("append", "remove", "index", "count", "has"):
        w("> %s(%s[%s])\n" % (op, f[1], f[2]))
        seg = st["saved"][f[1]][int(f[2])]
        if op == "append":
            cur.append(seg)
        elif op == "remove":
            cur.remove(seg)
        elif op == "index":
            w("  -> %r\n" % cur.index(seg))
        elif op == "count":
            w("  -> %r\n" % cur.count(seg))
        else:
            w("  -> %r\n" % (seg in cur))
    elif op in ("insert", "set"):
        at = int(f[1])
        w("> %s(%d, %s[%s])\n" % (op, at, f[2], f[3]))
        seg = st["saved"][f[2]][int(f[3])]
        if op == "insert":
            cur.insert(at, seg)
        else:
            cur[at] = seg
    elif op == "del":
        w("> del [%s]\n" % f[1])
        del cur[int(f[1])]
    elif op == "pop":
        if len(f) > 1:
            w("> pop(%s)\n" % f[1])
            w("  -> %r\n" % cur.pop(int(f[1])))
        else:
            w("> pop()\n")
            w("  -> %r\n" % cur.pop())
    elif op == "reverse":
        w("> reverse()\n")
        cur.reverse()
    elif op == "slice":
        w("> [%s:%s]\n" % (f[1], f[2]))
        w("  -> %r\n" % cur[int(f[1]):int(f[2])])
    elif op == "len":
        w("> len()\n")
        w("  -> %d\n" % len(cur))
    elif op == "clear":
        w("> clear()\n")
        cur.clear()
    elif op == "plot":
        plot(w, f[1], f[2])


def main():
    w = sys.stdout.write
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as fh:
        steps = fh.read().split("\n")
    st = {"cur": None, "saved": {}}
    for line in steps:
        if not line:
            continue
        f = line.split("\t")
        if f[0] == "job":
            w("== %s\n" % f[1])
            continue
        try:
            run(w, st, f)
        except Exception as e:
            w("  error %s: %s\n" % (type(e).__name__, e))


main()
