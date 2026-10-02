"""LeetCode #325: Maximum Size Subarray Sum Equals k — Python mirror.

Mirrors max_sub_len.kara (prefix sums, first index per prefix sum) and
max_sub_len_brute.kara (every start, every end). Prints the same lines; run
with `--brute` for the quadratic arm.
"""
import sys


def max_sub_len(nums, k):
    first = {0: -1}
    p = 0
    best = 0
    for i, x in enumerate(nums):
        p += x
        j = first.get(p - k)
        if j is not None and i - j > best:
            best = i - j
        if p not in first:
            first[p] = i
    return best


def max_sub_len_brute(nums, k):
    n = len(nums)
    best = 0
    for j in range(n):
        s = 0
        for i in range(j, n):
            s += nums[i]
            if s == k and i - j + 1 > best:
                best = i - j + 1
    return best


SOLVE = max_sub_len_brute if "--brute" in sys.argv else max_sub_len


def report(nums, k):
    print(f"{nums} k={k} -> {SOLVE(nums, k)}")


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_input(n, r, rng):
    return [rng.next() % (2 * r + 1) - r for _ in range(n)]


def tdiv(a, b):
    """Integer division truncating toward zero, as Kara's `/` does."""
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def main():
    report([1, -1, 5, -2, 3], 3)
    report([-2, -1, 2, 1], 1)
    report([1, 2, 3], 7)
    report([5], 4)
    report([5], 5)
    report([1, 2, 3], 6)
    report([3, -3, 1, -1, 2], 0)
    report([0, 0, 0, 0], 0)
    report([1, -1, 1, -1, 1, -1], 0)
    report([-5, 2, -3, 4, -1], -6)
    report([10000, -10000, 10000, -10000, 10000], 10000)

    rng = Rng(325)
    for n, r in zip([6, 9, 12, 15], [2, 3, 5, 1]):
        a = random_input(n, r, rng)
        k = rng.next() % 7 - 3
        report(a, k)

    for n, r in zip([500, 2000, 3000], [3, 50, 10000]):
        a = random_input(n, r, rng)
        for _ in range(4):
            k = tdiv((rng.next() % 41 - 20) * r, 4)
            print(f"n={n} r={r} k={k} -> {SOLVE(a, k)}")


if __name__ == "__main__":
    main()
