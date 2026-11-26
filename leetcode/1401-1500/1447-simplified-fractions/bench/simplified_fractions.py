# LeetCode #1447 Simplified Fractions: the bench, a mirror of
# simplified_fractions.kara.


def simplified_fractions(n):
    # every numerator below every denominator up to n, kept when the two
    # share no factor
    fractions = []
    for d in range(2, n + 1):
        for a in range(1, d):
            if gcd(a, d) == 1:
                fractions.append(f"{a}/{d}")
    return fractions


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def main():
    # every n from 1 to 100, 100 times over, each answer's letters counted
    # and folded to a checksum
    check = 0
    for _ in range(100):
        for n in range(1, 101):
            letters = sum(len(f) for f in simplified_fractions(n))
            check = (check * 131 + letters) % 1000000007
    print(f"10000 answers: checksum {check}")


main()
