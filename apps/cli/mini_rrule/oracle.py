#!/usr/bin/env python3
"""Runs every data/rules/*.rrule through the real dateutil (2.9.0):
rrulestr parses the rule lines, then each query line runs on the result.
mini_rrule.kara prints the same thing."""
import datetime
import itertools
import os
import warnings

from dateutil.rrule import rrulestr

warnings.simplefilter("ignore")


def dt(s):
    if "T" in s:
        return datetime.datetime.strptime(s, "%Y%m%dT%H%M%S")
    return datetime.datetime.strptime(s, "%Y%m%d")


def show(v):
    if isinstance(v, list):
        if not v:
            return ["  []"]
        return ["  " + str(x) for x in v]
    return ["  " + str(v)]


def query(r, q):
    w = q.split()
    inc = w[-1] == "inc"
    if w[0] == "all":
        return show(list(r))
    if w[0] == "list":
        return show(list(itertools.islice(r, int(w[1]))))
    if w[0] == "count":
        return show(r.count())
    if w[0] == "after":
        return show(r.after(dt(w[1]), inc=inc))
    if w[0] == "before":
        return show(r.before(dt(w[1]), inc=inc))
    if w[0] == "between":
        return show(r.between(dt(w[1]), dt(w[2]), inc=inc))
    if w[0] == "xafter":
        return show(list(r.xafter(dt(w[1]), count=int(w[2]), inc=inc)))
    if w[0] == "in":
        return show(dt(w[1]) in r)
    if w[0] == "at":
        try:
            return show(r[int(w[1])])
        except IndexError:
            return ["  error: index out of range"]
    if w[0] == "str":
        return ["  " + line for line in str(r).split("\n")]
    raise SystemExit("bad query " + q)


for name in sorted(os.listdir("data/rules")):
    text = open("data/rules/" + name).read()
    print("== " + name)
    lines = text.split("\n")
    opts = {}
    if lines[0].startswith("@"):
        for o in lines[0][1:].split():
            opts[o] = True
        lines = lines[1:]
    cut = lines.index("--")
    src = "\n".join(lines[:cut])
    try:
        r = rrulestr(src, **opts)
    except ValueError as e:
        print("  error: " + str(e))
        continue
    print("  " + ("set" if type(r).__name__ == "rruleset" else "rule"))
    for q in lines[cut + 1:]:
        if not q:
            continue
        print("> " + q)
        try:
            out = query(r, q)
        except ValueError as e:
            out = ["  error: " + str(e)]
        print("\n".join(out))
