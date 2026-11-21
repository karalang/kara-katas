# LeetCode #2499: Minimum Total Cost to Make Arrays Unequal -- benchmark
# mirror of the ★ arm (unequal.kara): 20 pairs of arrays of 10^5 values
# to 4, built once, then the passes; each sets one place of every nums2
# from the checksum so far, asks, and puts it back.


def minimum_total_cost(nums1, nums2):
    n = len(nums1)
    count = [0] * (n + 1)
    equal = 0
    cost = 0
    for i in range(n):
        if nums1[i] == nums2[i]:
            count[nums1[i]] += 1
            equal += 1
            cost += i
    mode = 0
    for v in range(1, n + 1):
        if count[v] > count[mode]:
            mode = v
    short = 2 * count[mode] - equal
    for j in range(n):
        if short <= 0:
            break
        if nums1[j] != nums2[j] and nums1[j] != mode and nums2[j] != mode:
            cost += j
            short -= 1
    return -1 if short > 0 else cost


seed = 2499


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    passes = 33
    pairs = []
    for _ in range(20):
        nums1 = []
        nums2 = []
        for _ in range(n):
            a = next_random() % 4 + 1
            nums1.append(a)
            nums2.append(a if next_random() % 2 == 0 else next_random() % 4 + 1)
        pairs.append((nums1, nums2))
    check = 0
    for p in range(passes):
        for nums1, nums2 in pairs:
            at = check % n
            was = nums2[at]
            nums2[at] = nums1[at] if (check // n + p) % 2 == 0 else check % 4 + 1
            check = (check * 31 + minimum_total_cost(nums1, nums2) + 1 + p) % 1000000007
            nums2[at] = was
    print(f"{passes} passes over 20 pairs of 10^5: checksum {check}")


main()
