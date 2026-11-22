# LeetCode #2874: Maximum Value of an Ordered Triplet II -- the Python
# mirror of the ★ arm (triplet.kara): one pass carrying the largest value
# so far and the largest gap so far.


def maximum_triplet_value(nums):
    best = 0
    top = 0
    gap = 0
    for v in nums:
        best = max(best, gap * v)
        gap = max(gap, top - v)
        top = max(top, v)
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def main():
    global seed
    print(f"{maximum_triplet_value([12, 6, 1, 2, 7])} {maximum_triplet_value([1, 10, 3, 4, 19])} {maximum_triplet_value([1, 2, 3])}")
    n = 100000
    print(f"{maximum_triplet_value(list(range(1, n + 1)))} {maximum_triplet_value(list(range(n, 0, -1)))} {maximum_triplet_value([1 if i == n // 2 else 1000000 for i in range(n)])}")
    seed = 2874
    total = 0
    check = 0
    for c in range(3100):
        small = c < 3000
        n = next_random() % 6 + 3 if small else wide() % 99001 + 1000
        if small:
            nums = [next_random() % 9 + 1 for _ in range(n)]
        elif c % 2 == 1:
            nums = [max(1000000 - i * 9 - wide() % 100000, 1) for i in range(n)]
        else:
            nums = [wide() % 1000000 + 1 for _ in range(n)]
        best = maximum_triplet_value(nums)
        total += best
        check = (check * 31 + best % 1000000007) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: values total {total}, checksum {check}")
            total = 0
            check = 0
    print(f"100 long arrays: values total {total}, checksum {check}")


main()
