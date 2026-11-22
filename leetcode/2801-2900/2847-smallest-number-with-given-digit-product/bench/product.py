# LeetCode #2847: Smallest Number With Given Digit Product -- the bench,
# mirrored from product.kara: the largest digit that divides what is
# left, 9 down to 2, and the digits smallest first.

seed = 2847


def smallest_number(n):
    if n == 1:
        return "1"
    rest = n
    digits = []
    for d in range(9, 1, -1):
        while rest % d == 0:
            digits.append(str(d))
            rest //= d
    if rest != 1:
        return "-1"
    return "".join(reversed(digits))


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 100000, 20
    numbers = []
    for _ in range(count):
        n = 1
        for _ in range(next_random() % 41):
            p = [2, 3, 5, 7][next_random() % 4]
            if n <= 10**18 // p:
                n *= p
        if next_random() % 10 == 0 and n <= 10**18 // 11:
            n *= 11
        numbers.append(n)
    digits = 0
    check = 0
    for r in range(rounds):
        for n in numbers:
            s = smallest_number(n)
            digits += len(s)
            for b in s.encode():
                check = (check * 31 + b + r) % 1000000007
    print(f"{count} numbers, {rounds} rounds: {digits} digits, checksum {check}")


main()
