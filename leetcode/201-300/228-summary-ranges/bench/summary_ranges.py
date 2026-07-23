"""Benchmark workload for LeetCode #228 — Summary Ranges (Python; scale lane)."""


def summary_metric(nums, n):
    i = 1
    start = nums[0]
    ranges = 0
    esum = 0
    while i <= n:
        if i == n or nums[i] != nums[i - 1] + 1:
            end = nums[i - 1]
            ranges += 1
            esum += start + end
            if i < n:
                start = nums[i]
        i += 1
    return ranges + esum


def main():
    n = 1000000
    passes = 250

    nums = []
    state = 12345
    v = 0
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        v = v + 1 + (state % 3)
        nums.append(v)

    sink = 0
    for _ in range(passes):
        sink += summary_metric(nums, n)
    print(sink)


main()
