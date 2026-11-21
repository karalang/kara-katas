# LeetCode #2407: Longest Increasing Subsequence II -- the mirror of the ★
# arm: a bottom-up segment tree over the values, the longest ending at x
# one more than the tree's maximum over x - k to x - 1.

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


def values(n, top):
    return [1 + (next_random() * 32768 + next_random()) % top for _ in range(n)]


def main():
    print(length_of_lis([4, 2, 1, 4, 3, 4, 5, 8, 15], 3))
    print(length_of_lis([7, 4, 5, 1, 8, 12, 4, 7], 5))
    print(length_of_lis([1, 5], 1))
    print(length_of_lis([100000], 100000))
    odd = [1 + 2 * i for i in range(50)]
    print(f"{length_of_lis(odd, 1)} {length_of_lis(odd, 2)}")
    big = values(20000, 100000)
    print(f"{length_of_lis(big, 1)} {length_of_lis(big, 100)} {length_of_lis(big, 100000)}")
    gentle = [1 + i * 4 + next_random() % 9 for i in range(20000)]
    print(f"{length_of_lis(gentle, 3)} {length_of_lis(gentle, 8)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 50
        k = 1 + next_random() % 10
        a = length_of_lis(values(n, top), k)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
