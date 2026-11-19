# LeetCode #2333: Minimum Sum of Squared Difference -- the bench, the ★
# arm in Python: the gaps counted by size, the largest dropped a level at
# a time while the moves cover them, and the moves left taking that many
# of the rest one lower.


def min_sum_square_diff(nums1, nums2, k1, k2):
    count = [0] * 100001
    top = 0
    for i in range(len(nums1)):
        gap = abs(nums1[i] - nums2[i])
        count[gap] += 1
        if gap > top:
            top = gap
    moves = k1 + k2
    level = top
    while level > 0 and moves >= count[level]:
        moves -= count[level]
        count[level - 1] += count[level]
        count[level] = 0
        level -= 1
    if level > 0:
        count[level] -= moves
        count[level - 1] += moves
    total = 0
    for gap in range(1, level + 1):
        total += count[gap] * gap * gap
    return total


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    cases = []
    for c in range(10):
        nums1 = [scrambled(c * 40000 + i) % 100001 for i in range(20000)]
        nums2 = [scrambled(c * 40000 + 20000 + i) % 100001 for i in range(20000)]
        cases.append((nums1, nums2))
    check = 0
    for p in range(10):
        for c in range(10):
            nums1, nums2 = cases[c]
            k1 = (10 * c + p) * 3000000 % 400000000
            k2 = (7 * p + c) * 5000000 % 300000000
            check = (check * 31 + min_sum_square_diff(nums1, nums2, k1, k2)) % 1000000007
    print(f"10 passes over 10 cases of 2*10^4 pairs: checksum {check}")


main()
