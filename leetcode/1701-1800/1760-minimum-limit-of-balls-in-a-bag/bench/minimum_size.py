# LeetCode #1760: Minimum Limit of Balls in a Bag -- the bench in Python,
# mirroring minimum_size.kara: a binary search on the penalty.
def operations(nums, penalty):
    return sum((x - 1) // penalty for x in nums)


def minimum_size(nums, max_operations):
    lo, hi = 1, max(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if operations(nums, mid) <= max_operations:
            hi = mid
        else:
            lo = mid + 1
    return lo


def main():
    seed = 1760
    bags = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        bags.append(1 + (high * 32768 + seed // 65536) % 1000000000)
    check = 0
    for call in range(100):
        at = (check + call * 7919) % 100000
        bags[at] = 1 + (check * 13 + call) % 1000000000
        ops = 1 + (check + call * 104729) % 1000000000
        check = (check * 31 + minimum_size(bags, ops)) % 1000000007
    print(f"100 calls over 100000 bags: checksum {check}")


main()
