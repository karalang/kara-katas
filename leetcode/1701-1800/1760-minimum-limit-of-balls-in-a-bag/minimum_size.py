# LeetCode #1760: Minimum Limit of Balls in a Bag -- the ★ arm in Python,
# with the same harness.
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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_bags(n, most):
    bags = []
    for _ in range(n):
        r = next_random() * 32768
        r += next_random()
        bags.append(1 + r % most)
    return bags


def main():
    global seed
    print(f"{minimum_size([9], 2)} {minimum_size([2, 4, 8, 2], 4)}")
    print(" ".join(str(minimum_size(a, m)) for a, m in [([1, 1, 1], 5), ([1], 1), ([3, 5], 6), ([3, 5], 5), ([7, 7, 7, 7], 4), ([1000000000], 1)]))
    seed = 1760
    big = random_bags(100000, 1000000000)
    print(f"100000 bags: {minimum_size(big, 1)} {minimum_size(big, 100000)} {minimum_size(big, 1000000000)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        bags = random_bags(n, 60)
        ops = 1 + next_random() % 40
        check = (check * 31 + minimum_size(bags, ops)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
