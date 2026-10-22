#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pathvalidate: op \t filename, one per line.

op is validate or sanitize; the target platform is Windows throughout. Inputs
cover reserved names, every invalid-character class (control / \ : * ? " < > |),
trailing/leading space and period, absolute paths, length, the "."/".." exempt
cases, and the null/empty path. A \x01 shows control-character handling.
"""
import os

JOBS = [
    ("validate", "report.txt"),
    ("validate", "CON"),
    ("validate", "con.txt"),
    ("validate", "COM1"),
    ("validate", "LPT9.log"),
    ("validate", "a<b>c"),
    ("validate", "a/b"),
    ("validate", "a\\b"),
    ("validate", "a\x01b"),
    ("validate", "name "),
    ("validate", "name."),
    ("validate", " name"),
    ("validate", "C:\\Windows"),
    ("validate", "/etc/passwd"),
    ("validate", ""),
    ("validate", "   "),
    ("validate", "x" * 300),
    ("validate", "."),
    ("validate", ".."),
    ("validate", "ok_file-1.2.3"),
    ("sanitize", "a<b>c:d"),
    ("sanitize", "CON"),
    ("sanitize", "con.txt"),
    ("sanitize", "name "),
    ("sanitize", "name."),
    ("sanitize", "  spaced  "),
    ("sanitize", "a/b\\c"),
    ("sanitize", "a\x01b"),
    ("sanitize", ""),
    ("sanitize", "???"),
    ("sanitize", "report.final.txt"),
    ("sanitize", ".."),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op, arg in JOBS:
        fh.write("%s\t%s\n" % (op, arg))
