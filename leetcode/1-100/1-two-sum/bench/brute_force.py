"""Benchmark workload — brute-force O(n²) Two Sum.

Algorithmic mirror of bench/brute_force.kara. See ../README.md § Benchmarks
for the choice of N / K and the no-short-circuit target sentinel.
"""

from __future__ import annotations


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return i, j
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
