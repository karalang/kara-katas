#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored ftfy 6.3.1, printing what
mini_ftfy.kara must print.

Each op prints "> <function>(<args>)" with its arguments as repr() shows
them, then "  -> <repr of the result>" or "  error <Class>: <str(e)>". A
job prints "== name". Warnings (a deprecated octal escape) are not part
of the output.

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import ftfy  # noqa: E402
from ftfy import badness, chardata, fixes  # noqa: E402
from html.entities import html5  # noqa: E402

warnings.simplefilter("ignore")
OUT = []


def dec(w):
    if w == "n":
        return None
    t, v = w.split(":", 1)
    if t == "b":
        return v == "1"
    if t == "i":
        return int(v)
    if t == "s":
        return bytes.fromhex(v).decode("utf-8")
    if t == "y":
        return bytes.fromhex(v)
    assert t == "p", w
    return [tuple(step.split(",", 1)) for step in v.split(";") if step]


def lookup(name):
    if name.startswith("fixes."):
        return getattr(fixes, name[6:])
    if name.startswith("badness."):
        return getattr(badness, name[8:])
    return getattr(ftfy, name)


def table(name):
    """The two tables chardata builds at import time, shown so the port's
    builders are checked entry by entry: WIDTH_MAP in full, and the
    all-caps names HTML_ENTITIES adds to the html5 names."""
    OUT.append("> chardata." + name)
    if name == "WIDTH_MAP":
        items = sorted(chardata.WIDTH_MAP.items())
        OUT.append("  -> %d entries" % len(items))
        OUT.extend("  0x%04x: %r" % kv for kv in items)
        return
    items = sorted(chardata.HTML_ENTITIES.items())
    OUT.append("  -> %d entries" % len(items))
    OUT.extend("  %r: %r" % kv for kv in items if kv[0][1:] not in html5)


def main():
    with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as fh:
        lines = [ln for ln in fh.read().split("\n") if ln]
    for line in lines:
        f = line.split("\t")
        if f[0] == "job":
            OUT.append("== " + f[1])
            continue
        if f[0] == "table":
            table(f[1])
            continue
        args, kwargs, shown = [], {}, []
        for w in f[1:]:
            name, eq, rest = w.partition("=")
            if eq and name.replace("_", "").isalnum() and ":" not in name:
                kwargs[name] = dec(rest)
                shown.append("%s=%r" % (name, kwargs[name]))
            else:
                args.append(dec(w))
                shown.append(repr(args[-1]))
        OUT.append("> %s(%s)" % (f[0], ", ".join(shown)))
        try:
            r = lookup(f[0])(*args, **kwargs)
            OUT.append("  -> " + repr(r))
        except Exception as e:  # noqa: BLE001
            OUT.append("  error %s: %s" % (type(e).__name__, e))
    sys.stdout.buffer.write(("\n".join(OUT) + "\n").encode("utf-8"))


main()
