#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_mmh3: one hash job per line.

    <op> \t <seed> \t <text>

`op` is `h32` (MurmurHash3 x86_32, the 32-bit hash) or `h128` (MurmurHash3
x86 128-bit). `seed` is a decimal unsigned 32-bit seed. The inputs are short
ASCII strings whose lengths walk every tail size the two algorithms branch on
(lengths 0..17, 31..33: for h32 the length mod 4, for h128 the length mod 16),
across a few seeds. oracle.py hashes them through the vendored pymmh3;
mini_mmh3.kara reproduces expected.out byte-for-byte.
"""
import os

TEXTS = [
    "",
    "a",
    "ab",
    "abc",
    "abcd",
    "abcde",
    "abcdef",
    "abcdefg",
    "abcdefgh",
    "hello",
    "hello, world",
    "The quick brown fox",
    "0123456789abcdef",
    "0123456789abcdefg",
    "murmur3 x86 128",
    "xxxxxxxxxxxxxxxxx",
    "The quick brown fox jumps over",
    "a-really-long-partition-key-value-0001",
]
SEEDS = [0, 42, 2504183948]  # 0x9747b28c, a seed common in Murmur test vectors

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for seed in SEEDS:
        for t in TEXTS:
            fh.write("h32\t%d\t%s\n" % (seed, t))
    for seed in SEEDS:
        for t in TEXTS:
            fh.write("h128\t%d\t%s\n" % (seed, t))
