"""Benchmark workload for LeetCode #162 — Find Peak Element (Python; scale lane)."""


def find_peak(arr, lo, hi):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main():
    n = 4000000
    window = 4096
    passes = 1000000
    arr = [0] * n
    state = 12345
    for c in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        arr[c] = state % 1000003
    span = n - window
    sink = 0
    for p in range(passes):
        base = (p * 4099) % span
        arr[base] = (arr[base] + 1) % 1000003
        sink += find_peak(arr, base, base + window - 1)
    print(sink)


main()
