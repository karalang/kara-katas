# LeetCode #2771: Longest Non-decreasing Subarray From Two Arrays -- the
# ★ arm in Python (nondecreasing.kara): two running lengths, the longest
# non-decreasing run ending at i that takes nums1[i] and the one that
# takes nums2[i].


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
    print(max_non_decreasing_length([2, 3, 1], [1, 2, 1]))
    print(max_non_decreasing_length([1, 3, 2, 1], [2, 2, 3, 4]))
    print(max_non_decreasing_length([1, 1], [2, 2]))
    n = 100000
    rising = list(range(1, n + 1))
    falling = rising[::-1]
    print(max_non_decreasing_length(falling, rising))
    print(max_non_decreasing_length(falling, falling))
    evens = [i if i % 2 == 0 else 0 for i in range(1, n + 1)]
    odds = [i if i % 2 == 1 else 0 for i in range(1, n + 1)]
    print(max_non_decreasing_length(evens, odds))
    total = 0
    check = 0
    for _ in range(3000):
        k = next_random() % 12 + 1
        nums1 = [next_random() % 5 + 1 for _ in range(k)]
        nums2 = [next_random() % 5 + 1 for _ in range(k)]
        a = max_non_decreasing_length(nums1, nums2)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small pairs: lengths sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(10):
        noise = next_random() % 200 + 1
        nums1 = [i * 10 + next_random() % noise + 1 for i in range(n)]
        nums2 = [wide() % 1000000000 + 1 for _ in range(n)]
        a = max_non_decreasing_length(nums1, nums2)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"10 pairs of 10^5: lengths sum to {total}, checksum {check}")


main()
