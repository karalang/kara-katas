"""Benchmark workload for LeetCode #231 — Power of Two (Python; scale lane)."""


def is_power_of_two(n):
    if n <= 0:
        return False
    return (n & (n - 1)) == 0


def main():
    n = 130000000
    mask = 1023
    state = 12345
    sink = 0
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        v = state & mask
        if is_power_of_two(v):
            sink += 1
    print(sink)


main()
