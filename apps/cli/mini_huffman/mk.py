#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one input string per line. The job builds a Huffman
code from the string's bytes, then prints the encoded bytes (hex) and the code
table. No dahuffman import here (only literal inputs); oracle.py replays each
line through the vendored library to produce expected.out."""

INPUTS = [
    "aaaa",
    "ab",
    "abracadabra",
    "mississippi",
    "hello world",
    "the quick brown fox jumps over the lazy dog",
    "aaaabbbccd",
    "banana",
    "1223334444",
    "to be or not to be",
    "AAAAAAAAB",
    "abcabcabcabc",
    "committee",
    "bookkeeper",
    "0123456789",
    "racecar",
    "tennessee",
    "!!!???...",
    "the rain in spain",
    "compression",
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for s in INPUTS:
            fh.write(s + "\n")


main()
