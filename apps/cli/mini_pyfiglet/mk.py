#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pyfiglet: one render job per line.

    render \t <text>

Each job renders <text> as FIGlet art in the standard font. The inputs are
short single-line ASCII strings chosen to exercise the horizontal smushing
rules the standard font turns on (equal-character, underscore, hierarchy and
bracket-pair smushing), plus spaces between words and the first-character edge
case. oracle.py renders them through the vendored pyfiglet; mini_pyfiglet.kara
reproduces expected.out byte-for-byte, trailing spaces and all.
"""
import os

TEXTS = [
    "Hi",
    "Kara",
    "foo bar",
    "AVA",
    "a_b_c",
    "O(1)",
    "x|y",
    "12/34",
    "C++",
    "[a]{b}",
    "Yes!",
    "mix 9",
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for t in TEXTS:
        fh.write("render\t" + t + "\n")
