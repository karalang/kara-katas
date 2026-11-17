# LeetCode #2215: Find the Difference of Two Arrays -- the mirror of
# difference.kara: each array put in a set, and each list the distinct
# numbers of one set the other lacks.


def find_difference(nums1, nums2):
    first = set(nums1)
    second = set(nums2)
    return [[x for x in first if x not in second], [x for x in second if x not in first]]


def sorted_answer(nums1, nums2):
    return [sorted(lst) for lst in find_difference(nums1, nums2)]


seed = 2215


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, spread):
    return [next_random() % (2 * spread + 1) - spread for _ in range(n)]


def show(nums1, nums2):
    print(f"{nums1} and {nums2} -> {sorted_answer(nums1, nums2)}")


def main():
    # LeetCode's two examples, then four more: the same numbers twice,
    # nothing shared, negatives and repeats, and one number each
    show([1, 2, 3], [2, 4, 6])
    show([1, 2, 3, 3], [1, 1, 2, 2])
    show([5, 5, 5], [5])
    show([1, 2], [3, 4])
    show([-1000, 0, 1000, -1000], [1000, -999])
    show([7], [-7])
    # 3000 random pairs of 1 to 30 numbers, spread over -3..3, -30..30
    # and -1000..1000 in turn
    check = 0
    for t in range(3000):
        spread = [3, 30, 1000][t % 3]
        n1 = next_random() % 30 + 1
        n2 = next_random() % 30 + 1
        nums1 = random_nums(n1, spread)
        nums2 = random_nums(n2, spread)
        for lst in sorted_answer(nums1, nums2):
            check = (check * 31 + 1001) % 1000000007
            for x in lst:
                check = (check * 31 + x + 1000) % 1000000007
    print(f"3000 pairs: checksum {check}")
    # the constraints' largest: 1000 numbers each over the whole range,
    # then 1000 each that share nothing
    wide = sorted_answer(random_nums(1000, 1000), random_nums(1000, 1000))
    low = [-1000 + i for i in range(1000)]
    high = [1000 - i for i in range(1000)]
    apart = sorted_answer(low, high)
    print(f"1000 random: {len(wide[0])} and {len(wide[1])}, sums {sum(wide[0])} and {sum(wide[1])}; 1000 apart: {len(apart[0])} and {len(apart[1])}")


main()
