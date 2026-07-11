"""Benchmark workload — Subsets (LeetCode #78).

Python mirror of bench/subsets.kara. Emit-at-every-node backtracking that ENUMERATES
the power set of [1..16] and folds each node's path into a threaded accumulator (no
storage). Runs K=30 iterations — 1/10 of the compiled mirrors' K=300 — because the
pure-Python recursion is slow; timed separately, sink NOT cross-checked (different K).
The kata's correctness is verified by the top-level subsets.py oracle instead.
"""

from __future__ import annotations


def enumerate_subsets(nums: list[int], start: int, path: list[int], acc: int) -> int:
    a = acc
    a = (a * 131 + (len(path) + 1)) % 1000000007
    for x in path:
        a = (a * 131 + x) % 1000000007
    n = len(nums)
    for i in range(start, n):
        path.append(nums[i])
        a = enumerate_subsets(nums, i + 1, path, a)
        path.pop()
    return a


def main() -> None:
    n, total, modulus = 16, 30, 1_000_000_007
    nums = list(range(1, n + 1))
    path: list[int] = []
    total_sum = 0
    for it in range(total):
        r = enumerate_subsets(nums, 0, path, it)
        total_sum = (total_sum + r) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
