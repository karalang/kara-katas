"""Benchmark harness for LeetCode #128 — Longest Consecutive Sequence.

Mirrors longest_consecutive.kara algorithm-for-algorithm. Committed as the
correctness oracle; not a measured lane.
"""

NP = 8
N = 20000
CAPV = 25000
ITERS = 150


def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for v in nums:
        if (v - 1) not in s:
            length = 1
            cur = v
            while (cur + 1) in s:
                cur += 1
                length += 1
            if length > best:
                best = length
    return best


def lcg(seed, n, cap):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(x % cap)
    return out


def main():
    arrays = [lcg(j + 1, N, CAPV) for j in range(NP)]

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % NP
        sink += longest_consecutive(arrays[idx])
    print(sink)


if __name__ == "__main__":
    main()
