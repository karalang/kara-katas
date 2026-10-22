#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored isoweek, prints expected.out.

Each job is tab-separated: an op name followed by its arguments. Output per job:
  == <op> | <args joined by space>
    <result>            (or `ValueError: <msg>`)

Dates print as date.isoformat() (YYYY-MM-DD); a Week prints as str(Week).
"""
import sys
from datetime import date

sys.path.insert(0, "vendor")
from isoweek import Week  # noqa: E402


def run(fields):
    op = fields[0]
    a = fields[1:]
    if op == "str":
        return str(Week(int(a[0]), int(a[1])))
    if op == "repr":
        return repr(Week(int(a[0]), int(a[1])))
    if op == "year_week":
        w = Week(int(a[0]), int(a[1]))
        return "%d %d" % w.year_week()
    if op == "fromstring":
        return str(Week.fromstring(a[0]))
    if op == "withdate":
        return str(Week.withdate(date(int(a[0]), int(a[1]), int(a[2]))))
    if op == "day":
        return Week(int(a[0]), int(a[1])).day(int(a[2])).isoformat()
    if op == "monday":
        return Week(int(a[0]), int(a[1])).monday().isoformat()
    if op == "sunday":
        return Week(int(a[0]), int(a[1])).sunday().isoformat()
    if op == "days":
        return " ".join(d.isoformat() for d in Week(int(a[0]), int(a[1])).days())
    if op == "toordinal":
        return str(Week(int(a[0]), int(a[1])).toordinal())
    if op == "fromordinal":
        return str(Week.fromordinal(int(a[0])))
    if op == "add":
        return str(Week(int(a[0]), int(a[1])) + int(a[2]))
    if op == "sub_int":
        return str(Week(int(a[0]), int(a[1])) - int(a[2]))
    if op == "sub_week":
        return str(Week(int(a[0]), int(a[1])) - Week(int(a[2]), int(a[3])))
    if op == "contains":
        w = Week(int(a[0]), int(a[1]))
        return str(w.contains(date(int(a[2]), int(a[3]), int(a[4]))))
    if op == "replace_week":
        return str(Week(int(a[0]), int(a[1])).replace(week=int(a[2])))
    if op == "replace_year":
        return str(Week(int(a[0]), int(a[1])).replace(year=int(a[2])))
    if op == "last_week_of_year":
        return str(Week.last_week_of_year(int(a[0])))
    if op == "weeks_of_year":
        ws = list(Week.weeks_of_year(int(a[0])))
        return "%d %s %s" % (len(ws), str(ws[0]), str(ws[-1]))
    raise SystemExit("unknown op: " + op)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().split("\n"):
        if line == "":
            continue
        fields = line.split("\t")
        out.append("== " + fields[0] + " | " + " ".join(fields[1:]))
        try:
            res = run(fields)
        except ValueError as e:
            res = "ValueError: " + str(e)
        out.append("  " + res)

sys.stdout.write("\n".join(out) + "\n")
