# LeetCode #1625: Lexicographically Smallest String After Applying
# Operations -- the Python mirror of smallest.kara (★).
#
# Every reachable string is a rotation by a multiple of gcd(b, n), with
# some count of `a` added to its odd digits and, when b is odd, to its even
# digits too; every such string is made and the least kept.

from math import gcd


def find_lex_smallest_string(s, a, b):
    digits = [ord(c) - 48 for c in s]
    n = len(digits)
    step = gcd(b, n)
    even_counts = 10 if b % 2 == 1 else 1
    best = s
    for start in range(0, n, step):
        for odd in range(10):
            for even in range(even_counts):
                t = "".join(
                    chr(48 + (digits[(i + start) % n] + (odd if i % 2 == 1 else even) * a) % 10)
                    for i in range(n)
                )
                if t < best:
                    best = t
    return best


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, longest):
    check = 0
    unchanged = 0
    for _ in range(count):
        n = 2 * (next_random() % (longest // 2) + 1)
        s = "".join(chr(48 + next_random() % 10) for _ in range(n))
        a = next_random() % 9 + 1
        b = next_random() % (n - 1) + 1
        got = find_lex_smallest_string(s, a, b)
        if got == s:
            unchanged += 1
        for c in got:
            check = mix(check, ord(c) - 48)
    print(f"{count} cases of up to {longest} digits: {unchanged} already smallest, checksum {check}")


def main():
    global seed
    print(find_lex_smallest_string("5525", 9, 2))
    print(find_lex_smallest_string("74", 5, 1))
    print(find_lex_smallest_string("0011", 4, 2))
    print(find_lex_smallest_string("43987654", 7, 3))
    print(find_lex_smallest_string("9999999999", 5, 4))
    seed = 1625
    batch(1000, 10)
    batch(100, 40)
    batch(10, 100)


main()
