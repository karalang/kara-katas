# LeetCode #2843: Count Symmetric Integers -- the bench, mirrored from
# symmetric.kara: each number written out, its halves' digits summed.

seed = 2843


def symmetric(x):
    digits = str(x).encode()
    n = len(digits)
    if n % 2 == 1:
        return False

    def half(part):
        return sum(d - 48 for d in part)

    return half(digits[: n // 2]) == half(digits[n // 2 :])


def count_symmetric_integers(low, high):
    return sum(1 for x in range(low, high + 1) if symmetric(x))


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 5000, 2
    ranges = []
    for _ in range(count):
        a = next_random() % 10000 + 1
        b = next_random() % 10000 + 1
        ranges.append((min(a, b), max(a, b)))
    total = 0
    check = 0
    for r in range(rounds):
        for low, high in ranges:
            got = count_symmetric_integers(low, high)
            total += got
            check = (check * 31 + got + r) % 1000000007
    print(f"{count} ranges, {rounds} rounds: {total} in all, checksum {check}")


main()
