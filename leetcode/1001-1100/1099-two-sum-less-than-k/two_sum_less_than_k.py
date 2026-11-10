# LeetCode #1099: Two Sum Less Than K -- Python mirror of the ★ arm:
# sorting and two pointers. Same cases and output as
# two_sum_less_than_k.kara.


def two_sum_less_than_k(nums, k):
    v = sorted(nums)
    best = -1
    lo, hi = 0, len(v) - 1
    while lo < hi:
        s = v[lo] + v[hi]
        if s < k:
            best = max(best, s)
            lo += 1
        else:
            hi -= 1
    return best


seed = 1099


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        ([34, 23, 1, 24, 75, 33, 54, 8], 60),
        ([10, 20, 30], 15),
        ([5], 100),
        ([1, 1], 3),
        ([1, 1], 2),
        ([7, 7, 7, 7], 15),
        ([1000, 1000], 2000),
        ([999, 1000], 2000),
        ([1, 2, 3, 4, 5], 1),
        ([3, 9, 1, 8, 2], 11),
        ([500, 400, 600, 100], 1001),
    ]
    for nums, k in cases:
        print(two_sum_less_than_k(nums, k))
    found = 0
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 100 + 1
        nums = [next_random() % 1000 + 1 for _ in range(n)]
        k = next_random() % 2000 + 1
        best = two_sum_less_than_k(nums, k)
        if best >= 0:
            found += 1
            total += best
        check = (check * 31 + best + 1) % 1000000007
    print(f"2000 random arrays: {found} with a pair, sums total {total}, checksum {check}")
    nums = [(i * 37 + 11) % 1000 + 1 for i in range(100)]
    s = 0
    for k in range(1, 2001):
        s += two_sum_less_than_k(nums, k)
    print(f"100 values, k from 1 to 2000: answers sum to {s}")


main()
