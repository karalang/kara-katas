#!/usr/bin/env python3
"""Runs data/jobs.txt through Python 3.13's struct module; prints expected.out.

Each job is a Python expression (or `name = expr`). It prints `>>> job`,
then the result's repr, or `ExceptionType: message` when it raises.
Comment lines are printed as they are.
"""
import os, struct, sys
from struct import calcsize, pack, pack_into, unpack, unpack_from, iter_unpack, Struct

os.chdir("data")


def read(name):
    with open(name, "rb") as f:
        return f.read()


def unpack_file(fmt, name, offset):
    return unpack_from(fmt, read(name), offset)


def records(fmt, name):
    return list(iter_unpack(fmt, read(name)))


def names(name):
    data = read(name)
    magic, version, count = unpack_from(">4sBxH", data, 0)
    off = calcsize(">4sBxH")
    out = []
    for _ in range(count):
        (n,) = unpack_from(">H", data, off)
        off += 2
        (s,) = unpack_from(f">{n}s", data, off)
        off += n
        out.append(s)
    return out


env = dict(globals())
out = []
for line in read("jobs.txt").decode().splitlines():
    if line.startswith("#") or not line.strip():
        out.append(line)
        continue
    out.append(">>> " + line)
    target = None
    expr = line
    if " = " in line and line.split(" = ")[0].isidentifier():
        target, expr = line.split(" = ", 1)
    try:
        v = eval(expr, env)
        if target:
            env[target] = v
        else:
            out.append(repr(v))
    except Exception as e:
        out.append(f"{type(e).__name__}: {e}")
sys.stdout.write("\n".join(out) + "\n")
