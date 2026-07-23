"""Benchmark workload for LeetCode #219 — Contains Duplicate II (Python; scale lane)."""


def count_nearby(nums, k):
    last = {}
    n = len(nums)
    hits = 0
    for i in range(n):
        x = nums[i]
        j = last.get(x)
        if j is not None and i - j <= k:
            hits += 1
        last[x] = i
    return hits


def main():
    n = 1000000
    kmax = 40
    m = 49999

    nums = []
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        nums.append(state % m)

    sink = 0
    for k in range(1, kmax + 1):
        sink += count_nearby(nums, k)
    print(sink)


main()
