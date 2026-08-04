#!/usr/bin/env python3
"""LeetCode 248 - Strobogrammatic Number III. Oracle mirror.

Count strobogrammatic numbers in [low, high] (inclusive), both given as
decimal strings without leading zeros.

Same algorithm as the Kara version: generate every strobogrammatic number of
each length in [len(low), len(high)] by building middle-outward, then keep the
ones inside the range. Because all candidates of a given length have that
length, the range test is a plain lexicographic compare -- no numeric parse,
so it works for lengths beyond machine integers.
"""
import sys

PAIRS = [("0", "0"), ("1", "1"), ("6", "9"), ("8", "8"), ("9", "6")]


def build(k, n):
    """Every strobogrammatic string of length k, as the inside of a length-n
    number. `n` is threaded so only the OUTERMOST layer bars a leading zero."""
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


def strobogrammatic(n):
    return build(n, n)


def count_in_range(low, high):
    lo_len, hi_len = len(low), len(high)
    if lo_len > hi_len or (lo_len == hi_len and low > high):
        return 0
    total = 0
    for length in range(lo_len, hi_len + 1):
        for s in strobogrammatic(length):
            if length == lo_len and s < low:
                continue
            if length == hi_len and s > high:
                continue
            total += 1
    return total


def brute(low, high):
    """Independent check: walk every integer in the range and test the
    property directly with the #246 two-pointer predicate."""
    rot = {"0": "0", "1": "1", "6": "9", "8": "8", "9": "6"}

    def ok(s):
        lo, hi = 0, len(s) - 1
        while lo <= hi:
            if s[lo] not in rot or rot[s[lo]] != s[hi]:
                return False
            lo += 1
            hi -= 1
        return True

    return sum(1 for v in range(int(low), int(high) + 1) if ok(str(v)))


CASES = [
    ("50", "100"), ("0", "0"), ("0", "9"), ("1", "1"), ("8", "8"),
    ("0", "100"), ("10", "1000"), ("1", "10000"), ("100", "999"),
    ("11", "69"), ("69", "69"), ("609", "906"), ("2", "3"),
    ("1000", "99999"), ("6", "9"),
]

if __name__ == "__main__":
    if "--verify" in sys.argv:
        bad = 0
        for lo, hi in CASES:
            g, b = count_in_range(lo, hi), brute(lo, hi)
            if g != b:
                print(f"MISMATCH low={lo} high={hi} gen={g} brute={b}")
                bad += 1
        print("verify: all agree" if not bad else f"verify: {bad} mismatch(es)")
        sys.exit(1 if bad else 0)
    for lo, hi in CASES:
        print(f"low={lo} high={hi} count={count_in_range(lo, hi)}")
