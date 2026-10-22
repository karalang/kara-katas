#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_toposort (tab-separated ops):
  l <graphspec>   toposort into levels: each level's items sorted and joined by
                  ",", levels joined by " | "; or ERR on a circular dependency
  f <graphspec>   toposort_flatten(sort=True): the flat sorted order, space-joined;
                  or ERR on a circular dependency
A <graphspec> is ";"-separated entries "key:dep1,dep2" (deps may be empty), e.g.
"a:b,c;b:d;c:d;d:". mk.py writes only literal inputs (no library import);
oracle.py replays every job against the vendored toposort library. Items are
ASCII tokens containing no tab, newline, ';', ':' or ','. See README.md."""
import os
os.makedirs("data", exist_ok=True)

specs = [
    "",
    "a:",
    "a:b;b:",
    "a:b,c;b:d;c:d;d:",
    "2:11,10;9:11,8;10:11,3;11:7,5;8:7,3;7:;5:;3:",
    "x:y;y:z;z:",
    "build:compile;compile:parse;parse:lex;lex:",
    "a:b;b:c;c:a",
    "a:a",
    "a:b;b:a",
    "web:db,cache;api:db;db:;cache:",
    "root:;c1:root;c2:root;leaf:c1,c2",
    "d:a,b,c;a:;b:a;c:b",
    "only:",
    "p:q,r;q:;r:q",
    "m:n;n:o;o:p;p:",
    "1:2;2:3;3:4;4:5;5:",
    "a:b,c,d;b:c;c:d;d:;e:a",
    "s:",
    "cycle3:x;x:y;y:cycle3",
]

lines = []
for s in specs:
    lines.append("l\t%s" % s)
for s in specs:
    lines.append("f\t%s" % s)

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
