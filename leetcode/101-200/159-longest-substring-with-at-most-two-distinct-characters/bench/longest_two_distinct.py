"""Benchmark workload for LeetCode #159 — Longest Substring with At Most Two
Distinct Characters (Python; scale lane). Count table modeled as a flat list."""


def longest(buf, lo, hi, alphabet):
    counts = [0] * alphabet
    for a in range(alphabet):
        counts[a] = 0
    distinct = 0
    left = lo
    best = 0
    right = lo
    while right < hi:
        c = buf[right]
        if counts[c] == 0:
            distinct += 1
        counts[c] += 1
        while distinct > 2:
            lc = buf[left]
            counts[lc] -= 1
            if counts[lc] == 0:
                distinct -= 1
            left += 1
        w = right - left + 1
        if w > best:
            best = w
        right += 1
    return best


def main():
    size = 20000
    alphabet = 8
    width = 96
    reps = 100

    buf = [0] * size
    state = 12345
    for c in range(size):
        state = (state * 1103515245 + 12345) & 2147483647
        buf[c] = state % alphabet

    ranges = size - width
    sink = 0
    for rep in range(reps):
        idx = (rep * 131 + 7) % size
        buf[idx] = (buf[idx] + 1) % alphabet
        start = 0
        while start < ranges:
            sink += longest(buf, start, start + width, alphabet)
            start += 1
    print(sink)


main()
