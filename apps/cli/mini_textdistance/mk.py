#!/usr/bin/env python3
"""Writes data/jobs.tsv: one string pair per line (op=pair), tab-separated.

The argument is two ASCII strings separated by `|`. The oracle reports five
integer metrics for the pair: Hamming distance, Levenshtein distance, the
restricted (optimal string alignment) Damerau-Levenshtein distance, the
longest-common-subsequence length and the longest-common-substring length.
"""
import os

PAIRS = [
    ("kitten", "sitting"),          # classic Levenshtein 3
    ("Saturday", "Sunday"),         # classic Levenshtein 3
    ("flaw", "lawn"),
    ("abc", "abc"),                 # identical
    ("", "abc"),                    # one empty
    ("abc", ""),
    ("", ""),                       # both empty
    ("ba", "ab"),                   # transposition: lev 2, damerau 1
    ("ca", "abc"),                  # unequal-length transposition case
    ("CA", "ABC"),
    ("karolin", "kathrin"),         # equal length, Hamming 3
    ("1011101", "1001001"),         # equal length, Hamming 2
    ("hello", "world"),
    ("abcdef", "zabcf"),            # substring / subsequence
    ("AGCAT", "GAC"),               # classic LCS subsequence
    ("ABCDEF", "ABDDEF"),           # single substitution
    ("a quick fox", "a quik fox"),  # spaces kept as chars
    ("abcdxyz", "xyzabcd"),         # long common substrings, rotated
    ("GeeksforGeeks", "GeeksQuiz"),
    ("12345", "135"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for a, b in PAIRS:
        fh.write("pair\t" + a + "|" + b + "\n")
