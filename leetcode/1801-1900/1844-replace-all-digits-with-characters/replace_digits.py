# LeetCode #1844: Replace All Digits with Characters -- the ★ arm in Python


def replace_digits(s):
    out = []
    for i in range(len(s)):
        if i % 2 == 0:
            out.append(s[i])
        else:
            out.append(chr(ord(s[i - 1]) + ord(s[i]) - ord("0")))
    return "".join(out)


seed = 1844


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def case(n):
    out = []
    letter = 0
    for i in range(n):
        if i % 2 == 0:
            letter = next_random() % 26
            out.append(chr(ord("a") + letter))
        else:
            most = min(25 - letter, 9)
            out.append(chr(ord("0") + next_random() % (most + 1)))
    return "".join(out)


def main():
    f = replace_digits
    print(f"{f('a1c1e1')} {f('a1b2c3d4e')}")
    print(f"{f('q')} {f('m0')} {f('q9')} {f('a9')} {f('z0y1x2w')}")
    drawn = case(100)
    print(f"the most: {f(drawn)} {f('a9' * 50)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        out = f(case(n))
        for b in out.encode():
            check = (check * 31 + b) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
