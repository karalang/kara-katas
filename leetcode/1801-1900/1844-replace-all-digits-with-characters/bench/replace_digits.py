# LeetCode #1844: Replace All Digits with Characters -- the bench in Python: the ★ arm over
# 500000 calls on 40 strings of 100 places, built once, each call's string
# drawn from the checksum so far and one byte of its output, at a place
# drawn the same way, folded in. Each call builds its own output string.


def replace_digits(s):
    out = []
    for i in range(len(s)):
        if i % 2 == 0:
            out.append(s[i])
        else:
            out.append(chr(ord(s[i - 1]) + ord(s[i]) - 48))
    return "".join(out)


def main():
    seed = 1844

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    cases = []
    for _ in range(40):
        s = []
        letter = 0
        for i in range(100):
            if i % 2 == 0:
                letter = next_random() % 26
                s.append(chr(97 + letter))
            else:
                most = min(25 - letter, 9)
                s.append(chr(48 + next_random() % (most + 1)))
        cases.append("".join(s))
    check = 0
    for call in range(500000):
        out = replace_digits(cases[(check + call) % 40])
        check = (check * 31 + ord(out[(check // 40 + call) % 100])) % 1000000007
    print(f"500000 calls: checksum {check}")


main()
