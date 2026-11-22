# LeetCode #2843: Count Symmetric Integers -- the Python mirror of the
# ★ arm: each number written out, kept when it has an even count of
# digits and its halves' digits sum alike.


def symmetric(x):
    digits = str(x)
    n = len(digits)
    if n % 2 == 1:
        return False

    def half(part):
        return sum(ord(d) - 48 for d in part)

    return half(digits[: n // 2]) == half(digits[n // 2 :])


def count_symmetric_integers(low, high):
    return sum(1 for x in range(low, high + 1) if symmetric(x))


# ---- the harness: the same in every arm --------------------------------

seed = 2843


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    c = count_symmetric_integers
    print(f"{c(1, 100)} {c(1200, 1230)}")
    print(f"{c(11, 11)} {c(12, 12)} {c(10000, 10000)} {c(1001, 1001)}")
    print(f"{c(1, 10000)}")
    check = 0
    total = 0
    for i in range(6000):
        a = next_random() % 10000 + 1
        b = next_random() % 10000 + 1 if i < 3000 else min(a + next_random() % 100, 10000)
        got = c(min(a, b), max(a, b))
        total += got
        check = (check * 31 + got) % 1000000007
        if i == 2999 or i == 5999:
            print(f"3000 ranges: {total} in all, checksum {check}")
            total = 0
            check = 0


main()
