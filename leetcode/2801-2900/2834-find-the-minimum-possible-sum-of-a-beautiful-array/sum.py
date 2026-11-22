# LeetCode #2834: Find the Minimum Possible Sum of a Beautiful Array --
# the Python mirror of the ★ arm: 1 to min(n, target / 2), then the rest
# from target up, two arithmetic series.

MOD = 1000000007


def minimum_possible_sum(n, target):
    low = min(n, target // 2)
    high = n - low
    first = low * (low + 1) // 2
    rest = high * (2 * target + high - 1) // 2
    return (first + rest) % MOD


# ---- the harness: the same in every arm --------------------------------

seed = 2834


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    s = minimum_possible_sum
    print(f"{s(2, 3)} {s(3, 3)} {s(1, 1)}")
    print(f"{s(5, 2)} {s(4, 100)}")
    print(f"{s(1000000000, 1000000000)} {s(1000000000, 1)}")
    print(f"{s(1, 1000000000)} {s(999999999, 1000000000)}")
    check = 0
    for n in range(1, 61):
        for target in range(1, 61):
            check = (check * 31 + s(n, target)) % 1000000007
    print(f"3600 small pairs: checksum {check}")
    check = 0
    for _ in range(20000):
        n = wide() % 1000000000 + 1
        target = wide() % 1000000000 + 1
        check = (check * 31 + s(n, target)) % 1000000007
    print(f"20000 random pairs: checksum {check}")


main()
