# LeetCode 788 — Rotated Digits, digit by digit.
# Mirrors rotated_digits.kara (the ★ arm) and its harness.


def rotated_digits(n):
    good = 0
    for x in range(1, n + 1):
        rest = x
        valid = True
        changed = False
        while rest > 0:
            d = rest % 10
            if d in (3, 4, 7):
                valid = False
                break
            if d in (2, 5, 6, 9):
                changed = True
            rest //= 10
        if valid and changed:
            good += 1
    return good


seed = 788


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for n in [10, 1, 2, 9, 100, 857, 1000, 2019, 9999, 10000]:
        print(f"n = {n} -> {rotated_digits(n)}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 10000
        good = rotated_digits(n)
        total += good
        check = (check * 31 + good) % 1000000007
    print(f"300 random n: answers sum to {total}, checksum {check}")


main()
