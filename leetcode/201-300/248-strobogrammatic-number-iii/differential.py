#!/usr/bin/env python3
"""Randomized differential for LeetCode 248.

Two independent answers per case, compared directly:

  A. The kata algorithm — generate every strobogrammatic number of each
     length in [len(low), len(high)] and keep those inside the range.
  B. Brute force — walk every integer in [low, high] and test the property
     with the #246 two-pointer predicate.

They share no code path: A never parses a number and B never generates one.
Ranges are kept narrow (width <= 500) so B stays cheap while A still has to
reason about lengths, boundaries, and the leading-zero rule.

Prints a rolling hash of all counts. The Kara mirror must print the same line.
"""
PAIRS = [("0", "0"), ("1", "1"), ("6", "9"), ("8", "8"), ("9", "6")]
ROT = {"0": "0", "1": "1", "6": "9", "8": "8", "9": "6"}


def lcg(state):
    return (state * 1103515245 + 12345) & 2147483647


def build(k, n):
    if k == 0:
        return [""]
    if k == 1:
        return ["0", "1", "8"]
    out = []
    for inner in build(k - 2, n):
        for a, b in PAIRS:
            if a == "0" and k == n:
                continue
            out.append(a + inner + b)
    return out


def count_gen(low, high):
    lo_len, hi_len = len(low), len(high)
    if lo_len > hi_len or (lo_len == hi_len and low > high):
        return 0
    total = 0
    for length in range(lo_len, hi_len + 1):
        for s in build(length, length):
            if length == lo_len and s < low:
                continue
            if length == hi_len and s > high:
                continue
            total += 1
    return total


def is_strobo(s):
    lo, hi = 0, len(s) - 1
    while lo <= hi:
        if s[lo] not in ROT or ROT[s[lo]] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def count_brute(low, high):
    return sum(1 for v in range(int(low), int(high) + 1) if is_strobo(str(v)))


def main():
    state = 1
    acc = 0
    cases = 0
    mismatch = 0
    for _ in range(3000):
        state = lcg(state)
        lo_hi = state // 65536
        state = lcg(state)
        lo_v = (lo_hi * 32768 + state // 65536) % 100000
        state = lcg(state)
        width = (state // 65536) % 501
        hi_v = lo_v + width
        low, high = str(lo_v), str(hi_v)
        g, b = count_gen(low, high), count_brute(low, high)
        if g != b:
            if mismatch < 5:
                print(f"MISMATCH low={low} high={high} gen={g} brute={b}")
            mismatch += 1
        acc = (acc * 131 + g) % 1000000007
        cases += 1
    print(f"cases={cases} mismatch={mismatch} hash={acc}")


main()
