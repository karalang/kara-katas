# LeetCode #2860: Happy Students -- the bench: the ★ arm over 50
# classes of 10^5 students, LeetCode's most, half of them random and
# half built around a group size, all drawn first, then each answered 20
# times, the sort included.


def count_ways(nums):
    s = sorted(nums)
    n = len(s)
    ways = 0
    for k in range(n + 1):
        if (k == 0 or s[k - 1] < k) and (k == n or s[k] > k):
            ways += 1
    return ways


def main():
    count, rounds, n = 50, 20, 100000
    seed = 2860

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    def klass(n):
        if nr() % 2 == 0:
            return [wide() % n for _ in range(n)]
        g = wide() % (n + 1)
        nums = [min(wide() % max(g, 1) if i < g else g + 1 + wide() % max(n - g, 1), n - 1) for i in range(n)]
        if nr() % 4 == 0:
            nums[wide() % n] = min(g, n - 1)
        for i in range(n - 1, 0, -1):
            j = wide() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        return nums

    classes = [klass(n) for _ in range(count)]
    total = check = 0
    for r in range(rounds):
        for nums in classes:
            ways = count_ways(nums)
            total += ways
            check = (check * 31 + ways + r) % 1000000007
    print(f"{count} classes of {n}, {rounds} rounds: {total} ways, checksum {check}")


main()
