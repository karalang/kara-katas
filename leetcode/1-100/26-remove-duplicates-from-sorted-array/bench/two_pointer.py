"""Benchmark workload — two-pointer in-place O(n) Remove Duplicates.

Algorithmic mirror of bench/two_pointer.kara. See ../README.md § Benchmarks
for the choice of N, K and the LCG-random-gap input.
"""

from __future__ import annotations


def remove_duplicates(nums: list[int], length: int) -> int:
    if length == 0:
        return 0
    k = 1
    for i in range(1, length):
        if nums[i] != nums[k - 1]:
            nums[k] = nums[i]
            k += 1
    return k


def main() -> None:
    n = 2_000_000

    original = [0] * n
    state = 1
    for i in range(1, n):
        state = (state * 1103515245 + 12345) % 2147483648
        original[i] = original[i - 1] + (state // 65536) % 2

    workspace = [0] * n

    sum_result = 0
    for _ in range(10):
        for p in range(n):
            workspace[p] = original[p]
        k = remove_duplicates(workspace, n)
        sum_result += k + workspace[k - 1]
    print(sum_result)


if __name__ == "__main__":
    main()
