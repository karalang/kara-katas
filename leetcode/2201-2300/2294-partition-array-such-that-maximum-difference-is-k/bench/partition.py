# LeetCode #2294: Partition Array Such That Maximum Difference Is K --
# the bench, the ★ arm's Python mirror. Sort a copy, then open a group at
# each number more than k above the one that opened the last.


def partition_array(nums, k):
    groups = 0
    low = -1
    for x in sorted(nums):
        if groups == 0 or x - low > k:
            groups += 1
            low = x
    return groups


# ---- bench harness ---------------------------------------------------------

seed = 2294


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(20):
        nums = []
        for _ in range(100000):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % 100001)
        arrays.append(nums)
    check = 0
    for p in range(5):
        for a in range(20):
            check = (check * 31 + partition_array(arrays[a], 7 * a + p)) % 1000000007
    print(f"5 passes over 20 arrays of 10^5: checksum {check}")


main()
