# LeetCode #1035: Uncrossed Lines -- bench
# Mirrors ./uncrossed_lines.kara; see ../README.md § Benchmarks.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count, rounds = 40, 20
    seed = [1035]
    pairs = []
    for _ in range(count):
        nums1 = [next_random(seed) % 10 + 1 for _ in range(500)]
        nums2 = [next_random(seed) % 10 + 1 for _ in range(500)]
        pairs.append((nums1, nums2))
    total = 0
    check = 0
    for _ in range(rounds):
        for nums1, nums2 in pairs:
            lines = max_uncrossed_lines(nums1, nums2)
            total += lines
            check = (check * 131 + lines) % 1000000007
    print(f"{count} pairs of 500 values, {rounds} rounds: sum {total}, checksum {check}")


main()
