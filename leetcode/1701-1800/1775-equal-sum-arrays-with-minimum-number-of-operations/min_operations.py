# LeetCode #1775: Equal Sum Arrays With Minimum Number of Operations -- a
# Python mirror of the ★ arm: the gains counted by size, the largest taken
# first until the gap is closed.


def min_operations(nums1, nums2):
    sum1, sum2 = sum(nums1), sum(nums2)
    if sum1 == sum2:
        return 0
    low, high = (nums1, nums2) if sum1 < sum2 else (nums2, nums1)
    gap = abs(sum1 - sum2)
    gains = [0] * 6
    for x in low:
        gains[6 - x] += 1
    for x in high:
        gains[x - 1] += 1
    ops = 0
    for g in range(5, 0, -1):
        while gains[g] > 0 and gap > 0:
            gap -= g
            gains[g] -= 1
            ops += 1
    return -1 if gap > 0 else ops


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n dice from `low` to `high`
def random_dice(n, low, high):
    return [low + next_random() % (high - low + 1) for _ in range(n)]


def main():
    global seed
    # LeetCode's three examples
    print(f"{min_operations([1, 2, 3, 4, 5, 6], [1, 1, 2, 2, 2, 2])} {min_operations([1, 1, 1, 1, 1, 1, 1], [6])} {min_operations([6, 6], [1])}")
    # the edges
    print(f"{min_operations([3], [3])} {min_operations([1], [6])} {min_operations([1, 1], [6, 6])} {min_operations([1, 1, 1, 1, 1, 1, 1], [6])} {min_operations([1, 1, 1, 1, 1, 1], [6])}")
    # the constraints' most
    seed = 1775
    ones = [1] * 100000
    sixes = [6] * 100000
    a = random_dice(100000, 1, 6)
    b = random_dice(100000, 2, 6)
    print(f"the most: {min_operations(ones, sixes)} {min_operations(a, b)}")
    # 3000 random cases
    check = 0
    for _ in range(3000):
        n1 = 1 + next_random() % 20
        n2 = 1 + next_random() % 20
        low1 = 1 + next_random() % 6
        low2 = 1 + next_random() % 6
        nums1 = random_dice(n1, low1, 6)
        nums2 = random_dice(n2, 1, 7 - low2)
        check = (check * 31 + min_operations(nums1, nums2) + 1) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
