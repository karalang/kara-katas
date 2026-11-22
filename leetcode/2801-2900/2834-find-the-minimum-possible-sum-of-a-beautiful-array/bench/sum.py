# LeetCode #2834: Find the Minimum Possible Sum of a Beautiful Array --
# the bench, mirrored from sum.kara: two arithmetic series.

MOD = 1000000007


def minimum_possible_sum(n, target):
    low = min(n, target // 2)
    high = n - low
    first = low * (low + 1) // 2
    rest = high * (2 * target + high - 1) // 2
    return (first + rest) % MOD


seed = 2834


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    count, rounds = 1000000, 20
    pairs = []
    for _ in range(count):
        n = wide() % 1000000000 + 1
        pairs.append((n, wide() % 1000000000 + 1))
    check = 0
    for r in range(rounds):
        for n, target in pairs:
            check = (check * 31 + minimum_possible_sum(n, target) + r) % MOD
    print(f"{count} pairs, {rounds} rounds: checksum {check}")


main()
