#!/usr/bin/env python3
"""Benchmark harness for LeetCode #137 — Single Number II.

Mirrors single_number.kara algorithm-for-algorithm. Kept as a correctness
oracle for the sink; Python is not a measured lane (see ../README.md).
"""

MASK = 4294967295


def sign_extend32(v):
    if v >= 2147483648:
        return v - 4294967296
    return v


def single_ones_twos(nums):
    ones = 0
    twos = 0
    for v in nums:
        x = v & MASK
        ones = (ones ^ x) & (~twos) & MASK
        twos = (twos ^ x) & (~ones) & MASK
    return sign_extend32(ones)


def single_bitcount(nums):
    res = 0
    for b in range(32):
        cnt = 0
        for v in nums:
            if (v >> b) & 1 == 1:
                cnt += 1
        if cnt % 3 != 0:
            res |= 1 << b
    return sign_extend32(res)


def main():
    np_ = 4
    k = 30000
    iters = 40

    arrays = []
    for j in range(np_):
        vals = []
        x = j + 1
        for _ in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            vals.append((x // 65536) % 100000)
        arr = []
        for _ in range(3):
            arr.extend(vals)
        arr.append(999983 + j)
        arrays.append(arr)

    sink = 0
    for it in range(iters):
        idx = (it * 3) % np_
        a = single_ones_twos(arrays[idx])
        b = single_bitcount(arrays[idx])
        if a != b:
            sink += 1000000000
        sink = (sink + a + b) % 1000000007
    print(sink)


main()
