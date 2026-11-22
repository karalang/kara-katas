# LeetCode #2779: Maximum Beauty of an Array After Applying Operation --
# the ★ arm in Python (beauty.kara): the numbers sorted and the widest
# window with its greatest at most 2k above its least.


def maximum_beauty(nums, k):
    s = sorted(nums)
    best = 0
    lo = 0
    for hi in range(len(s)):
        while s[hi] - s[lo] > 2 * k:
            lo += 1
        best = max(best, hi - lo + 1)
    return best


seed = 2779


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(maximum_beauty([4, 6, 1, 2], 2))
    print(maximum_beauty([1, 1, 1, 1], 10))
    n = 100000
    print(maximum_beauty([0] * n, 0))
    rising = list(range(n))
    print(maximum_beauty(rising, 0))
    print(maximum_beauty(rising, 100000))
    print(maximum_beauty([3 * i for i in range(n // 3)], 1))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 12 + 1
        nums = [next_random() % 21 for _ in range(m)]
        k = next_random() % 6
        b = maximum_beauty(nums, k)
        total += b
        check = (check * 31 + b) % 1000000007
    print(f"3000 small arrays: beauties sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20):
        nums = [wide() % 100001 for _ in range(n)]
        k = wide() % 1001
        b = maximum_beauty(nums, k)
        total += b
        check = (check * 31 + b) % 1000000007
    print(f"20 arrays of 10^5: beauties sum to {total}, checksum {check}")


main()
