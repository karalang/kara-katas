# LeetCode #1780: Check if Number is a Sum of Powers of Three -- the ★ arm in
# Python: no digit of n in base 3 may be a 2.


def check_powers_of_three(n):
    rest = n
    while rest > 0:
        if rest % 3 == 2:
            return False
        rest //= 3
    return True


seed = 1780


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_number():
    bits = next_random() % 32768
    n, power = 0, 1
    for k in range(15):
        if (bits >> k) & 1 == 1:
            n += power
        power *= 3
    if next_random() % 2 == 0:
        n += next_random() % 4
    return max(n, 1)


def show(b):
    return "true" if b else "false"


def main():
    f = check_powers_of_three
    print(f"{show(f(12))} {show(f(91))} {show(f(21))}")
    print(f"{show(f(1))} {show(f(2))} {show(f(2187))} {show(f(28))} {show(f(1093))}")
    print(f"the most: {show(f(10000000))} {show(f(7174453))} {show(f(7174454))}")
    check = 0
    for _ in range(3000):
        n = random_number()
        check = (check * 31 + (2 if f(n) else 1)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
