#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored ordered_set and writes
expected.out. The vendored ordered_set is a single pure-Python module with no
required dependencies, so the oracle runs exactly the OrderedSet code
mini_ordered_set.kara mirrors. See mk.py for the op table."""
import sys
sys.path.insert(0, "vendor")
from ordered_set import OrderedSet  # noqa: E402


def fmt_list(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


regs = []
out = []


def mkreg(s):
    regs.append(s)
    return "reg %d = %s" % (len(regs) - 1, repr(s))


for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "new":
        out.append(mkreg(OrderedSet([int(x) for x in f[1:]])))
    elif op == "union":
        base = regs[int(f[1])]
        others = [regs[int(x)] for x in f[2:]]
        out.append(mkreg(base.union(*others)))
    elif op == "inter":
        base = regs[int(f[1])]
        others = [regs[int(x)] for x in f[2:]]
        out.append(mkreg(base.intersection(*others)))
    elif op == "diff":
        base = regs[int(f[1])]
        others = [regs[int(x)] for x in f[2:]]
        out.append(mkreg(base.difference(*others)))
    elif op == "symdiff":
        out.append(mkreg(regs[int(f[1])].symmetric_difference(regs[int(f[2])])))
    elif op == "add":
        out.append(str(regs[int(f[1])].add(int(f[2]))))
    elif op == "upd":
        out.append(str(regs[int(f[1])].update([int(x) for x in f[2:]])))
    elif op == "disc":
        regs[int(f[1])].discard(int(f[2]))
        out.append(repr(regs[int(f[1])]))
    elif op == "pop":
        out.append(str(regs[int(f[1])].pop()))
    elif op == "idx":
        out.append(str(regs[int(f[1])].index(int(f[2]))))
    elif op == "has":
        out.append("yes" if int(f[2]) in regs[int(f[1])] else "no")
    elif op == "len":
        out.append(str(len(regs[int(f[1])])))
    elif op == "repr":
        out.append(repr(regs[int(f[1])]))
    elif op == "list":
        out.append(fmt_list(list(regs[int(f[1])])))
    elif op == "rev":
        out.append(fmt_list(list(reversed(regs[int(f[1])]))))
    elif op == "sub":
        out.append("yes" if regs[int(f[1])].issubset(regs[int(f[2])]) else "no")
    elif op == "super":
        out.append("yes" if regs[int(f[1])].issuperset(regs[int(f[2])]) else "no")
    elif op == "eq":
        out.append("yes" if regs[int(f[1])] == regs[int(f[2])] else "no")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
