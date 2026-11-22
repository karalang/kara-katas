# LeetCode #2809: Minimum Time to Make Array Sum At Most x -- the bench in
# Python: the ★ arm over 20 cases of 1000 pairs, nums1 up to 1000 and
# nums2 up to 2, x from 3 * 10^5 to 5 * 10^5, all drawn first, then each
# answered 20 times.


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
    count = 20
    rounds = 20
    cases = []
    for _ in range(count):
        nums1 = [next_random() % 1001 for _ in range(1000)]
        nums2 = [next_random() % 3 for _ in range(1000)]
        cases.append((nums1, nums2, 300000 + (next_random() * 32768 + next_random()) % 200000))
    total = 0
    check = 0
    for r in range(rounds):
        for nums1, nums2, x in cases:
            a = minimum_time(nums1, nums2, x)
            total += a
            check = (check * 31 + a + 1 + r) % 1000000007
    print(f"{count} cases of 1000 pairs, {rounds} rounds: times sum to {total}, checksum {check}")


main()
