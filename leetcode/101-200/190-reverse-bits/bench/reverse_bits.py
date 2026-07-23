"""Benchmark workload for LeetCode #190 — Reverse Bits (Python; scale lane)."""


def reverse_bits(n):
    result = 0
    x = n
    for _ in range(32):
        result = (result << 1) | (x & 1)
        x >>= 1
    return result


def main():
    count = 8000000
    state = 12345
    sink = 0
    for _ in range(count):
        state = (state * 1103515245 + 12345) & 2147483647
        sink += reverse_bits(state)
    print(sink)


main()
