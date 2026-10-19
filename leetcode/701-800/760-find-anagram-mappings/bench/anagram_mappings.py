# LeetCode 760 — Find Anagram Mappings: benchmark, the ★ arm.


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


def main():
    rounds = 100000
    fixed = 0
    check = 0
    for _ in range(rounds):
        nums1 = [next_random() % 50 for _ in range(100)]
        nums2 = list(nums1)
        for i in range(100):
            j = i + next_random() % (100 - i)
            nums2[i], nums2[j] = nums2[j], nums2[i]
        mapping = anagram_mappings(nums1, nums2)
        for i in range(100):
            if mapping[i] == i:
                fixed += 1
            check = (check * 31 + mapping[i]) % 1000000007
    print(f"{rounds} pairs of 100 values: {fixed} mapped to their own index, checksum {check}")


main()
