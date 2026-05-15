"""Benchmark workload — binary search find-min on a rotated sorted array.

Algorithmic mirror of bench/binary_search.kara. See ../README.md § Benchmarks
for the choice of N / K and the rotated-sorted generator.
"""

from __future__ import annotations


def find_min(nums: list[int]) -> int:
    lo = 0
    hi = len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


def main() -> None:
    N = 2_000_000
    R = 666_666
    data: list[int] = []
    for i in range(N):
        data.append(((i + R) % N) + 1)

    sum_result = 0
    for _ in range(2_000_000):
        sum_result += find_min(data)
    print(sum_result)


if __name__ == "__main__":
    main()
