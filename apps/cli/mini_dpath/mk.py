#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_dpath: one query job per line.

    <op> \t <glob> \t <json-document>

dpath addresses nested dict/list data with filesystem-like glob paths. `op`
is one of:

  search  → every (path, value) pair whose path matches the glob, in dpath's
            walk order (all of a node's direct children first, then each
            child's subtree), joined with ` | ` (or `(none)`);
  values  → just the matching values, in the same order;
  get     → the single value the glob addresses, or `KeyError` (no match) /
            `ValueError` (more than one match).

A glob segment is an exact key, `*` (any one segment), or `**` (any run of
segments); a numeric segment matches a list index. Paths are rendered with
list indices as their decimal string, joined by `/`.
"""
import os

D1 = '{"a": {"b": 1, "c": 2}, "d": [10, 20, 30], "e": {"b": 9}}'
D2 = '{"users": [{"name": "x", "age": 1}, {"name": "y", "age": 2}], "meta": {"count": 2}}'

JOBS = [
    ("search", "a/*", D1),
    ("search", "*/b", D1),
    ("search", "**/b", D1),
    ("search", "d/*", D1),
    ("search", "a/b", D1),
    ("search", "**", D1),
    ("values", "d/*", D1),
    ("values", "*/b", D1),
    ("get", "a/b", D1),
    ("get", "d/1", D1),
    ("get", "*/b", D1),
    ("get", "x/y", D1),
    ("search", "users/*/name", D2),
    ("search", "users/**/age", D2),
    ("search", "users/*/*", D2),
    ("values", "users/*/name", D2),
    ("values", "meta/*", D2),
    ("get", "meta/count", D2),
    ("get", "users/0/name", D2),
    ("get", "users/5/name", D2),
    ("search", "**", D2),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op, glob, doc in JOBS:
        fh.write(op + "\t" + glob + "\t" + doc + "\n")
