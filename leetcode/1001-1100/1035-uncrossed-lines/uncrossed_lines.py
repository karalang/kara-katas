# LeetCode #1035: Uncrossed Lines -- Python mirror of uncrossed_lines.kara


def max_uncrossed_lines(nums1, nums2):
    m = len(nums1)
    n = len(nums2)
    best = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i - 1] == nums2[j - 1]:
                best[i][j] = best[i - 1][j - 1] + 1
            else:
                best[i][j] = max(best[i - 1][j], best[i][j - 1])
    return best[m][n]


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_list(length, top, seed):
    return [next_random(seed) % top + 1 for _ in range(length)]


def show(nums):
    return "[" + ",".join(str(v) for v in nums) + "]"


def main():
    examples = [
        ([1, 4, 2], [1, 2, 4]),
        ([2, 5, 1, 2, 5], [10, 5, 2, 1, 5, 2]),
        ([1, 3, 7, 1, 7, 5], [1, 9, 2, 5, 1]),
        ([1], [1]),
        ([1], [2]),
        ([3, 3, 3], [3, 3]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([1, 2, 1, 2, 1, 2], [2, 1, 2, 1, 2, 1]),
    ]
    for nums1, nums2 in examples:
        print(f"{show(nums1)}, {show(nums2)} -> {max_uncrossed_lines(nums1, nums2)}")
    seed = [1035]
    for count, longest, top in [(300, 8, 3), (200, 30, 2), (200, 30, 10), (40, 200, 5), (40, 200, 2000), (6, 500, 4), (6, 500, 2000)]:
        total = 0
        check = 0
        for _ in range(count):
            len1 = next_random(seed) % longest + 1
            len2 = next_random(seed) % longest + 1
            nums1 = random_list(len1, top, seed)
            nums2 = random_list(len2, top, seed)
            lines = max_uncrossed_lines(nums1, nums2)
            total += lines
            check = (check * 131 + lines) % 1000000007
        print(f"{count} pairs of up to {longest} values from 1 to {top}: sum {total}, checksum {check}")
    up = [i % 2000 + 1 for i in range(500)]
    down = [500 - i for i in range(500)]
    same = [7] * 500
    wide = random_list(500, 2000, seed)
    for name, nums1, nums2 in [("1 to 500 against itself", up, up), ("1 to 500 against 500 to 1", up, down), ("500 sevens against 500 sevens", same, same), ("random against itself", wide, wide)]:
        print(f"{name}: {max_uncrossed_lines(nums1, nums2)}")


main()
