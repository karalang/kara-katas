"""Benchmark workload — hash-map O(n) Two Sum.

Same N / K / target as bench/brute_force.py. The single-pass dict
implementation walks the array once per call (O(n) work) — at
N=5000, K=10 that is ~50,000 ops per process. See ../README.md
§ Benchmarks for what the numbers mean.
"""

from __future__ import annotations


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return seen[complement], i
        seen[num] = i
    return None


def main() -> None:
    N = 5000
    data = [(i * 7) % 1000 for i in range(N)]
    target = -1

    sum_result = 0
    for _ in range(10):
        r = two_sum(data, target)
        if r is None:
            sum_result += -1 + -1
        else:
            sum_result += r[0] + r[1]
    print(sum_result)


if __name__ == "__main__":
    main()
