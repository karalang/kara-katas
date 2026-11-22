# LeetCode #2873: Maximum Value of an Ordered Triplet I -- the bench, as
# triplet.kara: 100000 arrays of 100 values, each answered 30 times by
# the one-pass arm.


def maximum_triplet_value(nums):
    best = 0
    top = 0
    gap = 0
    for v in nums:
        best = max(best, gap * v)
        gap = max(gap, top - v)
        top = max(top, v)
    return best


seed = 2873


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 100000, 30, 100
    arrays = [[wide() % 1000000 + 1 for _ in range(n)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            best = maximum_triplet_value(nums)
            total += best
            check = (check * 31 + best % 1000000007 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: values total {total}, checksum {check}")


main()
