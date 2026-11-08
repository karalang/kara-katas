# LeetCode #1071: Greatest Common Divisor of Strings -- the Python mirror of
# gcd_strings.kara (the ★ arm): the two concatenations compared, then the
# prefix as long as the gcd of the lengths.


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def gcd_of_strings(a, b):
    if a + b != b + a:
        return ""
    return a[: gcd(len(a), len(b))]


seed = 1071


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, k):
    return "".join(chr(ord("A") + next_random() % k) for _ in range(n))


def random_pair(longest, most, k):
    root = random_word(next_random() % longest + 1, k)
    a = root * (next_random() % most + 1)
    b = root * (next_random() % most + 1)
    roll = next_random() % 6
    if roll < 2:
        at = next_random() % len(b)
        letter = chr(ord("A") + next_random() % k)
        b = b[:at] + letter + b[at + 1 :]
    elif roll == 2:
        b = random_word(next_random() % (longest * most) + 1, k)
    return a, b


def checksum(s):
    check = len(s)
    for c in s.encode():
        check = (check * 31 + c) % 1000000007
    return check


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        ("ABCABC", "ABC"),
        ("ABABAB", "ABAB"),
        ("LEET", "CODE"),
        ("A", "A"),
        ("AAAAAA", "AAAA"),
        ("ABAB", "ABA"),
        ("ABCABCABC", "ABCABC"),
        ("TAUXXTAUXXTAUXXTAUXXTAUXX", "TAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXX"),
        ("AA", "AB"),
    ]
    for a, b in examples:
        print(f'{a} {b} -> "{gcd_of_strings(a, b)}"')
    for count, longest, most, ks, label in [(3000, 4, 6, 3, "3000 pairs up to 24 letters"), (300, 20, 50, 4, "300 pairs up to 1000 letters")]:
        found = letters = check = 0
        for _ in range(count):
            k = next_random() % ks + 1
            a, b = random_pair(longest, most, k)
            x = gcd_of_strings(a, b)
            if len(x) > 0:
                found += 1
            letters += len(x)
            check = (check * 31 + checksum(x)) % 1000000007
        print(f"{label}: {found} found, {letters} letters, checksum {check}")
    a1000 = "A" * 1000
    print(f"1000 A's against 999, 600, 250 and 1: {show([len(gcd_of_strings(a1000, 'A' * n)) for n in [999, 600, 250, 1]])}")
    abc = "ABC" * 333
    print(f"333 ABC's against 111, 222, 1 and 332: {show([len(gcd_of_strings(abc, 'ABC' * n)) for n in [111, 222, 1, 332]])}")
    near = "AB" * 499 + "AC"
    print(f'500 AB\'s against 499 and an AC: "{gcd_of_strings("AB" * 500, near)}"')


main()
