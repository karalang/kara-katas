#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_braceexpand: one brace pattern per line.

Patterns exercise integer ranges (with padding, step, direction, negatives),
character ranges (step, mixed-case skip), sequences, nesting, the literal-brace
fallbacks ({} and {a}), escaped braces, and an unbalanced pattern (error path).
"""
import os

PATTERNS = [
    "item{1..3}",
    "{a..c}",
    "index.html{,.backup}",
    "python{2.{5..7},3.{2,3}}",
    "{07..10}",
    "{a..g..2}",
    "{4..1}",
    "{2..-1}",
    r"{1\{2,3}",
    "file{A..E..2}.txt",
    "{x,y,z}",
    "a{b,c}d{e,f}",
    "{}",
    "{a}",
    "host{1..3}.example.com",
    "{Z..a}",
    "img{001..003}.png",
    "{10..4..3}",
    "pre{1..2}mid{A..B}post",
    "{1{2,3}",
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(PATTERNS) + "\n")
