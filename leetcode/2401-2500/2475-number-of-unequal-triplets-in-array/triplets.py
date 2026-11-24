# LeetCode #2475: Number of Unequal Triplets in Array -- the Python
# mirror of triplets.kara: a dict counts the values, and each value of
# count `c` is the middle of `left * c * right` triplets.


def unequal_triplets(nums):
    counts = {}
    for v in nums:
        counts[v] = counts.get(v, 0) + 1
    n = len(nums)
    left = 0
    total = 0
    for c in counts.values():
        total += left * c * (n - left - c)
        left += c
    return total


# ---- test harness ---------------------------------------------------------

seed = 2475


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, top):
    return [1 + next_random() % top for _ in range(n)]


def main():
    cases = [
        [4, 4, 2, 4, 3],
        [1, 1, 1, 1, 1],
        [1, 2, 3],
        [5, 7, 5, 7, 7, 5],
        [9, 1, 9, 2, 9, 3],
        [1000, 1, 1000, 1000, 2],
    ]
    for nums in cases:
        shown = "[" + ", ".join(str(v) for v in nums) + "]"
        print(f"{shown} -> {unequal_triplets(nums)}")
    distinct = [1000 - 7 * i for i in range(100)]
    print(f"100 distinct -> {unequal_triplets(distinct)}")
    print(f"100 of 1 to 1000 -> {unequal_triplets(random_nums(100, 1000))}")
    print(f"100 of 1 to 10 -> {unequal_triplets(random_nums(100, 10))}")
    print(f"100 of 1 to 3 -> {unequal_triplets(random_nums(100, 3))}")
    check = 0
    for _ in range(3000):
        n = 3 + next_random() % 98
        top = 1 + next_random() % 20
        check = (check * 31 + unequal_triplets(random_nums(n, top))) % 1000000007
    print(f"3000 random: checksum {check}")


main()
