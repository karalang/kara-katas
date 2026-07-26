#!/usr/bin/env python3
"""Benchmark harness for LeetCode #287 — Find the Duplicate Number.

Mirrors find_duplicate.kara algorithm-for-algorithm. Kept as a correctness
oracle for the sink; Python is not a measured lane (see ../README.md).
"""


def find_duplicate(nums):
    slow = nums[0]
    fast = nums[0]
    slow = nums[slow]
    fast = nums[nums[fast]]
    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]
    finder = nums[0]
    while finder != slow:
        finder = nums[finder]
        slow = nums[slow]
    return finder


def main():
    np_ = 4
    n = 200000
    iters = 80

    arrays = []
    for p in range(np_):
        order = list(range(1, n + 1))
        x = p + 12345
        for k in range(n - 1, 0, -1):
            x = (x * 1103515245 + 12345) % 2147483648
            j = (x // 65536) % (k + 1)
            order[k], order[j] = order[j], order[k]

        arr = [0] * (n + 1)
        for t in range(n):
            nxt = (t + 1) % n
            arr[order[t]] = order[nxt]
        arr[0] = order[p * 37]
        arrays.append(arr)

    sink = 0
    for it in range(iters):
        idx = (it * 3) % np_
        sink = (sink * 31 + find_duplicate(arrays[idx])) % 1000000007
    print(sink)


main()
