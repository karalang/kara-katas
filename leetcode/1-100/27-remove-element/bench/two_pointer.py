"""Benchmark workload — two-pointer in-place O(n) Remove Element.

Algorithmic mirror of bench/two_pointer.kara. See ../README.md § Benchmarks
for the choice of N, K and the LCG ~50%-match input.
"""

from __future__ import annotations


def remove_element(nums: list[int], length: int, val: int) -> int:
    k = 0
    for i in range(length):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    return k


def main() -> None:
    n = 2_000_000
    val = 0

    original = [0] * n
    state = 1
    for i in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        if (state // 65536) % 2 == 1:
            original[i] = i + 1
        else:
            original[i] = 0

    workspace = [0] * n

    sum_result = 0
    for _ in range(10):
        for p in range(n):
            workspace[p] = original[p]
        k = remove_element(workspace, n, val)
        sum_result += k + workspace[k - 1]
    print(sum_result)


if __name__ == "__main__":
    main()
