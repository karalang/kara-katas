# LeetCode #908: Smallest Range I -- bench program, Python.
#
# The largest and smallest values, over 500,000 numbers up to 10^4 built
# once. Each round scores them with a k that changes from round to round,
# folds the score into a checksum and changes one number.


def smallest_range_i(nums, k):
    lo = nums[0]
    hi = nums[0]
    for i in range(1, len(nums)):
        lo = min(lo, nums[i])
        hi = max(hi, nums[i])
    return max(hi - lo - 2 * k, 0)


seed = 908


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 500000
    rounds = 500
    nums = [next_random() % 10001 for _ in range(n)]
    total = 0
    check = 0
    for r in range(rounds):
        got = smallest_range_i(nums, r * 37 % 5001)
        total += got
        check = (check * 31 + got) % 1000000007
        nums[r * 7919 % n] = next_random() % 10001
    print(f"{rounds} rounds over {n} numbers: scores summing to {total}, checksum {check}")


main()
