#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pyrsistent: a register machine over PVectors.

Every creating op appends one new vector to a register file and prints
`reg <k> len <n>` (k is its index, in creation order); query ops print a
result. One op per line (tab-separated):

    iota <n>              pvector(range(n))                 -> reg k len n
    new <v...>            pvector([v...])                   -> reg k len n
    app  <r> <val>        regs[r].append(val)               -> reg k len n
    set  <r> <i> <val>    regs[r].set(i, val)               -> reg k len n
    ext  <r> <v...>       regs[r].extend([v...])            -> reg k len n
    extr <r> <r2>         regs[r].extend(regs[r2])          -> reg k len n
    mset <r> i v i v ...  regs[r].mset(i, v, ...)           -> reg k len n
    del  <r> <i>          regs[r].delete(i)                 -> reg k len n
    dels <r> <i> <j>      regs[r].delete(i, j)  (slice)     -> reg k len n
    mul  <r> <t>          regs[r] * t                       -> reg k len n
    get  <r> <i>          regs[r][i]   (negative allowed)   -> <value>
    len  <r>              len(regs[r])                      -> <n>
    idx  <r> <val>        regs[r].index(val)                -> <i> | miss
    cnt  <r> <val>        regs[r].count(val)                -> <n>
    eq   <r> <r2>         regs[r] == regs[r2]               -> yes | no
    lt   <r> <r2>         regs[r] <  regs[r2]               -> yes | no
    rng  <r> <a> <b>      list(regs[r])[a:b]                -> [..]   (a window)
    list <r>              list(regs[r])                     -> [..]
    repr <r>              repr(regs[r])                     -> pvector([..])

The `iota 1100` vector overflows the 32-wide tail into a tree and, past 1024
elements, grows the trie a level, so the boundary gets/sets/windows prove the
`_node_for` / `_push_tail` / `_create_new_root` / `_new_path` math. Small
vectors carry the full-list / repr / compare / index checks.
"""
import os

ops = []
k = 0            # next register index


def emit(*parts):
    ops.append(tuple(str(p) for p in parts))


def create(*parts):
    global k
    emit(*parts)
    r = k
    k += 1
    return r


# r0: a big vector — tail overflow (32) and one trie-level growth (1024)
big = create("iota", 1100)
for i in [0, 1, 31, 32, 33, 1023, 1024, 1025, 1099, -1, -1100]:
    emit("get", big, i)
for a, b in [(30, 35), (1022, 1027), (1095, 1100), (0, 4)]:
    emit("rng", big, a, b)
emit("len", big)

# sets at a tail slot, a first-level leaf, and across the 1024 boundary;
# the original must stay unchanged (structural sharing)
s1 = create("set", big, 1099, -8)      # in the tail
emit("get", s1, 1099)
emit("get", big, 1099)
s2 = create("set", big, 33, -7)        # in a tree leaf
emit("get", s2, 33)
emit("get", big, 33)
s3 = create("set", big, 1024, -9)      # just past the growth boundary
emit("get", s3, 1024)
emit("get", big, 1024)

# append past the end (==len) and plain append
a1 = create("app", big, 7)
emit("len", a1)
emit("get", a1, 1100)

# a medium vector that crosses exactly one tail boundary
med = create("iota", 40)
emit("rng", med, 30, 34)
emit("get", med, -1)
emit("len", med)

# small vectors: full list / repr / extend / index / count
sv = create("new", 10, 20, 30, 40, 50)
emit("list", sv)
emit("repr", sv)
e1 = create("ext", sv, 60, 70)
emit("list", e1)
emit("idx", e1, 40)
emit("idx", e1, 999)
emit("cnt", e1, 30)
e2 = create("extr", sv, med)           # extend one vector by another
emit("len", e2)
emit("rng", e2, 3, 9)

# delete, slice-delete, mset, mul
d1 = create("del", e1, 2)
emit("list", d1)
d2 = create("dels", e1, 1, 4)
emit("list", d2)
m1 = create("mset", e1, 0, 9, 6, 8)
emit("list", m1)
mu = create("mul", sv, 3)
emit("list", mu)
emit("len", mu)
mz = create("mul", sv, 0)
emit("len", mz)

# comparisons (library compares by tolist())
c1 = create("new", 1, 2, 3)
c2 = create("new", 1, 2, 3)
c3 = create("new", 1, 2, 4)
c4 = create("new", 1, 2)
emit("eq", c1, c2)
emit("eq", c1, c3)
emit("lt", c1, c3)
emit("lt", c3, c1)
emit("lt", c4, c1)
emit("lt", c1, c4)

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op in ops:
        fh.write("\t".join(op) + "\n")
