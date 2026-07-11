"""Benchmark workload — Minimum Window Substring (LeetCode #76).

Python mirror of bench/minimum_window_substring.kara. Same sliding-window need/have
algorithm over a fixed n=50000 sequence (alphabet {0,1,2,3}). Runs K=500 iterations
— 1/10 of the compiled mirrors' K=5000 — because a pure-Python O(n) scan at full
scale is slow; this row is timed separately and its sink is NOT cross-checked
against the compiled sink (different K). The kata's correctness is verified by the
top-level minimum_window_substring.py oracle instead.
"""

from __future__ import annotations

N = 50000


def min_window(s: list[int], t: list[int]) -> tuple[int, int]:
    n, m = len(s), len(t)
    if m > n:
        return (-1, 0)
    need = [0, 0, 0, 0]
    required = 0
    for c in t:
        if need[c] == 0:
            required += 1
        need[c] += 1
    have = [0, 0, 0, 0]
    formed = 0
    l = 0
    best_start, best_len = -1, 0
    for r in range(n):
        cr = s[r]
        have[cr] += 1
        if have[cr] == need[cr]:
            formed += 1
        while formed == required:
            win = r - l + 1
            if best_start == -1 or win < best_len:
                best_start, best_len = l, win
            cl = s[l]
            have[cl] -= 1
            if have[cl] < need[cl]:
                formed -= 1
            l += 1
    return (best_start, best_len)


def main() -> None:
    total = 500  # 1/10 of the compiled mirrors' K; timed-only, not cross-checked
    modulus = 1_000_000_007
    s = [(i * 7) % 4 for i in range(N)]
    targets = [[0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1], [0, 2, 3], [1, 3, 0]]
    acc = 0
    for k in range(total):
        start, length = min_window(s, targets[k % 6])
        acc = (acc * 131 + (start + 1)) % modulus
        acc = (acc * 131 + length) % modulus
    print(acc)


if __name__ == "__main__":
    main()
