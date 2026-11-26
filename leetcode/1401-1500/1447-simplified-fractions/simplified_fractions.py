# LeetCode #1447 Simplified Fractions: a mirror of simplified_fractions.kara.


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


# ---- test harness ---------------------------------------------------------


def fold(fractions, check):
    for f in sorted(fractions):
        for b in f.encode():
            check = (check * 131 + b) % 1000000007
        check = (check * 131 + 32) % 1000000007
    return check


def main():
    print(" ".join(f"[{', '.join(sorted(simplified_fractions(n)))}]" for n in range(1, 5)))
    most = simplified_fractions(100)
    print(f"n = 100: {len(most)} fractions, checksum {fold(most, 0)}")
    total = 0
    check = 0
    for n in range(1, 101):
        fractions = simplified_fractions(n)
        total += len(fractions)
        check = fold(fractions, check)
    print(f"every n to 100: {total} fractions, checksum {check}")


main()
