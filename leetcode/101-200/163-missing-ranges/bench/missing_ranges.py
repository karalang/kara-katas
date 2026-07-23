"""Benchmark workload for LeetCode #163 — Missing Ranges (Python; scale lane)."""


def missing_ranges(arr, start, length, lower, upper):
    count = 0
    checksum = 0
    prev = lower - 1
    i = 0
    while i <= length:
        cur = arr[start + i] if i < length else upper + 1
        if cur - prev >= 2:
            count += 1
            checksum += (prev + 1) + (cur - 1)
        prev = cur
        i += 1
    return count, checksum


def main():
    n = 1000000
    window = 2000
    passes = 120000
    arr = [0] * n
    state = 12345
    val = 0
    for c in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val += 1 + (state % 3)
        arr[c] = val
    span = n - window
    sink = 0
    for p in range(passes):
        start = (p * 7919) % span
        lower = arr[start]
        upper = arr[start + window - 1] + (p % 5)
        count, checksum = missing_ranges(arr, start, window, lower, upper)
        sink += count + checksum
    print(sink)


main()
