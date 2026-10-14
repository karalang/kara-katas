# LeetCode #628: Maximum Product of Three Numbers -- Python mirror of
# the ★ arm.
#
# One pass keeping the three largest and the two smallest values.


def maximum_product(nums):
    max1 = max2 = max3 = -(2**63)
    min1 = min2 = 2**63 - 1
    for v in nums:
        if v > max1:
            max3, max2, max1 = max2, max1, v
        elif v > max2:
            max3, max2 = max2, v
        elif v > max3:
            max3 = v
        if v < min1:
            min2, min1 = min1, v
        elif v < min2:
            min2 = v
    return max(max1 * max2 * max3, max1 * min1 * min2)


seed = 628


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"{nums} -> {maximum_product(nums)}")


def random_values(count, spread):
    return [next_random() % (2 * spread + 1) - spread for _ in range(count)]


def main():
    show([1, 2, 3])
    show([1, 2, 3, 4])
    show([-1, -2, -3])
    show([-10, -10, 1, 3, 2])
    show([-5, -4, -3, -2, -1])
    show([0, 0, 0])
    show([-4, 2, 3])
    show([-3, -2, -1, 0])
    show([-1000, -1000, 1000])
    show([1000, 1000, 1000, -1000])
    show([7, 7, 7, 7, 7])
    show([-6, 5, -6, 1, 2, 4])
    total = 0
    checksum = 0
    for _ in range(300):
        n = 3 + next_random() % 48
        p = maximum_product(random_values(n, 1000))
        total += p
        checksum = (checksum * 31 + p % 1000000007 + 1000000007) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")
    print(f"10000 values: {maximum_product(random_values(10000, 1000))}")
    negative = [-1 - abs(x) % 1000 for x in random_values(10000, 1000)]
    print(f"10000 negative values: {maximum_product(negative)}")
    print(f"10000 small values: {maximum_product(random_values(10000, 10))}")


main()
