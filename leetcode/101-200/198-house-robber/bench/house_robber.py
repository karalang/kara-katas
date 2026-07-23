"""Benchmark workload for LeetCode #198 — House Robber (Python; scale lane)."""


def rob(nums, n):
    prev2 = 0
    prev = 0
    for i in range(n):
        v = prev2 + nums[i]
        cur = v if v > prev else prev
        prev2 = prev
        prev = cur
    return prev


def main():
    n = 5000
    passes = 90000
    nums = [0] * n
    state = 12345
    for b in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        nums[b] = (state >> 16) % 1000
    sink = 0
    for _ in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        idx = state % n
        nums[idx] = (state >> 16) % 1000
        sink += rob(nums, n)
    print(sink)


main()
