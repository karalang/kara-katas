#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored utm library and writes
expected.out. numpy is blocked so the library takes its `math` path (its
documented fallback, and the only one on scalars). API calls print one line,
"<op>(<args>) => <repr of result>", or "<ExceptionType>: <message>" when the
call raises. A cli job runs vendor/utm-converter with that command line and
prints "cli(<args>):" followed by each line it writes, indented two spaces.
Run: python3 -I -B oracle.py > expected.out"""
import contextlib
import io
import runpy
import sys

sys.modules["numpy"] = None  # import numpy -> ImportError
sys.path.insert(0, "vendor")
import utm  # noqa: E402
from utm import conversion  # noqa: E402

assert not conversion.use_numpy


def val(s):
    if s == "None":
        return None
    if s == "True":
        return True
    if s == "False":
        return False
    return s


def opt_int(s):
    return None if s == "None" else int(s)


def call(f):
    op = f[0]
    if op == "fl":
        return utm.from_latlon(float(f[1]), float(f[2]), opt_int(f[3]), val(f[4]), val(f[5]))
    if op == "tl":
        return utm.to_latlon(float(f[1]), float(f[2]), int(f[3]), val(f[4]), val(f[5]), val(f[6]))
    if op == "zl":
        return utm.latitude_to_zone_letter(float(f[1]))
    if op == "zn":
        return utm.latlon_to_zone_number(float(f[1]), float(f[2]))
    if op == "cl":
        return utm.zone_number_to_central_longitude(int(f[1]))
    if op == "cz":
        return utm.zone_letter_to_central_latitude(f[1])
    if op == "cv":
        return utm.check_valid_zone(int(f[1]), f[2])
    raise SystemExit("unknown op " + op)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if line == "":
        continue
    f = line.split("\t")
    if f[0] == "cli":
        sys.argv = ["utm-converter"] + f[1:]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                runpy.run_path("vendor/utm-converter", run_name="__main__")
        except SystemExit:
            pass
        out.append("cli(%s):" % ", ".join(f[1:]))
        for ln in buf.getvalue().split("\n")[:-1]:
            out.append("  " + ln)
        continue
    try:
        res = repr(call(f))
    except Exception as e:
        res = "%s: %s" % (type(e).__name__, e)
    out.append("%s(%s) => %s" % (f[0], ", ".join(f[1:]), res))
print("\n".join(out))
