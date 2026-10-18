#!/usr/bin/env python3
"""Python 3.13's pprint over data/jobs.tsv: writes expected.out's text to
stdout. Run mk.py first."""
import ast
import pprint


def source(arg):
    if arg.startswith("@"):
        with open("data/" + arg[1:], encoding="utf-8") as f:
            return f.read()
    return arg


def options(fields):
    kw = {}
    for f in fields:
        k, _, v = f.partition("=")
        if k in ("compact", "sort_dicts", "underscore_numbers"):
            kw[k] = v == "1"
        else:
            kw[k] = int(v)
    return kw


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        jobs = f.read().splitlines()
    for job in jobs:
        f = job.split("\t")
        print("== " + " | ".join(f))
        obj = ast.literal_eval(source(f[1]))
        kw = options(f[2:])
        try:
            p = pprint.PrettyPrinter(**kw)
        except ValueError as e:
            print("  ValueError: %s" % e)
            continue
        if f[0] == "pformat":
            for line in p.pformat(obj).split("\n"):
                print("  |" + line)
        elif f[0] == "saferepr":
            print("  " + pprint.saferepr(obj))
        elif f[0] == "readable":
            print("  readable %s recursive %s" % (p.isreadable(obj), p.isrecursive(obj)))


main()
