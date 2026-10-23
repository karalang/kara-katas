#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored maidenhead library and writes
expected.out. API calls print one line, "<op>(<args>) => <repr of result>";
a cli job prints "cli(<args>):" followed by each line `python -m maidenhead`
would print, indented by two spaces (the module's main() function is called
directly, with the arguments argparse would have produced). A ValueError
prints as "ValueError: <message>". Run: python3 -I -B oracle.py > expected.out"""
import contextlib
import io
import json
import sys

sys.path.insert(0, "vendor")
import maidenhead  # noqa: E402

# __main__ parses sys.argv at import time; give it a valid one, and swallow
# what that first run prints, so that main() can then be called per job.
sys.argv = ["maidenhead", "AA00"]
with contextlib.redirect_stdout(io.StringIO()):
    from maidenhead import __main__ as cli  # noqa: E402


def api(f):
    op = f[0]
    if op == "maiden":
        return maidenhead.to_maiden(float(f[1]), float(f[2]), int(f[3]))
    if op == "loc":
        return repr(maidenhead.to_location(f[1], f[2] == "1"))
    if op == "rect":
        return repr(maidenhead.to_location_rect(f[1]))
    if op == "geo":
        return json.dumps(maidenhead.to_geoJSONObject(f[1], f[2] == "1", f[3] == "1"), indent=None)
    if op == "url":
        return maidenhead.google_maps(f[1], f[2] == "1")
    raise SystemExit("unknown op " + op)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if line == "":
        continue
    f = line.split("\t")
    if f[0] == "cli":
        loc = f[1]
        if "," in loc:
            loc = tuple(loc.split(","))
        flags = f[3]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                cli.main(loc, int(f[2]), "u" in flags, "c" in flags, "g" in flags, "n" in flags)
            text = buf.getvalue()
        except ValueError as e:
            text = buf.getvalue() + "ValueError: %s\n" % e
        out.append("cli(%s):" % ", ".join(f[1:]))
        for ln in text.split("\n")[:-1]:
            out.append("  " + ln)
        continue
    try:
        res = api(f)
    except ValueError as e:
        res = "ValueError: %s" % e
    out.append("%s(%s) => %s" % (f[0], ", ".join(f[1:]), res))
sys.stdout.write("\n".join(out) + "\n")
