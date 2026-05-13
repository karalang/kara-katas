"""LeetCode #1: Two Sum — brute-force O(n²).

Algorithmic mirror of brute_force.kara. Output format matches line-for-line
so the two can be diffed directly.
"""

from __future__ import annotations


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return i, j
    return None


def report(nums: list[int], target: int) -> None:
    result = two_sum(nums, target)
    if result is None:
        print(-1)
        print(-1)
    else:
        print(result[0])
        print(result[1])


def main() -> None:
    report([2, 7, 11, 15], 9)   # expect: 0, 1
    report([3, 2, 4], 6)        # expect: 1, 2
    report([3, 3], 6)           # expect: 0, 1


if __name__ == "__main__":
    main()
