# LeetCode 788 — Rotated Digits: the bench, in Python.
# Mirrors rotated_digits.kara: every number up to n checked digit by
# digit, for 50,000 random n.


def rotated_digits(n):
    good = 0
    for x in range(1, n + 1):
        rest = x
        valid = True
        changed = False
        while rest > 0:
            d = rest % 10
            if d == 3 or d == 4 or d == 7:
                valid = False
                break
            if d == 2 or d == 5 or d == 6 or d == 9:
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
    rounds = 50000
    total = 0
    check = 0
    for _ in range(rounds):
        n = 1 + next_random() % 10000
        good = rotated_digits(n)
        total += good
        check = (check * 31 + good) % 1000000007
    print(f"{rounds} rounds of n up to 10000: answers sum to {total}, checksum {check}")


main()
