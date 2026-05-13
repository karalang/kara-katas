"""LeetCode #1: Two Sum — hash-map O(n).

Idiomatic Python: a single dict maps each seen value to its index, so
finding the complement is O(1) per element. Output format matches
brute_force.kara line-for-line so the two can be diffed directly.
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


def report(nums: list[int], target: int) -> None:
    result = two_sum(nums, target)
    if result is None:
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
