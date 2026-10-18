#!/usr/bin/env python3
"""Runs data/jobs.jsonl with the real tabulate (0.10.0, without the
optional wcwidth, so a width is a count of code points). A table job
calls tabulate() on a JSON table with the job's keyword arguments, a
format job formats numbers the way tabulate's floatfmt does, and a cli
job runs tabulate's command-line tool. mini_tabulate.kara prints the
same thing."""
import contextlib
import io
import json
import sys

import tabulate as tab
from tabulate import tabulate

assert tab.wcwidth is None


def err(e):
    msg = str(e)
    return "error: " + type(e).__name__ + (": " + msg if msg else "")


def run_table(j):
    data = json.load(open("data/tables/%s.json" % j.pop("table")))
    try:
        print(tabulate(data, **j))
    except Exception as e:
        print(err(e))


def run_format(j):
    for v in j["values"]:
        try:
            x = float(v) if isinstance(v, str) else v
            print("  " + format(x, j["format"]))
        except Exception as e:
            print("  " + err(e))


class Captured(io.StringIO):
    def close(self):
        pass


def run_cli(j):
    out = Captured()
    code = 0
    sys.argv = ["tabulate"] + j["cli"]
    with contextlib.redirect_stdout(out):
        try:
            tab._main()
        except SystemExit as e:
            code = e.code
    sys.stdout.write(out.getvalue())
    if code:
        print("exit %d" % code)


for line in open("data/jobs.jsonl").read().split("\n"):
    if not line:
        continue
    print("== " + line)
    j = json.loads(line)
    if "table" in j:
        run_table(j)
    elif "format" in j:
        run_format(j)
    else:
        run_cli(j)
