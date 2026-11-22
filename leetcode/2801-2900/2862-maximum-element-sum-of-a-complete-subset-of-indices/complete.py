# LeetCode #2862: Maximum Element-Sum of a Complete Subset of Indices --
# the ★ arm's mirror: for each square-free part k, the values at
# k·1², k·2², ... summed, and the best kept.


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


seed = 2862


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(f"{maximum_sum([8, 7, 3, 5, 7, 2, 4, 9])} {maximum_sum([8, 10, 3, 8, 1, 13, 7, 9, 4])}")
    n = 10000
    print(f"{maximum_sum([1000000000] * n)} {maximum_sum(list(range(1, n + 1)))}")
    total = check = 0
    for c in range(3030):
        small = c < 3000
        n = next_random() % 30 + 1 if small else wide() % 9001 + 1000
        top = 20 if small else 1000000000
        nums = [wide() % top + 1 for _ in range(n)]
        best = maximum_sum(nums)
        total += best
        check = (check * 31 + best) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: best sums total {total}, checksum {check}")
            total = check = 0
    print(f"30 long arrays: best sums total {total}, checksum {check}")


main()
