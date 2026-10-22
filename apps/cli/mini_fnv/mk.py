#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one FNV hash job per line, tab-separated as
`variant<TAB>input`. variant is one of fnv0_32, fnv1_32, fnv1a_32; input is the
ASCII text whose UTF-8 bytes are hashed. No fnvhash import here (only literal
inputs); oracle.py replays each line through the vendored library to produce
expected.out (the 32-bit hash as 8 lowercase hex digits)."""

VARIANTS = ["fnv0_32", "fnv1_32", "fnv1a_32"]

# ASCII inputs (no tab/newline). Mix of empty, single chars, words, phrases,
# digits, punctuation and repeats, so each variant is exercised over varied
# lengths and byte patterns.
INPUTS = [
    "",
    "a",
    "b",
    "ab",
    "abc",
    "abcd",
    "hello",
    "Hello",
    "hello world",
    "The quick brown fox jumps over the lazy dog",
    "foobar",
    "chongo was here!",
    "chongo was here!\\n".replace("\\n", ""),  # kept ASCII, no newline
    "1234567890",
    "0",
    "00",
    "000",
    "FNV",
    "fnv",
    "geohash",
    "a quick test of the fnv hash",
    "!@#$%^&*()",
    "aaaaaaaa",
    "zzzzzzzzzzzz",
    "The five boxing wizards jump quickly",
    "xyzzy",
    "line with spaces and  double  spaces",
    "MixedCASE Letters 123",
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for inp in INPUTS:
            for v in VARIANTS:
                fh.write(v + "\t" + inp + "\n")


main()
