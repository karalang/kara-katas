#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored pyrsistent PVector and writes
expected.out. Uses the pure-Python PythonPVector (python_pvector) explicitly,
so the oracle runs exactly the trie code mini_pyrsistent.kara mirrors — never
the optional C accelerator. See mk.py for the op table."""
import sys
sys.path.insert(0, "vendor")
from pyrsistent._pvector import python_pvector  # noqa: E402


def fmt_list(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


regs = []
out = []


def mkreg(v):
    regs.append(v)
    return "reg %d len %d" % (len(regs) - 1, len(v))


for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "iota":
        out.append(mkreg(python_pvector(range(int(f[1])))))
    elif op == "new":
        out.append(mkreg(python_pvector([int(x) for x in f[1:]])))
    elif op == "app":
        out.append(mkreg(regs[int(f[1])].append(int(f[2]))))
    elif op == "set":
        out.append(mkreg(regs[int(f[1])].set(int(f[2]), int(f[3]))))
    elif op == "ext":
        out.append(mkreg(regs[int(f[1])].extend([int(x) for x in f[2:]])))
    elif op == "extr":
        out.append(mkreg(regs[int(f[1])].extend(regs[int(f[2])])))
    elif op == "mset":
        args = [int(x) for x in f[2:]]
        out.append(mkreg(regs[int(f[1])].mset(*args)))
    elif op == "del":
        out.append(mkreg(regs[int(f[1])].delete(int(f[2]))))
    elif op == "dels":
        out.append(mkreg(regs[int(f[1])].delete(int(f[2]), int(f[3]))))
    elif op == "mul":
        out.append(mkreg(regs[int(f[1])] * int(f[2])))
    elif op == "get":
        out.append(str(regs[int(f[1])][int(f[2])]))
    elif op == "len":
        out.append(str(len(regs[int(f[1])])))
    elif op == "idx":
        v, val = regs[int(f[1])], int(f[2])
        out.append(str(v.index(val)) if val in v.tolist() else "miss")
    elif op == "cnt":
        out.append(str(regs[int(f[1])].count(int(f[2]))))
    elif op == "eq":
        out.append("yes" if regs[int(f[1])] == regs[int(f[2])] else "no")
    elif op == "lt":
        out.append("yes" if regs[int(f[1])] < regs[int(f[2])] else "no")
    elif op == "rng":
        out.append(fmt_list(regs[int(f[1])].tolist()[int(f[2]):int(f[3])]))
    elif op == "list":
        out.append(fmt_list(regs[int(f[1])].tolist()))
    elif op == "repr":
        out.append(repr(regs[int(f[1])]))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
