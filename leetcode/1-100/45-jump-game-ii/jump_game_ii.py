"""LeetCode #45: Jump Game II — known-correct reference oracle.

From index 0, ``nums[i]`` is the maximum forward jump length from ``i``; return the MINIMUM
number of jumps to reach the last index (the input is guaranteed reachable).

Three styles, all returning the IDENTICAL answer for every case (cross-checked below), each
mirroring one Kāra pedagogical file:

  - Style 1 (greedy range expansion, one pass, O(1) space, ★) — jump_game_ii.kara
  - Style 2 (explicit BFS layers via a sliding window, O(1) space) — jump_game_ii_bfs.kara
  - Style 3 (bottom-up DP over the min-jumps recurrence, O(n) space) — jump_game_ii_dp.kara

Output is the bare integer per case, line-for-line diffable against each Kāra mirror's stdout
under both ``karac run`` and ``karac build``.
"""

from __future__ import annotations


# --- Style 1: greedy range expansion (mirrors jump_game_ii.kara, ★) ------------------------
#
# Walk one cursor; `farthest` is the running max of `i + nums[i]`, `current_end` is the current
# BFS-layer boundary. Reaching the boundary spends one jump and extends it to `farthest`.

def jump_greedy(nums: list[int]) -> int:
    n = len(nums)
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(n - 1):
        if i + nums[i] > farthest:
            farthest = i + nums[i]
        if i == current_end:
            jumps += 1
            current_end = farthest
    return jumps


# --- Style 2: explicit BFS layers via a sliding window (mirrors jump_game_ii_bfs.kara) ------
#
# The current layer is an index window [lo, hi]; sweep it for the farthest reach to get the
# next window [hi+1, next_hi]. One jump per layer; each index is swept by exactly one window.

def jump_bfs(nums: list[int]) -> int:
    n = len(nums)
    jumps = 0
    lo = 0
    hi = 0
    while hi < n - 1:
        next_hi = hi
        for i in range(lo, hi + 1):
            if i + nums[i] > next_hi:
                next_hi = i + nums[i]
        lo = hi + 1
        hi = next_hi
        jumps += 1
    return jumps


# --- Style 3: bottom-up DP over the min-jumps recurrence (mirrors jump_game_ii_dp.kara) -----
#
# dp[j] = min jumps to reach j. Relax forward from each reached i over (i, i+nums[i]]. The
# first sweep finalizes each cell because the graph only points forward. O(n^2) time, O(n) space.

def jump_dp(nums: list[int]) -> int:
    n = len(nums)
    inf = n + 1
    dp = [inf] * n
    dp[0] = 0
    for i in range(n):
        reach = i + nums[i]
        j = i + 1
        while j <= reach and j < n:
            if dp[i] + 1 < dp[j]:
                dp[j] = dp[i] + 1
            j += 1
    return dp[n - 1]


def report(nums: list[int]) -> None:
    a = jump_greedy(nums)
    b = jump_bfs(nums)
    c = jump_dp(nums)
    assert a == b == c, (nums, a, b, c)
    print(a)


def main() -> None:
    report([2, 3, 1, 1, 4])
    report([2, 3, 0, 1, 4])
    report([0])
    report([1, 2])
    report([2, 1])
    report([1, 1, 1, 1])
    report([5, 1, 1, 1, 1])
    report([4, 1, 1, 1, 1])
    report([1, 2, 3])
    report([2, 1, 1, 1, 1])


if __name__ == "__main__":
    main()
