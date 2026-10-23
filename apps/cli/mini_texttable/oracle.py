#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored texttable 1.7.2, printing
what mini_texttable.kara must print.

Each line is one op (see mk.py). A job prints "== name"; an op prints
"> op <arguments as ascii()>". What the library writes to stderr prints
as "  stderr: <text>", an exception as "  error <Class>: <str(e)>" (with
no colon when the message is empty), and the job goes on. draw() prints
"  -> None" or each line of the table indented by four spaces.

The optional wcwidth and cjkwrap modules are not installed, so the
library measures characters with unicodedata and wraps with textwrap.

Run: python3 -I -B oracle.py > expected.out"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import texttable  # noqa: E402
from texttable import Texttable  # noqa: E402

assert texttable.textwrapper.__code__.co_names[0] == "textwrap"
assert "unicodedata" in texttable.uchar_width.__code__.co_names

OUT = []
SETTERS = {
    "chars": "set_chars", "header_align": "set_header_align",
    "align": "set_cols_align", "valign": "set_cols_valign",
    "dtype": "set_cols_dtype", "width": "set_cols_width",
    "header": "header", "row": "add_row",
}
SCALARS = {"max_width": "set_max_width", "deco": "set_deco",
           "precision": "set_precision"}


def emit(s):
    OUT.append(s)


def vis(s):
    return ascii(s)[1:-1]


def dec(w):
    if w == "n":
        return None
    t, v = w[0], w[2:]
    if t == "b":
        return v == "1"
    if t == "i":
        return int(v)
    if t == "f":
        return float(v)
    if t == "y":
        return bytes.fromhex(v)
    assert t == "s", w
    return bytes.fromhex(v).decode("utf-8")


def run(t, fields):
    name, args = fields[0], fields[1:]
    if name == "new":
        vals = [dec(a) for a in args]
        emit("> new" + "".join(" " + ascii(v) for v in vals))
        return Texttable(*vals)
    if name == "rows":
        header = dec(args[0])
        rs = [[]]
        for a in args[1:]:
            if a == "/":
                rs.append([])
            else:
                rs[-1].append(dec(a))
        if len(args) == 1:
            rs = []
        emit("> rows header=%s %s" % (header, ascii(rs)))
        t.add_rows(rs, header=header)
        return t
    if name == "draw":
        emit("> draw")
        s = t.draw()
        if s is None:
            emit("  -> None")
        else:
            for line in s.split("\n"):
                emit("    " + line)
        return t
    if name == "reset":
        emit("> reset")
        t.reset()
        return t
    if name in SCALARS:
        v = dec(args[0])
        emit("> %s %s" % (name, ascii(v)))
        getattr(t, SCALARS[name])(v)
        return t
    vals = [dec(a) for a in args]
    emit("> %s %s" % (name, ascii(vals)))
    getattr(t, SETTERS[name])(vals)
    return t


class Capture(io.StringIO):
    pass


def main():
    with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    t = None
    real_err = sys.stderr
    for line in lines:
        if not line:
            continue
        fields = line.split("\t")
        if fields[0] == "job":
            emit("== " + fields[1])
            t = Texttable()
            continue
        cap = Capture()
        sys.stderr = cap
        try:
            t = run(t, fields)
            failure = None
        except Exception as e:  # noqa: BLE001
            failure = e
        finally:
            sys.stderr = real_err
        for piece in cap.getvalue().split("\n")[:-1]:
            emit("  stderr: " + vis(piece))
        if failure is not None:
            msg = vis(str(failure))
            emit("  error " + type(failure).__name__ + (": " + msg if msg else ""))
    sys.stdout.buffer.write(("\n".join(OUT) + "\n").encode("utf-8"))


main()
