#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_glom: one glom job per line.

    <spec-dsl> \t <json-target>

The DSL is documented in oracle.py (P/V/D/I/T/C). The jobs exercise path
access over dicts, nested dicts, and list indices; the three access-error
classes glom surfaces (KeyError on a dict miss, IndexError on a list
out-of-range, AttributeError reaching into a scalar); dict restructuring;
mapping a subpath over a list (`I` and the `T` nav+map idiom); the literal
`Val`; and Coalesce hitting its first, a later, a default, or failing.
"""
import os

D1 = '{"a": {"b": {"c": 10}}, "d": [1, 2, 3], "e": {"name": "x"}}'
D2 = '{"users": [{"name": "x", "age": 1}, {"name": "y", "age": 2}], "meta": {"count": 2}}'
D3 = '[{"v": 1}, {"v": 2}, {"v": 3}]'

JOBS = [
    # path access — success
    ("P a", D1),
    ("P a.b", D1),
    ("P a.b.c", D1),
    ("P d", D1),
    ("P d.0", D1),
    ("P d.2", D1),
    ("P e.name", D1),
    ("P users.0.name", D2),
    ("P users.1.age", D2),
    ("P meta.count", D2),
    # path access — the three error classes
    ("P a.z", D1),          # KeyError on dict
    ("P a.b.z", D1),        # KeyError deeper
    ("P d.5", D1),          # IndexError on list
    ("P a.b.c.x", D1),      # AttributeError reaching into an int
    ("P users.9.name", D2),  # IndexError on list of dicts
    # dict restructure
    ("D first=a.b.c;who=e.name", D1),
    ("D n=meta.count;top=users.0.name", D2),
    ("D miss=a.z", D1),     # a failing field fails the whole glom
    # map a path over a list
    ("I v", D3),
    ("T users | name", D2),
    ("T users | age", D2),
    ("T d | ", D1),         # inner empty path is identity over each element
    # literal
    ("V 42", D1),
    ('V "hello"', D1),
    ("V [1, 2, 3]", D2),
    ('V {"k": true}', D3),
    # Coalesce
    ("C a.b.c || e.name", D1),       # first hits
    ("C x.y || a.b.c", D1),          # first misses, second hits
    ("C x || y => -1", D1),          # all miss, default
    ('C a.z || meta.nope => "fb"', D1),  # default is a string
    ("C x", D1),                     # single miss, no default -> error
    ("C x || y || z", D1),           # three misses -> error
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for dsl, target in JOBS:
        fh.write(dsl + "\t" + target + "\n")
