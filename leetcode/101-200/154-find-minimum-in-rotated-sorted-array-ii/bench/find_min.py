"""Benchmark workload for LeetCode #154 — Find Minimum in Rotated Sorted Array II (Python; scale lane)."""


def find_min(nums, n):
    lo = 0
    hi = n - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        elif nums[mid] < nums[hi]:
            hi = mid
        else:
            hi = hi - 1
    return nums[lo]


def main():
    n = 2000
    punches = 75000
    arr = [0] * n

    state = 12345
    sink = 0
    for _pn in range(punches):
        state = (state * 1103515245 + 12345) & 2147483647
        start = state % 1000000
        state = (state * 1103515245 + 12345) & 2147483647
        rot = state % n

        cur = start
        for k in range(n):
            state = (state * 1103515245 + 12345) & 2147483647
            inc = (state // 5) % 4 if state % 5 == 0 else 0
            cur += inc
            arr[(k + rot) % n] = cur

        sink += find_min(arr, n)
    print(sink)


main()
