# LeetCode #2860: Happy Students -- the ★ arm's mirror: the values
# sorted, and every group size k from 0 to n with nums[k - 1] < k and
# nums[k] > k counted.


def count_ways(nums):
    s = sorted(nums)
    n = len(s)
    ways = 0
    for k in range(n + 1):
        if (k == 0 or s[k - 1] < k) and (k == n or s[k] > k):
            ways += 1
    return ways


seed = 2860


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def klass(n):
    if next_random() % 2 == 0:
        return [wide() % n for _ in range(n)]
    g = wide() % (n + 1)
    nums = [wide() % max(g, 1) if i < g else g + 1 + wide() % max(n - g, 1) for i in range(n)]
    nums = [min(x, n - 1) for x in nums]
    if next_random() % 4 == 0:
        nums[wide() % n] = min(g, n - 1)
    for i in range(n - 1, 0, -1):
        j = wide() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def main():
    print(f"{count_ways([1, 1])} {count_ways([6, 0, 3, 3, 6, 7, 2, 7])}")
    n = 100000
    print(f"{count_ways([0] * n)} {count_ways([n - 1] * n)} {count_ways(list(range(n)))}")
    total = check = 0
    for c in range(3030):
        n = next_random() % 8 + 1 if c < 3000 else wide() % 90001 + 10000
        ways = count_ways(klass(n))
        total += ways
        check = (check * 31 + ways) % 1000000007
        if c == 2999:
            print(f"3000 small classes: {total} ways, checksum {check}")
            total = check = 0
    print(f"30 large classes: {total} ways, checksum {check}")


main()
