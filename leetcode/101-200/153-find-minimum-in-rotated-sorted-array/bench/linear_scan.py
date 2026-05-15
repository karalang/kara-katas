"""Benchmark workload — linear scan find-min on a rotated sorted array.

Algorithmic mirror of bench/linear_scan.kara. See ../README.md § Benchmarks
for the choice of N / K and the rotated-sorted generator.
"""

from __future__ import annotations


def find_min(nums: list[int]) -> int:
    n = len(nums)
    m = nums[0]
    for i in range(1, n):
        x = nums[i]
        if x < m:
            m = x
    return m


def main() -> None:
    N = 2_000_000
    R = 666_666
    data: list[int] = []
    for i in range(N):
        data.append(((i + R) % N) + 1)

    sum_result = 0
    for _ in range(10):
        sum_result += find_min(data)
    print(sum_result)


if __name__ == "__main__":
    main()
