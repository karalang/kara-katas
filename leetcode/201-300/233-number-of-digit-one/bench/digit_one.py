"""Benchmark workload for LeetCode #233 — Number of Digit One (Python; scale lane)."""


def count_digit_one(n):
    if n < 0:
        return 0
    count = 0
    pos = 1
    while pos <= n:
        high = n // (pos * 10)
        cur = (n // pos) % 10
        low = n % pos
        if cur == 0:
            count += high * pos
        elif cur == 1:
            count += high * pos + low + 1
        else:
            count += (high + 1) * pos
        pos *= 10
    return count


def main():
    limit = 6000000
    sink = 0
    for i in range(limit):
        sink += count_digit_one(i)
    print(sink)


main()
