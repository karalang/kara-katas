# LeetCode #2831: Find the Longest Equal Subarray -- the Python mirror of
# the ★ arm: the places of each value listed in order, and two pointers
# over each list.


def longest_equal_subarray(nums, k):
    n = len(nums)
    places = [[] for _ in range(n + 1)]
    for i, v in enumerate(nums):
        places[v].append(i)
    best = 0
    for pos in places:
        l = 0
        for r in range(len(pos)):
            while pos[r] - pos[l] - (r - l) > k:
                l += 1
            best = max(best, r - l + 1)
    return best


# ---- the harness: the same in every arm --------------------------------

seed = 2831


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(longest_equal_subarray([1, 3, 2, 3, 1, 3], 3))
    print(longest_equal_subarray([1, 1, 2, 2, 1, 1], 2))
    print(longest_equal_subarray([1], 0))
    print(longest_equal_subarray([1, 2, 2, 3, 3, 3, 2, 2, 2, 2], 0))
    print(longest_equal_subarray([4, 1, 4, 2, 4, 3, 4], 7))
    print(longest_equal_subarray([i % 2 + 1 for i in range(2000)], 999))
    check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        nums = [next_random() % min(n, 3) + 1 for _ in range(n)]
        k = next_random() % (n + 1)
        check = (check * 31 + longest_equal_subarray(nums, k)) % 1000000007
    print(f"3000 short arrays: checksum {check}")
    check = 0
    for _ in range(50):
        n = next_random() % 3000 + 1
        nums = [next_random() % min(n, 20) + 1 for _ in range(n)]
        k = next_random() % 101
        check = (check * 31 + longest_equal_subarray(nums, k)) % 1000000007
    print(f"50 long arrays: checksum {check}")


main()
