# LeetCode #2874: Maximum Value of an Ordered Triplet II -- the bench, as
# triplet.kara: 50 arrays of 10^5 values, each answered 20 times by the
# one-pass arm.


def maximum_triplet_value(nums):
    best = 0
    top = 0
    gap = 0
    for v in nums:
        best = max(best, gap * v)
        gap = max(gap, top - v)
        top = max(top, v)
    return best


seed = 2874


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 50, 20, 100000
    arrays = []
    for c in range(count):
        if c % 2 == 1:
            arrays.append([max(1000000 - i * 9 - wide() % 100000, 1) for i in range(n)])
        else:
            arrays.append([wide() % 1000000 + 1 for _ in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            best = maximum_triplet_value(nums)
            total += best
            check = (check * 31 + best % 1000000007 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: values total {total}, checksum {check}")


main()
