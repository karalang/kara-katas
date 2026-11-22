# LeetCode #2771: Longest Non-decreasing Subarray From Two Arrays -- the
# bench in Python: the ★ arm over 20 pairs of 10^5 numbers, all drawn
# first, then each answered 10 times.


def max_non_decreasing_length(nums1, nums2):
    n = len(nums1)
    one, two = 1, 1
    best = 1
    for i in range(1, n):
        next_one = 1
        next_two = 1
        if nums1[i - 1] <= nums1[i]:
            next_one = max(next_one, one + 1)
        if nums2[i - 1] <= nums1[i]:
            next_one = max(next_one, two + 1)
        if nums1[i - 1] <= nums2[i]:
            next_two = max(next_two, one + 1)
        if nums2[i - 1] <= nums2[i]:
            next_two = max(next_two, two + 1)
        one = next_one
        two = next_two
        best = max(best, one, two)
    return best


seed = 2771


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count = 20
    rounds = 10
    n = 100000
    pairs = []
    for _ in range(count):
        noise = next_random() % 200 + 1
        nums1 = [i * 10 + next_random() % noise + 1 for i in range(n)]
        nums2 = [wide() % 1000000000 + 1 for _ in range(n)]
        pairs.append((nums1, nums2))
    total = 0
    check = 0
    for r in range(rounds):
        for nums1, nums2 in pairs:
            a = max_non_decreasing_length(nums1, nums2)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} pairs of 10^5, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()
