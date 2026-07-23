"""Benchmark workload for LeetCode #167 — Two Sum II (Python; scale lane)."""


def two_sum(arr, target):
    lo = 0
    hi = len(arr) - 1
    while lo < hi:
        s = arr[lo] + arr[hi]
        if s == target:
            return lo + 1, hi + 1
        if s < target:
            lo += 1
        else:
            hi -= 1
    return -1, -1  # unreachable — a solution is guaranteed


def main():
    n = 20000
    passes = 20000
    arr = [0] * n
    state = 12345
    val = 0
    for c in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val += 1 + (state % 3)
        arr[c] = val
    sink = 0
    for _p in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        a = state % n
        state = (state * 1103515245 + 12345) & 2147483647
        b = state % n
        if a == b:
            b = (a + 1) % n
        target = arr[a] + arr[b]
        lo, hi = two_sum(arr, target)
        sink += lo + hi
    print(sink)


main()
