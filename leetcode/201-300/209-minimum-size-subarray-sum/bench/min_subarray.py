"""Benchmark workload for LeetCode #209 — Minimum Size Subarray Sum (Python; scale lane)."""


def min_subarray_len(target, nums, n):
    left = 0
    sum_ = 0
    best = -1
    right = 0
    while right < n:
        sum_ += nums[right]
        while sum_ >= target:
            length = right - left + 1
            if best == -1 or length < best:
                best = length
            sum_ -= nums[left]
            left += 1
        right += 1
    return 0 if best == -1 else best


def main():
    n = 200000
    targets = 290

    nums = []
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        nums.append(1 + state % 100)  # 1..100, all positive

    sink = 0
    for t in range(targets):
        target = 200 + t * 80
        sink += min_subarray_len(target, nums, n)

    print(sink)


main()
