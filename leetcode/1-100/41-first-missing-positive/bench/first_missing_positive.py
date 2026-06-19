"""LeetCode #41 bench mirror — Python, the in-place cyclic-sort solver (★).

Mirrors bench/first_missing_positive.kara: swap each in-range value to its home index v-1,
then scan for the first slot not holding its home value. Buffer reused in place each
iteration. Same workload + sink as every other mirror — the slow interpreter foil.
"""

from __future__ import annotations

TOTAL = 200000
N = 100
MODULUS = 1000000007


def first_missing_positive(nums: list[int], n: int) -> int:
    i = 0
    while i < n:
        v = nums[i]
        if 1 <= v <= n and nums[v - 1] != v:
            nums[v - 1], nums[i] = v, nums[v - 1]
        else:
            i += 1
    j = 0
    while j < n:
        if nums[j] != j + 1:
            return j + 1
        j += 1
    return n + 1


def main() -> None:
    nums = [0] * N
    acc = 0
    for k in range(TOTAL):
        rot = k % N
        i = 0
        while i < N:
            nums[i] = ((i + rot) % N) + 1
            i += 1
        nums[k % N] = N + 7

        ans = first_missing_positive(nums, N)
        acc = (acc * 131 + ans) % MODULUS

    print(acc)


if __name__ == "__main__":
    main()
