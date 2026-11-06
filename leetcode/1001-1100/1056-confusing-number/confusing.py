# LeetCode #1056: Confusing Number -- mirror of confusing.kara.


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


def b(x):
    return "true" if x else "false"


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_turnable(rng):
    digits = [0, 1, 6, 8, 9]
    n = 0
    for _ in range(rng.next() % 9 + 1):
        n = n * 10 + digits[rng.next() % 5]
    return n


def main():
    for n in [6, 89, 11, 25, 0, 10, 916, 69, 8000, 100]:
        print(f"{n} -> {b(confusing_number(n))}")
    count = total = check = 0
    for n in range(100001):
        answer = confusing_number(n)
        if answer:
            count += 1
            total += n
        check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"0 to 100000: {count} confusing, total {total}, checksum {check}")
    rng = Rng(1056)
    count = total = check = 0
    for _ in range(3000):
        n = random_turnable(rng)
        answer = confusing_number(n)
        if answer:
            count += 1
            total = (total + n) % 1000000007
        check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"3000 random numbers of 0, 1, 6, 8 and 9: {count} confusing, total {total}, checksum {check}")
    for n in [1000000000, 999999999, 968999896, 916000001, 986101986, 818181818, 123456789]:
        print(f"{n} -> {b(confusing_number(n))}")


main()
