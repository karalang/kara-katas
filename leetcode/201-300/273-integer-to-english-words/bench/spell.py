#!/usr/bin/env python3
"""Benchmark workload for LeetCode #273 — Integer to English Words.

Algorithm-for-algorithm mirror of spell.kara. Kept as a CORRECTNESS ORACLE, not
a timed lane: Python is excluded from the measured comparison
(KARA_BENCH_INCLUDE_PY defaults to 0 in scripts/bench-lib.sh).
"""

COUNT = 200000
ROUNDS = 5

SMALL = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
         "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
         "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy",
        "Eighty", "Ninety"]
SCALES = ["", "Thousand", "Million", "Billion"]


def group_name(n):
    if n == 0:
        return ""
    if n < 20:
        return SMALL[n]
    if n < 100:
        t = TENS[n // 10]
        r = n % 10
        return t if r == 0 else t + " " + SMALL[r]
    h = SMALL[n // 100] + " " + "Hundred"
    r = group_name(n % 100)
    return h if r == "" else h + " " + r


def number_to_words(n):
    if n == 0:
        return "Zero"
    out = ""
    rem, scale = n, 0
    while rem > 0:
        part = rem % 1000
        if part > 0:
            piece = group_name(part)
            if scale > 0:
                piece = piece + " " + SCALES[scale]
            out = piece if out == "" else piece + " " + out
        rem //= 1000
        scale += 1
    return out


def main():
    nums = []
    lo, hi = 2147483647, 0
    state = 273273
    for _ in range(COUNT):
        state = (state * 1103515245 + 12345) & 2147483647
        lo = min(lo, state)
        hi = max(hi, state)
        nums.append(state)

    sink = 0
    for _ in range(ROUNDS):
        for q in range(COUNT):
            for b in number_to_words(nums[q]).encode():
                sink = (sink * 131 + b) % 1000000007

    print(sink)
    print(f"count {COUNT} range {lo}..{hi}")


main()
