"""Benchmark workload for LeetCode #172 — Factorial Trailing Zeroes (Python; scale lane)."""


def trailing_zeroes(n):
    count = 0
    m = n // 5
    while m > 0:
        count += m
        m //= 5
    return count


def main():
    limit = 35000000
    sink = 0
    for i in range(limit):
        sink += trailing_zeroes(i)
    print(sink)


main()
