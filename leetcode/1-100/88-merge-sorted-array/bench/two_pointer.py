"""Benchmark workload — two-pointer-from-back O(m + n) Merge Sorted Array.

Algorithmic mirror of bench/two_pointer.kara. See ../README.md § Benchmarks
for the choice of m, n, K and the maximally-alternating input.
"""

from __future__ import annotations


def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    i = m - 1
    j = n - 1
    k = m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1


def main() -> None:
    M = 1_000_000
    N = 1_000_000
    total = M + N

    prefix_a = [2 * i for i in range(M)]
    b = [2 * i + 1 for i in range(N)]

    workspace = [0] * total

    sum_result = 0
    for _ in range(10):
        for p in range(M):
            workspace[p] = prefix_a[p]
        merge(workspace, M, b, N)
        sum_result += workspace[total - 1]
    print(sum_result)


if __name__ == "__main__":
    main()
