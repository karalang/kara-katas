# LeetCode #2294: Partition Array Such That Maximum Difference Is K --
# the ★ arm's Python mirror. Sort, then a group opens at each number more
# than k above the one that opened the last.


def partition_array(nums, k):
    groups = 0
    low = -1
    for x in sorted(nums):
        if groups == 0 or x - low > k:
            groups += 1
            low = x
    return groups


# ---- test harness ---------------------------------------------------------

seed = 2294


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        ([3, 6, 1, 2, 5], 2),
        ([1, 2, 3], 1),
        ([2, 2, 4, 5], 0),
        ([7], 3),
        ([5, 5, 5, 6, 6, 0], 0),
        ([100000, 0, 50000], 100000),
        ([0, 4, 8, 12, 16], 4),
    ]
    for nums, k in cases:
        print(f"{len(nums)} numbers, k {k}: {partition_array(nums, k)}")
    check = 0
    total = 0
    for _ in range(3000):
        n = next_random() % 60 + 1
        top = next_random() % 200 + 1
        k = next_random() % 31
        nums = [next_random() % (top + 1) for _ in range(n)]
        groups = partition_array(nums, k)
        check = (check * 31 + groups) % 1000000007
        total += groups
    print(f"3000 arrays: checksum {check}, {total} groups")


main()
