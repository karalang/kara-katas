# LeetCode #1071: Greatest Common Divisor of Strings -- the benchmark's
# Python mirror of gcd_strings.kara: the same concatenations compared over
# 20000 pairs built once, each answered 50 times.


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def gcd_of_strings(a, b):
    if a + b != b + a:
        return ""
    return a[: gcd(len(a), len(b))]


def main():
    seed = 1071

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def random_word(n, k):
        return "".join(chr(ord("A") + next_random() % k) for _ in range(n))

    pairs = []
    for _ in range(20000):
        k = next_random() % 4 + 1
        root = random_word(next_random() % 20 + 1, k)
        a = root * (next_random() % 50 + 1)
        b = root * (next_random() % 50 + 1)
        roll = next_random() % 6
        if roll < 2:
            at = next_random() % len(b)
            letter = chr(ord("A") + next_random() % k)
            b = b[:at] + letter + b[at + 1 :]
        elif roll == 2:
            b = random_word(next_random() % 1000 + 1, k)
        pairs.append((a, b))
    found = letters = check = 0
    for _ in range(50):
        for a, b in pairs:
            x = gcd_of_strings(a, b)
            if len(x) > 0:
                found += 1
            letters += len(x)
            check = (check * 31 + len(x)) % 1000000007
    print(f"1000000 calls: {found} found, {letters} letters, checksum {check}")


main()
