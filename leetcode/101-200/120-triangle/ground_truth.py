#!/usr/bin/env python3
"""Ground-truth check for LeetCode #120 — the minimum path sum, verified three ways that must agree.

  1. Bottom-up rolling row — seed dp with the base, collapse `dp[k] = tri[i][k] + min(dp[k], dp[k+1])`
     up to the apex (`triangle.kara`, the ★).
  2. Top-down rolling — the mirror recurrence from the apex down, adding each cell to the min of its
     two parents (an independent DP direction).
  3. Brute force — the exact minimum over ALL top-to-bottom paths (only feasible for small heights,
     the definitional oracle).

Checked on many random triangles per height for heights 1..12 (brute force caps the height), plus
the bottom-up == top-down agreement on taller triangles. Zero disagreements is the pass."""

import random


def bottom_up(tri):
    n = len(tri)
    if n == 0:
        return 0
    dp = list(tri[-1])
    for i in range(n - 2, -1, -1):
        for k in range(i + 1):
            dp[k] = tri[i][k] + min(dp[k], dp[k + 1])
    return dp[0]


def top_down(tri):
    n = len(tri)
    if n == 0:
        return 0
    dp = list(tri[0])  # length 1
    for i in range(1, n):
        nxt = [0] * (i + 1)
        for k in range(i + 1):
            if k == 0:
                best = dp[0]
            elif k == i:
                best = dp[i - 1]
            else:
                best = min(dp[k - 1], dp[k])
            nxt[k] = tri[i][k] + best
        dp = nxt
    return min(dp)


def brute(tri):
    n = len(tri)
    if n == 0:
        return 0
    best = [None]

    def go(i, j, total):
        total += tri[i][j]
        if i == n - 1:
            if best[0] is None or total < best[0]:
                best[0] = total
            return
        go(i + 1, j, total)
        go(i + 1, j + 1, total)

    go(0, 0, 0)
    return best[0]


def rand_triangle(h, lo, hi):
    return [[random.randint(lo, hi) for _ in range(i + 1)] for i in range(h)]


def main():
    random.seed(120)
    fails = 0
    # Brute-forceable heights: bottom-up == top-down == brute.
    for h in range(1, 13):
        for _ in range(60):
            tri = rand_triangle(h, -20, 20)
            a, b, c = bottom_up(tri), top_down(tri), brute(tri)
            if not (a == b == c):
                fails += 1
                if fails <= 5:
                    print(f"FAIL h={h}: bottom_up={a} top_down={b} brute={c}")
    # Taller triangles: bottom-up == top-down (brute infeasible).
    for h in [30, 60, 120, 200]:
        for _ in range(20):
            tri = rand_triangle(h, 0, 100)
            a, b = bottom_up(tri), top_down(tri)
            if a != b:
                fails += 1
                if fails <= 5:
                    print(f"FAIL h={h}: bottom_up={a} top_down={b}")
    if fails == 0:
        print("ground truth OK: bottom-up == top-down == brute force (0 disagreements)")
    else:
        print(f"GROUND TRUTH FAILED: {fails} disagreements")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
