"""Benchmark workload — Search in Rotated Sorted Array II (LeetCode #81).

Python mirror of bench/search_rotated_ii.kara. Build-once + punch: one rotated sorted
array with duplicates (each value 0..M appears twice, M=1000, rotated) built once,
then searched for targets sweeping present/absent values, each boolean folded through
a rolling polynomial hash. Runs a smaller K (pure-Python is slow); timed separately,
NOT cross-checked. See ../README.md.
"""


def search(nums, length, target):
    lo = 0
    hi = length - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] and nums[mid] == nums[hi]:
            lo += 1
            hi -= 1
        elif nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False


def build(m, dup, rot):
    base = []
    for v in range(m):
        for _ in range(dup):
            base.append(v)
    n = len(base)
    return [base[(i + rot) % n] for i in range(n)]


def main():
    m = 1000
    dup = 2
    total = 300000
    modulus = 1000000007
    arr = build(m, dup, (m * dup) // 3)
    n = len(arr)
    span = m + 50
    total_sum = 0
    for it in range(total):
        target = it % span
        found = search(arr, n, target)
        bit = 1 if found else 0
        total_sum = (total_sum * 131 + bit + 1) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
