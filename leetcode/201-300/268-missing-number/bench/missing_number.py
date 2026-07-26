#!/usr/bin/env python3
"""Benchmark harness for LeetCode #268 — Missing Number.

Mirrors missing_number.kara algorithm-for-algorithm. Kept as a correctness
oracle for the sink; Python is not a measured lane (see ../README.md).
"""


def missing_number(nums):
    n = len(nums)
    acc = n
    for i in range(n):
        acc = acc ^ i ^ nums[i]
    return acc


def main():
    np_ = 4
    n = 1000000
    iters = 850

    arrays = []
    for p in range(np_):
        missing = 200000 * p + 137
        arr = [0] * n
        v = 0
        for t in range(n):
            if v == missing:
                v += 1
            idx = (t * 499979) % n
            arr[idx] = v
            v += 1
        arrays.append(arr)

    sink = 0
    for it in range(iters):
        idx = (it * 3) % np_
        sink = (sink * 31 + missing_number(arrays[idx])) % 1000000007
    print(sink)


main()
