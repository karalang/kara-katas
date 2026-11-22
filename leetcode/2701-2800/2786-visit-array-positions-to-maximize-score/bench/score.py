# LeetCode #2786: Visit Array Positions to Maximize Score -- the bench in
# Python: the ★ arm over 20 arrays of 10^5 numbers up to 10^6 with x up
# to 10^6, all drawn first, then each answered 100 times.


def max_score(nums, x):
    unreached = -1000000000000000
    best = [unreached, unreached]
    best[nums[0] % 2] = nums[0]
    for v in nums[1:]:
        p = v % 2
        best[p] = max(best[p], best[1 - p] - x) + v
    return max(best[0], best[1])


seed = 2786


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count = 20
    rounds = 100
    cases = []
    for _ in range(count):
        nums = [wide() % 1000000 + 1 for _ in range(100000)]
        cases.append((nums, wide() % 1000000 + 1))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, x in cases:
            a = max_score(nums, x)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of 10^5, {rounds} rounds: scores sum to {total}, checksum {check}")


main()
