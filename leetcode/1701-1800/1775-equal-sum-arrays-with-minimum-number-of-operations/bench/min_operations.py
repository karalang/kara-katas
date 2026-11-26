# LeetCode #1775: Equal Sum Arrays With Minimum Number of Operations -- the
# bench in Python, mirroring min_operations.kara: the gains counted by size
# and the largest taken first.


def min_operations(nums1, nums2):
    sum1, sum2 = sum(nums1), sum(nums2)
    if sum1 == sum2:
        return 0
    low, high = (nums1, nums2) if sum1 < sum2 else (nums2, nums1)
    gap = abs(sum1 - sum2)
    gains = [0] * 6
    for x in low:
        gains[6 - x] += 1
    for x in high:
        gains[x - 1] += 1
    ops = 0
    for g in range(5, 0, -1):
        while gains[g] > 0 and gap > 0:
            gap -= g
            gains[g] -= 1
            ops += 1
    return -1 if gap > 0 else ops


seed = 1775


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(40):
        low = 1 + next_random() % 3
        high = 4 + next_random() % 3
        lists.append([low + next_random() % (high - low + 1) for _ in range(100000)])
    check = 0
    for call in range(400):
        a = (check + call) % 40
        b = (check // 40 + call * 7) % 40
        check = (check * 31 + min_operations(lists[a], lists[b]) + 1) % 1000000007
    print(f"400 calls over 40 lists: checksum {check}")


main()
