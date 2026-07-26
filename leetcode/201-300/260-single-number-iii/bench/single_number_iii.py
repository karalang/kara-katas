#!/usr/bin/env python3
"""Benchmark harness for LeetCode #260 — Single Number III.

Mirrors single_number_iii.kara algorithm-for-algorithm. Kept as a correctness
oracle for the sink; Python is not a measured lane (see ../README.md).
"""


def two_singles(nums):
    x = 0
    for v in nums:
        x ^= v
    bit = x & (0 - x)

    a = 0
    b = 0
    for v in nums:
        if v & bit != 0:
            a ^= v
        else:
            b ^= v
    if a <= b:
        return (a, b)
    return (b, a)


def main():
    np_ = 4
    k = 100000
    iters = 2600

    arrays = []
    for p in range(np_):
        vals = []
        x = p + 1
        for _ in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            vals.append((x // 65536) % 100000)
        arr = []
        for _ in range(2):
            arr.extend(vals)
        arr.append(999983 + p)
        arr.append(1000003 + p)
        arrays.append(arr)

    sink = 0
    for it in range(iters):
        idx = (it * 3) % np_
        r0, r1 = two_singles(arrays[idx])
        sink = (sink * 31 + r0 + r1 * 7) % 1000000007
    print(sink)


main()
