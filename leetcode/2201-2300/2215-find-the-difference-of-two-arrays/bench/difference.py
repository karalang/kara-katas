# LeetCode #2215: Find the Difference of Two Arrays -- bench mirror of
# difference.kara: each array put in a set, and each list the numbers of
# one set the other lacks.


def find_difference(nums1, nums2):
    first = set(nums1)
    second = set(nums2)
    return [[x for x in first if x not in second], [x for x in second if x not in first]]


seed = 2215


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    pairs = []
    for p in range(200):
        # 1000 numbers each, spread over -30..30, -300..300 and -1000..1000
        spread = [30, 300, 1000][p % 3]
        nums1 = [next_random() % (2 * spread + 1) - spread for _ in range(1000)]
        nums2 = [next_random() % (2 * spread + 1) - spread for _ in range(1000)]
        pairs.append((nums1, nums2))
    check = 0
    for nums1, nums2 in pairs:
        for r in range(10):
            # punch: one number of the first array moves before each answer
            nums1[r * 97] = (nums1[r * 97] + 1001) % 2001 - 1000
            for lst in find_difference(nums1, nums2):
                # the lists come in any order: their lengths and sums do not
                check = (check * 31 + len(lst)) % 1000000007
                check = (check * 31 + sum(lst) + 1000000) % 1000000007
    print(f"200 pairs of 1000, 10 punches: checksum {check}")


main()
