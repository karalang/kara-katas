# LeetCode #2809: Minimum Time to Make Array Sum At Most x -- the Python
# mirror of the ★ arm: the pairs sorted by nums2, best[j] the most j
# resets can save, and the least t whose sum is at most x.


def minimum_time(nums1, nums2, x):
    n = len(nums1)
    pairs = sorted(zip(nums2, nums1))
    best = [0] * (n + 1)
    for i, (b, a) in enumerate(pairs):
        for j in range(i + 1, 0, -1):
            best[j] = max(best[j], best[j - 1] + a + j * b)
    sum1 = sum(nums1)
    sum2 = sum(nums2)
    for t in range(n + 1):
        if sum1 + t * sum2 - best[t] <= x:
            return t
    return -1


seed = 2809


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(minimum_time([1, 2, 3], [1, 2, 3], 4))
    print(minimum_time([1, 2, 3], [3, 3, 3], 4))
    print(minimum_time([5, 5], [1, 1], 10))
    n = 1000
    print(minimum_time([1000] * n, [1] * n, 600000))
    print(minimum_time([i + 1 for i in range(n)], [0] * n, 0))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 6 + 1
        nums1 = [next_random() % 11 for _ in range(m)]
        nums2 = [next_random() % 11 for _ in range(m)]
        a = minimum_time(nums1, nums2, next_random() % 41)
        total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"3000 small cases: times sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(30):
        m = next_random() % n + 1
        nums1 = [next_random() % 1001 for _ in range(m)]
        nums2 = [next_random() % 1001 for _ in range(m)]
        x = (next_random() * 32768 + next_random()) % 1000001
        a = minimum_time(nums1, nums2, x)
        total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"30 large cases: times sum to {total}, checksum {check}")


main()
