#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_ordered_set: a register machine over
OrderedSets. Creating ops append a new register (printing `reg k = <repr>`, k in
creation order); mutating ops change a register in place; query ops print a
result. One op per line (tab-separated):

    new  <v...>              OrderedSet(v...)                 -> reg k = <repr>
    union  <r> <r2> ...      r.union(r2, ...)   (new set)     -> reg k = <repr>
    inter  <r> [<r2> ...]    r.intersection(...) (new set)    -> reg k = <repr>
    diff   <r> [<r2> ...]    r.difference(...)   (new set)    -> reg k = <repr>
    symdiff <r> <r2>         r.symmetric_difference(r2)       -> reg k = <repr>
    add  <r> <v>             r.add(v)   (in place)            -> returned index
    upd  <r> <v...>          r.update(v...) (in place)        -> last index
    disc <r> <v>             r.discard(v) (in place)          -> <repr> after
    pop  <r>                 r.pop()  (last, in place)        -> popped value
    idx  <r> <v>             r.index(v)
    has  <r> <v>             v in r                           -> yes | no
    len  <r>                 len(r)
    repr <r>                 repr(r)
    list <r>                 list(r)                          -> [..]
    rev  <r>                 list(reversed(r))                -> [..]
    sub  <r> <r2>            r.issubset(r2)                   -> yes | no
    super <r> <r2>           r.issuperset(r2)                 -> yes | no
    eq   <r> <r2>            r == r2  (order-sensitive)       -> yes | no

`oracle.py` replays the sequence against the vendored ordered_set. The point of
the suite is order: `add` keeps first-appearance order and returns the existing
index for a duplicate; `discard` reindexes; union/intersection/difference each
have their own ordering rule (union by first appearance across all sets,
intersection and difference by the first set's order), and `symmetric_difference`
puts self's uniques before other's.
"""
import os

ops = []
k = 0


def emit(*p):
    ops.append(tuple(str(x) for x in p))


def create(*p):
    global k
    emit(*p)
    r = k
    k += 1
    return r


a = create("new", 3, 1, 4, 1, 5, 9, 2, 6)
b = create("new", 1, 3, 5, 7, 9)
c = create("new", 2, 4, 6, 8)

emit("add", a, 7)
emit("add", a, 3)         # duplicate -> existing index
emit("upd", a, 10, 1, 11)
emit("repr", a)
emit("idx", a, 4)
emit("has", a, 9)
emit("has", a, 99)
emit("disc", a, 4)        # reindexes
emit("idx", a, 5)
emit("disc", a, 999)      # absent -> no change
emit("pop", a)            # pop last
emit("repr", a)
emit("len", a)
emit("list", a)
emit("rev", a)

u = create("union", b, c)
lit = create("new", 0, 1, 100)
u3 = create("union", b, c, lit)
inter = create("inter", b, c)
inter0 = create("inter", b)        # no other sets -> copy
d = create("diff", b, c)
d0 = create("diff", b)             # no other sets -> copy

s1 = create("new", 1, 4, 3, 5, 7)
s2 = create("new", 9, 7, 1, 3, 2)
sd = create("symdiff", s1, s2)

p = create("new", 1, 2)
q = create("new", 1, 2, 3)
emit("sub", p, q)
emit("sub", q, p)
emit("super", q, p)
emit("super", p, q)

e1 = create("new", 1, 3, 2)
e2 = create("new", 1, 3, 2)
e3 = create("new", 1, 2, 3)
emit("eq", e1, e2)
emit("eq", e1, e3)

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op in ops:
        fh.write("\t".join(op) + "\n")
