# LeetCode #2407: Longest Increasing Subsequence II -- the bench, the ★
# arm in Python: a bottom-up segment tree over the values, the longest
# ending at x one more than the tree's maximum over x - k to x - 1.

seed = 2407


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def length_of_lis(nums, k):
    top = max(nums)
    size = 1
    while size <= top:
        size *= 2
    tree = [0] * (2 * size)
    best = 0
    for x in nums:
        lo = max(x - k, 0) + size
        hi = x - 1 + size + 1
        longest = 0
        while lo < hi:
            if lo % 2 == 1:
                longest = max(longest, tree[lo])
                lo += 1
            if hi % 2 == 1:
                hi -= 1
                longest = max(longest, tree[hi])
            lo //= 2
            hi //= 2
        at = x + size
        tree[at] = max(tree[at], longest + 1)
        best = max(best, longest + 1)
        at //= 2
        while at > 0:
            tree[at] = max(tree[2 * at], tree[2 * at + 1])
            at //= 2
    return best


def main():
    arrays = [[1 + (next_random() * 32768 + next_random()) % 100000 for _ in range(100000)] for _ in range(5)]
    check = 0
    for p in range(4):
        k = 1
        for nums in arrays:
            check = (check * 31 + length_of_lis(nums, k) + p) % 1000000007
            k *= 10
    print(f"4 passes over 5 arrays of 10^5 values: checksum {check}")


main()
