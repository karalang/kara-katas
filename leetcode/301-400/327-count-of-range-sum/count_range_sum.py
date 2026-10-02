"""LeetCode #327: Count of Range Sum — Python mirror.

Mirrors count_range_sum.kara (merge sort over the prefix sums) and
count_range_sum_brute.kara (every start, every end). Prints the same lines;
run with `--brute` for the quadratic arm.
"""
import sys


def count_and_sort(p, tmp, lo, hi, lower, upper):
    if hi - lo <= 1:
        return 0
    mid = lo + (hi - lo) // 2
    count = count_and_sort(p, tmp, lo, mid, lower, upper) + count_and_sort(p, tmp, mid, hi, lower, upper)
    start = end = mid
    for a in range(lo, mid):
        while start < hi and p[start] < p[a] + lower:
            start += 1
        while end < hi and p[end] <= p[a] + upper:
            end += 1
        count += end - start
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if p[i] <= p[j]:
            tmp[k] = p[i]
            i += 1
        else:
            tmp[k] = p[j]
            j += 1
        k += 1
    while i < mid:
        tmp[k] = p[i]
        i += 1
        k += 1
    while j < hi:
        tmp[k] = p[j]
        j += 1
        k += 1
    p[lo:hi] = tmp[lo:hi]
    return count


def count_range_sum(nums, lower, upper):
    p = [0]
    for x in nums:
        p.append(p[-1] + x)
    tmp = [0] * len(p)
    return count_and_sort(p, tmp, 0, len(p), lower, upper)


def count_range_sum_brute(nums, lower, upper):
    count = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if lower <= s <= upper:
                count += 1
    return count


SOLVE = count_range_sum_brute if "--brute" in sys.argv else count_range_sum


def report(nums, lower, upper):
    print(f"[{', '.join(map(str, nums))}] [{lower}, {upper}] -> {SOLVE(nums, lower, upper)}")


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_input(n, r, rng):
    return [rng.next() % (2 * r + 1) - r for _ in range(n)]


I32_MIN = -2147483648
I32_MAX = 2147483647


def main():
    report([-2, 5, -1], -2, 2)
    report([0], 0, 0)
    report([1], 0, 0)
    report([5], 5, 5)
    report([0, 0, 0], 0, 0)
    report([1, -1, 1, -1], 0, 0)
    report([3, 3, 3], 4, 5)
    report([1, 2, 3], -100, 100)
    report([-1, -2, -3], 1, 100)
    report([2, -2, 2, -2, 2], -1, 1)
    report([I32_MAX, I32_MAX, I32_MAX], 4294967294, 6442450941)
    report([I32_MIN, I32_MAX, I32_MIN], I32_MIN, -1)
    rng = Rng(327)
    for t in range(4):
        report(random_input(8, 5, rng), t - 2, t + 2)
    for n in (500, 2000, 3000):
        nums = random_input(n, 100, rng)
        for w in (0, 10, 100, 1000):
            print(f"n={n} w={w} -> {SOLVE(nums, -w, w)}")


main()
