#!/usr/bin/env python3
"""Ground-truth cross-check for #115.

The 2-D DP (num_distinct.py) must equal two independent references on a battery and 20,000
randomised (s, t) pairs, zero disagreements:

  1. The rolling 1-D DP (the second Kāra solver's mechanism).
  2. A brute-force recursive count of subsequences (the literal definition), memoised so the
     fuzz strings stay tractable.
"""

import random
import sys
from functools import lru_cache

from num_distinct import num_distinct


def rolling(s, t):
    """Rolling 1-D DP (mirrors num_distinct_rolling.kara)."""
    n = len(t)
    dp = [1] + [0] * n
    for ch in s:
        for c in range(n, 0, -1):
            if ch == t[c - 1]:
                dp[c] += dp[c - 1]
    return dp[n]


def brute(s, t):
    @lru_cache(maxsize=None)
    def rec(i, j):
        if j == len(t):
            return 1
        if i == len(s):
            return 0
        cnt = rec(i + 1, j)  # skip s[i]
        if s[i] == t[j]:
            cnt += rec(i + 1, j + 1)  # use s[i]
        return cnt

    r = rec(0, 0)
    rec.cache_clear()
    return r


def check(s, t):
    a = num_distinct(s, t)
    return a == rolling(s, t) and a == brute(s, t)


def main():
    rng = random.Random(20260716)
    checked = 0

    # Battery: classics + edge cases (empty t, empty s, t longer than s, all-equal).
    battery = [
        ("rabbbit", "rabbit"), ("babgbag", "bag"), ("aaaaaa", "aaa"),
        ("", ""), ("abc", ""), ("", "abc"), ("a", "ab"), ("abc", "abcd"),
        ("aaaaaaaaaa", "aaaaa"), ("xyz", "xyz"), ("xyz", "zyx"),
    ]
    for s, t in battery:
        assert check(s, t), f"battery mismatch s={s!r} t={t!r}"
        checked += 1

    FUZZ = 20000
    alpha = "abc"  # small alphabet -> frequent matches, non-trivial counts
    for _ in range(FUZZ):
        s = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 12)))
        # t is often a subsequence-ish of s (bias toward non-zero counts), sometimes random.
        if s and rng.random() < 0.6:
            k = rng.randint(0, len(s))
            idxs = sorted(rng.sample(range(len(s)), k)) if k <= len(s) else []
            t = "".join(s[i] for i in idxs)
        else:
            t = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 6)))
        assert check(s, t), f"fuzz mismatch s={s!r} t={t!r}"
        checked += 1

    print(
        f"ground truth OK: 2-D DP == rolling 1-D == brute-force recursion on {checked} "
        f"(s,t) pairs (battery + {FUZZ} fuzz)"
    )


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
