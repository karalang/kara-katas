# LeetCode #2179: Count Good Triplets in an Array -- the Python mirror
# of triplets.kara: each value's place in nums2 read in nums1's order,
# and each middle's smaller places before it and larger after it counted
# by a Fenwick tree.


def good_triplets(nums1, nums2):
    n = len(nums1)
    where = [0] * n
    for i in range(n):
        where[nums2[i]] = i
    tree = [0] * (n + 1)
    total = 0
    for i in range(n):
        p = where[nums1[i]]
        smaller = 0
        j = p
        while j > 0:
            smaller += tree[j]
            j -= j & -j
        larger = (n - 1 - p) - (i - smaller)
        total += smaller * larger
        j = p + 1
        while j <= n:
            tree[j] += 1
            j += j & -j
    return total


# ---- test harness ---------------------------------------------------------

seed = 2179


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffled(n):
    perm = list(range(n))
    for i in range(n - 1, 0, -1):
        j = (next_random() * 32768 + next_random()) % (i + 1)
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def show(nums1, nums2):
    print(f"[{', '.join(map(str, nums1))}], [{', '.join(map(str, nums2))}] -> {good_triplets(nums1, nums2)}")


def main():
    show([2, 0, 1, 3], [0, 1, 2, 3])
    show([4, 0, 1, 3, 2], [4, 1, 0, 2, 3])
    show([0, 1, 2], [0, 1, 2])
    show([0, 1, 2], [2, 1, 0])
    show([3, 1, 4, 0, 2], [3, 1, 4, 0, 2])
    show([1, 0, 3, 2, 5, 4], [0, 1, 2, 3, 4, 5])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % [8, 30][rnd % 2] + 3
        nums1 = shuffled(n)
        nums2 = shuffled(n)
        found = good_triplets(nums1, nums2)
        total += found
        check = (check * 31 + found % 1000000007 + n) % 1000000007
    print(f"2000 pairs: {total} in all, checksum {check}")
    n = 100000
    same = list(range(n))
    back = list(range(n - 1, -1, -1))
    print(f"{n} values: {good_triplets(same, same)} {good_triplets(same, back)} {good_triplets(shuffled(n), shuffled(n))}")


main()
