#!/usr/bin/env python3
"""Benchmark harness for LeetCode #274 — H-Index.

Mirrors h_index.kara algorithm-for-algorithm. Kept as a correctness oracle for
the sink; Python is not a measured lane (see ../README.md).
"""


def h_index(cit):
    v = list(cit)
    v.sort()
    n = len(v)
    for j in range(n):
        if v[j] >= n - j:
            return n - j
    return 0


def main():
    np_ = 4
    n = 60000
    iters = 600

    arrays = []
    for p in range(np_):
        arr = []
        x = p + 1
        for t in range(n):
            x = (x * 1103515245 + 12345) % 2147483648
            r = (x // 65536) % 32768
            if p == 0:
                arr.append(r % 30000)
            elif p == 1:
                arr.append(r % 40)
            elif p == 2:
                arr.append((r % 7) * 3000)
            else:
                arr.append(t + (r % 5))
        arrays.append(arr)

    sink = 0
    for it in range(iters):
        idx = (it * 3) % np_
        sink = (sink * 31 + h_index(arrays[idx])) % 1000000007
    print(sink)


main()
