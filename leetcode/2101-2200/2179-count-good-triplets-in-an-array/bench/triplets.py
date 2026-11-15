# LeetCode #2179: Count Good Triplets in an Array -- the benchmark's
# Python mirror of triplets.kara.


def good_triplets(nums1, nums2):
    n = len(nums1)
    place = [0] * n
    for i in range(n):
        place[nums2[i]] = i
    tree = [0] * (n + 1)
    total = 0
    for i in range(n):
        p = place[nums1[i]]
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


seed = 2179


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffled(n):
    perm = list(range(n))
    for i in range(n - 1, 0, -1):
        a = next_random()
        b = next_random()
        j = (a * 32768 + b) % (i + 1)
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def main():
    n = 100000
    first = shuffled(n)
    second = shuffled(n)
    check = 0
    for _ in range(40):
        a = next_random()
        b = next_random()
        offset = (a * 32768 + b) % n
        rotated = [second[(i + offset) % n] for i in range(n)]
        found = good_triplets(first, rotated)
        check = (check * 31 + found % 1000000007) % 1000000007
    print(f"40 solves: checksum {check}")


main()
