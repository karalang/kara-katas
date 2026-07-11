"""Benchmark workload — Combinations (LeetCode #77).

Python mirror of bench/combinations.kara. Start-indexed pruned backtracking that
ENUMERATES all C(16,8)=12870 combinations and folds each leaf into a threaded
accumulator (no storage). Runs K=150 iterations — 1/10 of the compiled mirrors'
K=1500 — because the pure-Python recursion is slow; timed separately, sink NOT
cross-checked (different K). The kata's correctness is verified by the top-level
combinations.py oracle instead.
"""

from __future__ import annotations


def enumerate_combos(n: int, k: int, start: int, path: list[int], acc: int) -> int:
    if len(path) == k:
        a = acc
        for x in path:
            a = (a * 131 + x) % 1000000007
        return a
    need = k - len(path)
    limit = n - need + 1
    a = acc
    for i in range(start, limit + 1):
        path.append(i)
        a = enumerate_combos(n, k, i + 1, path, a)
        path.pop()
    return a


def main() -> None:
    n, k, total, modulus = 16, 8, 150, 1_000_000_007
    path: list[int] = []
    total_sum = 0
    for it in range(total):
        r = enumerate_combos(n, k, 1, path, it)
        total_sum = (total_sum + r) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
