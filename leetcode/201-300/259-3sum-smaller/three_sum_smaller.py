"""LeetCode 259 - 3Sum Smaller. Python oracle.

Mirrors three_sum_smaller.kara algorithm-for-algorithm: sort, then two pointers
per i, counting (hi - lo) whole runs at a time.
"""


def three_sum_smaller(nums, target):
    s = sorted(nums)
    n = len(s)
    count = 0
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        while lo < hi:
            if s[i] + s[lo] + s[hi] < target:
                count += hi - lo
                lo += 1
            else:
                hi -= 1
    return count


def main():
    cases = [
        ([-2, 0, 1, 3], 2, "[-2,0,1,3]"),
        ([], 0, "[]"),
        ([0, 0], 5, "[0,0]"),
        ([0, 0, 0], 1, "[0,0,0]"),
        ([0, 0, 0], 0, "[0,0,0]"),
        ([-5, -4, -3, -2, -1], 0, "[-5,-4,-3,-2,-1]"),
        ([1, 1, 1, 1, 1], 4, "[1,1,1,1,1]"),
        ([-10, -5, 0, 1, 2, 3], 5, "[-10,-5,0,1,2,3]"),
        ([3, 2, 1, 0, -1], 3, "[3,2,1,0,-1] (reversed)"),
        ([-1, 0, 1, 2, 3], 3, "[-1,0,1,2,3] (sorted)"),
    ]
    for nums, t, label in cases:
        print(f"{label} t={t} -> {three_sum_smaller(nums, t)}")


if __name__ == "__main__":
    main()
