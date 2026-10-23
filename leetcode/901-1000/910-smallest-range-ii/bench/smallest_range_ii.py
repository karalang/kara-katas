# LeetCode #910: Smallest Range II -- bench program, Python.
#
# The sorted values split in two, over 500,000 numbers up to 10^4 built
# once. Each round solves them with a k that changes from round to round,
# folds the score into a checksum and changes one number.


def smallest_range_ii(nums, k):
    a = sorted(nums)
    n = len(a)
    best = a[n - 1] - a[0]
    for i in range(n - 1):
        hi = max(a[i] + k, a[n - 1] - k)
        lo = min(a[0] + k, a[i + 1] - k)
        best = min(best, hi - lo)
    return best


seed = 910


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 500000
    rounds = 40
    nums = [next_random() % 10001 for _ in range(n)]
    total = 0
    check = 0
    for r in range(rounds):
        got = smallest_range_ii(nums, r * 373 % 5001)
        total += got
        check = (check * 31 + got) % 1000000007
        nums[r * 7919 % n] = next_random() % 10001
    print(f"{rounds} rounds over {n} numbers: scores summing to {total}, checksum {check}")


main()
