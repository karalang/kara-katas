# LeetCode #728: Self Dividing Numbers -- each digit, by remainders.
# Mirror of the Kara star arm and its harness.


def self_dividing(n):
    rest = n
    while rest > 0:
        d = rest % 10
        if d == 0 or n % d != 0:
            return False
        rest //= 10
    return True


def self_dividing_numbers(left, right):
    return [n for n in range(left, right + 1) if self_dividing(n)]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(left, right):
    print(f"{left}..{right} -> {self_dividing_numbers(left, right)}")


def main():
    show(1, 22)
    show(47, 85)
    show(1, 1)
    show(10, 10)
    show(100, 130)
    show(9990, 10000)
    show(1111, 1150)
    all_ = self_dividing_numbers(1, 10000)
    print(f"1..10000 -> {len(all_)} numbers, sum {sum(all_)}, largest {all_[-1]}")
    seed = [728]
    found = 0
    check = 0
    for _ in range(300):
        a = 1 + next_random(seed) % 10000
        b = 1 + next_random(seed) % 10000
        left, right = min(a, b), max(a, b)
        got = self_dividing_numbers(left, right)
        found += len(got)
        for n in got:
            check = (check * 131 + n) % 1000000007
        check = (check * 131 + 1) % 1000000007
    print(f"300 random ranges: {found} numbers, checksum {check}")


main()
