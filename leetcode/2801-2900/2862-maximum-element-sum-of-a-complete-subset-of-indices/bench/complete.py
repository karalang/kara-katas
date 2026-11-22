# LeetCode #2862: Maximum Element-Sum of a Complete Subset of Indices --
# the bench: the ★ arm over 200 arrays of 10^4 values up to 10^9,
# LeetCode's most, all drawn first, then each answered 50 times.


def maximum_sum(nums):
    n = len(nums)
    best = 0
    for k in range(1, n + 1):
        s = 0
        j = 1
        while k * j * j <= n:
            s += nums[k * j * j - 1]
            j += 1
        best = max(best, s)
    return best


def main():
    count, rounds, n = 200, 50, 10000
    seed = 2862

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    arrays = [[wide() % 1000000000 + 1 for _ in range(n)] for _ in range(count)]
    total = check = 0
    for r in range(rounds):
        for nums in arrays:
            best = maximum_sum(nums)
            total += best
            check = (check * 31 + best % 1000000007 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: best sums total {total}, checksum {check}")


main()
