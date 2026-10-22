#!/usr/bin/env python3
"""Writes data/jobs.tsv: one word_to_num call per line, tab-separated.

op is always `num`; arg is the number sentence. Only the integer feature is
exercised (the `point` / decimal path needs Python float-repr parity and is
out of scope), so no arg contains the word "point".
"""
import os

JOBS = [
    # single words and the under-100 forms
    ("num", "zero"),
    ("num", "one"),
    ("num", "eleven"),
    ("num", "fifty"),
    ("num", "seventy"),
    ("num", "forty-nine"),             # hyphen becomes a space
    # hundreds, with "and" / "&" dropped
    ("num", "one hundred"),
    ("num", "one hundred twenty three"),
    ("num", "two hundred and five"),
    ("num", "nine hundred ninety nine"),
    # thousands
    ("num", "one thousand"),
    ("num", "two thousand nineteen"),
    ("num", "twenty three thousand forty nine"),
    ("num", "one hundred twenty three thousand four hundred fifty six"),
    # millions and billions
    ("num", "one million"),
    ("num", "two million twenty three thousand and forty nine"),
    ("num", "one billion"),
    ("num", "three billion two hundred million"),
    # a bare digit string passes straight through
    ("num", "112"),
    # the error paths
    ("num", "hello world"),            # no valid number words
    ("num", ""),                       # no valid number words
    ("num", "two thousand thousand"),  # redundant thousand
    ("num", "one million million"),    # redundant million
    ("num", "one thousand two million"),  # malformed: thousand before million
    ("num", "five million three billion"),  # malformed: million before billion
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
