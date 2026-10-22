#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_iterutils: a register machine over the
sequence toolkit of boltons.iterutils, on Vec[i64]. `new` ops append a register
(printing `reg k = [..]`, k in creation order); every other op reads a register
(or bare integers, for `cranges`) and prints a result. One op per line
(tab-separated):

    new   <v...>                   a sequence                 -> reg k = [..]
    split <r> <sep>                split on a value           -> [[..], ..]
    lstrip <r> <v>                 strip leading <v>          -> [..]
    rstrip <r> <v>                 strip trailing <v>         -> [..]
    strip <r> <v>                  strip both ends            -> [..]
    chunked <r> <size>             fixed-size chunks          -> [[..], ..]
    chunkfill <r> <size> <fill>    chunks padded with <fill>  -> [[..], ..]
    cranges <isz> <csz> <off> <ovl> <align>   chunk_ranges    -> [(s, e), ..]
    pairwise <r>                   adjacent pairs             -> [(a, b), ..]
    pairend <r> <end>              pairs, last paired w/ end  -> [(a, b), ..]
    windowed <r> <size>            sliding windows            -> [(..), ..]
    winfill <r> <size> <fill>      windows padded to the end  -> [(..), ..]
    bucket <r> mod3|even           bucketize by key           -> {k: [..], ..}
    part1 <r> even|truthy          partition on one predicate -> ([..], [..])
    part2 <r>                      partition on >0 then <0    -> ([..], [..], [..])
    unique <r>                     first-seen uniques         -> [..]
    redund <r>                     first redundant of each    -> [..]
    redundg <r>                    groups of redundants       -> [[..], ..]
    one <r> truthy|gt40|even       the sole match, else None  -> v | None
    first <r> truthy|gt40|even     first match, else None     -> v | None
    same <r>                       all equal?                 -> yes | no
    sameref <r> <ref>              all equal to <ref>?        -> yes | no

`oracle.py` replays the sequence against the vendored boltons.iterutils, calling
the real functions with the key/predicate the mode names. The ported subset is
the flat-sequence toolkit; remap/get_path/research over nested structures, and
the float ranges (frange/backoff), are out of scope (documented in README).
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


a = create("new", 1, 2, 0, 0, 3, 0, 4, 5)       # has a split value (0)
b = create("new", 7, 7, 1, 2, 3, 7, 7)           # for strip
c = create("new", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)  # range-like
d = create("new", 1, 2, 3, 2, 3, 3, 4)           # redundancies
e = create("new", -3, -1, 0, 2, 4, 5)            # signs
f = create("new", 5, 5, 5, 5)                    # all-same
g = create("new", 10, 20, 30, 42)                # for gt40

# split / strip
emit("split", a, 0)
emit("lstrip", b, 7)
emit("rstrip", b, 7)
emit("strip", b, 7)

# chunking
emit("chunked", c, 3)
emit("chunkfill", c, 3, 0)
emit("chunked", c, 5)
emit("cranges", 10, 5, 10, 0, 0)
emit("cranges", 10, 5, 10, 1, 0)
emit("cranges", 15, 5, 4, 0, 1)
emit("cranges", 15, 5, 2, 1, 1)

# windows
emit("pairwise", c)
emit("pairend", c, -1)
emit("windowed", c, 3)
emit("windowed", a, 9)            # too short, no fill -> []
emit("winfill", a, 3, 0)

# grouping
emit("bucket", c, "mod3")
emit("bucket", c, "even")
emit("part1", c, "even")
emit("part1", a, "truthy")
emit("part2", e)

# de-dup
emit("unique", d)
emit("redund", d)
emit("redundg", d)

# selection
emit("one", f, "truthy")          # many matches -> None
emit("one", e, "gt40")            # none -> None
emit("one", g, "gt40")            # exactly one (42)
emit("first", a, "truthy")        # first nonzero -> 1
emit("first", c, "even")          # first even (0 is even) -> 0
emit("first", e, "gt40")          # none -> None

# equality
emit("same", f)
emit("same", c)
emit("sameref", f, 5)
emit("sameref", f, 9)

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op in ops:
        fh.write("\t".join(op) + "\n")
