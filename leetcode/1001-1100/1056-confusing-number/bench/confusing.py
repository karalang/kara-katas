# LeetCode #1056: Confusing Number -- the benchmark, mirror of confusing.kara.


def confusing_number(n):
    turned = [0, 1, -1, -1, -1, -1, 9, -1, 8, 6]
    rest = n
    upside = 0
    while rest > 0:
        d = turned[rest % 10]
        if d < 0:
            return False
        upside = upside * 10 + d
        rest //= 10
    return upside != n


def main():
    count = 500000
    rounds = 20
    turning = [0, 1, 6, 8, 9]
    other = [2, 3, 4, 5, 7]
    seed = 1056

    def rnd():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    numbers = []
    for _ in range(count):
        digits = 6 + rnd() % 5
        spoiled = rnd() % digits if rnd() % 8 == 0 else -1
        n = turning[1 + rnd() % 4]
        for k in range(1, digits):
            d = other[rnd() % 5] if k == spoiled else turning[rnd() % 5]
            n = n * 10 + d
        numbers.append(n)
    total = 0
    check = 0
    for _ in range(rounds):
        found = 0
        for n in numbers:
            if confusing_number(n):
                found += 1
                check = (check + n % 1000) % 1000000007
        total += found
        check = (check * 131 + found) % 1000000007
    print(f"{count} numbers, {rounds} rounds: {total} confusing, checksum {check}")


main()
