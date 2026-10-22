#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored colorama, prints expected.out."""
import io
import sys

sys.path.insert(0, "vendor")
from colorama import Fore, Back, Style, Cursor  # noqa: E402
from colorama.ansi import set_title, clear_screen, clear_line  # noqa: E402
from colorama.ansitowin32 import AnsiToWin32  # noqa: E402


def strip(text):
    buf = io.StringIO()
    AnsiToWin32(buf, strip=True, convert=False).write(text)
    return buf.getvalue()


def run(op, arg):
    if op == "fore":
        return getattr(Fore, arg)
    if op == "back":
        return getattr(Back, arg)
    if op == "style":
        return getattr(Style, arg)
    if op == "title":
        return set_title(arg)
    if op == "clearscreen":
        return clear_screen(int(arg))
    if op == "clearline":
        return clear_line(int(arg))
    if op == "cursorup":
        return Cursor.UP(int(arg))
    if op == "cursordown":
        return Cursor.DOWN(int(arg))
    if op == "cursorfwd":
        return Cursor.FORWARD(int(arg))
    if op == "cursorback":
        return Cursor.BACK(int(arg))
    if op == "pos":
        x, y = arg.split(";")
        return Cursor.POS(int(x), int(y))
    if op == "combo":
        return Fore.RED + Style.BRIGHT + "ERROR" + Style.RESET_ALL + " ok"
    if op == "strip":
        return strip(arg)
    return "?"


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        op = f[0]
        arg = f[1] if len(f) > 1 else ""
        out.append("== " + " | ".join(f))
        out.append("  " + run(op, arg))
sys.stdout.write("\n".join(out) + "\n")
