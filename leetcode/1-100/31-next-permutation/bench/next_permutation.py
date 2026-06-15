#!/usr/bin/env python3
"""LeetCode #31 bench — Python (mirror of next_permutation.kara).

Canonical four-move next-permutation, enumerating all K! permutations REPEAT
times and folding a rolling checksum. Same sink as every other mirror.
"""


def next_permutation(nums, length):
    i = length - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = length - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    lo, hi = i + 1, length - 1
    while lo < hi:
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo += 1
        hi -= 1


def main():
    k = 10
    fact = 3628800  # 10!
    repeat = 8
    modulus = 2147483647  # 2^31 - 1

    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    acc = 0

    for _ in range(repeat):
        for _step in range(fact):
            h = 0
            for i in range(k):
                h = (h * 131 + nums[i]) % modulus
            acc = (acc + h) % modulus
            next_permutation(nums, k)

    print(acc)


if __name__ == "__main__":
    main()
