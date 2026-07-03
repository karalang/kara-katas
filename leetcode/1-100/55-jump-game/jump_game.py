"""LeetCode #55: Jump Game — known-correct reference oracle.

From index 0, ``nums[i]`` is the maximum forward jump length from ``i``; return WHETHER the last
index is reachable (yes/no). This is the decision sibling of #45, which counts the fewest hops.

Three styles, all returning the IDENTICAL answer for every case (cross-checked below), each
mirroring one Kāra pedagogical file:

  - Style 1 (greedy forward max-reach, one pass, O(1) space, ★) — jump_game.kara
  - Style 2 (backward "last good index" scan, O(1) space)       — jump_game_backward.kara
  - Style 3 (bottom-up reachability DP, O(n) space)             — jump_game_dp.kara

Output is the bare lowercase boolean per case (``true`` / ``false``), line-for-line diffable
against each Kāra mirror's stdout under both ``karac run`` and ``karac build``.
"""

from __future__ import annotations


# --- Style 1: greedy forward max-reach (mirrors jump_game.kara, ★) --------------------------
#
# Sweep left to right carrying `farthest` = rightmost reachable index. If `i` is past `farthest`
# no chain of jumps lands on it, so bail; else extend the horizon by `i + nums[i]`.

def can_jump_greedy(nums: list[int]) -> bool:
    n = len(nums)
    farthest = 0
    for i in range(n):
        if i > farthest:
            return False
        if i + nums[i] > farthest:
            farthest = i + nums[i]
        if farthest >= n - 1:
            return True
    return True


# --- Style 2: backward "last good index" scan (mirrors jump_game_backward.kara) -------------
#
# `good` = leftmost index known to reach the end, seeded at n-1. Scanning right-to-left, an
# index that can hop onto the current `good` becomes the new `good`. Reachable iff good == 0.

def can_jump_backward(nums: list[int]) -> bool:
    n = len(nums)
    good = n - 1
    for i in range(n - 2, -1, -1):
        if i + nums[i] >= good:
            good = i
    return good == 0


# --- Style 3: bottom-up reachability DP (mirrors jump_game_dp.kara) -------------------------
#
# reach[j] = can index j be stood on? reach[0] = True; from each reachable i mark (i, i+nums[i]].
# One forward pass finalizes each cell because the graph only points forward. O(n^2) time.

def can_jump_dp(nums: list[int]) -> bool:
    n = len(nums)
    reach = [False] * n
    reach[0] = True
    for i in range(n):
        if reach[i]:
            bound = i + nums[i]
            j = i + 1
            while j <= bound and j < n:
                reach[j] = True
                j += 1
    return reach[n - 1]


def report(nums: list[int]) -> None:
    a = can_jump_greedy(nums)
    b = can_jump_backward(nums)
    c = can_jump_dp(nums)
    assert a == b == c, (nums, a, b, c)
    print("true" if a else "false")


def main() -> None:
    report([2, 3, 1, 1, 4])
    report([3, 2, 1, 0, 4])
    report([0])
    report([0, 1])
    report([1, 0])
    report([2, 0, 0])
    report([1, 1, 1, 1])
    report([1, 0, 1, 0])
    report([5, 0, 0, 0, 0])
    report([2, 5, 0, 0])
    report([1, 2, 3])
    report([1, 1, 0, 1])


if __name__ == "__main__":
    main()
