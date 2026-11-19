# LeetCode #1625: Lexicographically Smallest String After Applying
# Operations -- the bench in Python, mirroring smallest.kara: every
# rotation by a multiple of gcd(b, n) with every count of additions, each
# string made and the least kept.

from math import gcd

seed = 1625


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find_lex_smallest_string(s, a, b):
    digits = [ord(c) - 48 for c in s]
    n = len(digits)
    step = gcd(b, n)
    even_counts = 10 if b % 2 == 1 else 1
    best = s
    for start in range(0, n, step):
        for odd in range(10):
            for even in range(even_counts):
                chars = []
                for i in range(n):
                    count = odd if i % 2 == 1 else even
                    chars.append(chr(48 + (digits[(i + start) % n] + count * a) % 10))
                t = "".join(chars)
                if t < best:
                    best = t
    return best


def main():
    cases = []
    for _ in range(200):
        s = "".join(chr(48 + next_random() % 10) for _ in range(100))
        a = next_random() % 9 + 1
        b = next_random() % 99 + 1
        cases.append((s, a, b))
    check = 0
    zeros = 0
    for s, a, b in cases:
        for c in find_lex_smallest_string(s, a, b):
            if c == "0":
                zeros += 1
            check = (check * 31 + ord(c) - 48 + 1) % 1000000007
    print(f"200 cases of 100 digits: {zeros} zeros in the answers, checksum {check}")


main()
