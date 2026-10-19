# LeetCode 760 — Find Anagram Mappings: Python mirror of the ★ arm and its
# harness (same map of positions, same output).


def anagram_mappings(nums1, nums2):
    positions = {}
    for j, x in enumerate(nums2):
        positions.setdefault(x, []).append(j)
    used = {}
    mapping = []
    for x in nums1:
        k = used.get(x, 0)
        mapping.append(positions[x][k])
        used[x] = k + 1
    return mapping


seed = 760


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums1, nums2):
    print(f"{nums1} {nums2} -> {anagram_mappings(nums1, nums2)}")


def main():
    show([12, 28, 46, 32, 50], [50, 12, 32, 46, 28])
    show([84, 46], [84, 46])
    show([7], [7])
    show([1, 1, 1], [1, 1, 1])
    show([2, 1, 2, 1], [1, 2, 1, 2])
    show([0, 100000, 0], [0, 0, 100000])
    show([5, 4, 3, 2, 1], [1, 2, 3, 4, 5])
    fixed = 0
    check = 0
    for _ in range(500):
        n = 1 + next_random() % 100
        widest = 10 if next_random() % 2 == 0 else 100001
        rng = 1 + next_random() % widest
        nums1 = [next_random() * 4 % rng for _ in range(n)]
        nums2 = list(nums1)
        for i in range(n):
            j = i + next_random() % (n - i)
            nums2[i], nums2[j] = nums2[j], nums2[i]
        mapping = anagram_mappings(nums1, nums2)
        for i, p in enumerate(mapping):
            if p == i:
                fixed += 1
            check = (check * 31 + p) % 1000000007
    print(f"500 random pairs: {fixed} values mapped to their own index, checksum {check}")


main()
