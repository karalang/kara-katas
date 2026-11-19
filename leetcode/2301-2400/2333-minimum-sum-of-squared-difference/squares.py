# LeetCode #2333: Minimum Sum of Squared Difference -- the Python mirror
# of the ★ arm: the gaps counted by size, the largest dropped a level at
# a time while the moves cover them, and the moves left taking that many
# of the rest one lower.


def min_sum_square_diff(nums1, nums2, k1, k2):
    count = [0] * 100001
    top = 0
    for a, b in zip(nums1, nums2):
        gap = abs(a - b)
        count[gap] += 1
        top = max(top, gap)
    moves = k1 + k2
    level = top
    while level > 0 and moves >= count[level]:
        moves -= count[level]
        count[level - 1] += count[level]
        count[level] = 0
        level -= 1
    if level > 0:
        count[level] -= moves
        count[level - 1] += moves
    return sum(count[gap] * gap * gap for gap in range(1, level + 1))


SEED = [2333]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def random_nums(n, top):
    return [next_random() % (top + 1) for _ in range(n)]


def main():
    print(min_sum_square_diff([1, 2, 3, 4], [2, 10, 20, 19], 0, 0))
    print(min_sum_square_diff([1, 4, 10, 12], [5, 8, 6, 9], 1, 1))
    print(min_sum_square_diff([7, 0, 3], [2, 4, 3], 4, 5))
    print(min_sum_square_diff([5, 5, 5], [5, 5, 5], 3, 0))
    print(min_sum_square_diff([0], [100000], 1000000000, 0))
    big1 = random_nums(2000, 100000)
    big2 = random_nums(2000, 100000)
    print(min_sum_square_diff(big1, big2, 25000, 35000))
    check = 0
    total = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        nums1 = random_nums(n, 30)
        nums2 = random_nums(n, 30)
        k1 = next_random() % 41
        k2 = next_random() % 41
        least = min_sum_square_diff(nums1, nums2, k1, k2)
        check = (check * 31 + least) % 1000000007
        total += least
    print(f"2000 cases: checksum {check}, total {total}")


main()
