"""Benchmark workload for LeetCode #168 — Excel Sheet Column Title (Python; scale lane)."""


def col_checksum(n):
    x = n
    acc = 0
    while x > 0:
        x -= 1  # bijective base-26: shift to 0-based digit
        acc += 65 + (x % 26)  # 'A' = 65
        x //= 26
    return acc


def main():
    limit = 50000000
    sink = 0
    n = 1
    while n <= limit:
        sink += col_checksum(n)
        n += 1
    print(sink)


main()
