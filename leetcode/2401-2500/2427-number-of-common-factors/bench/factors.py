# LeetCode #2427: Number of Common Factors -- the bench, the ★ arm: the
# divisors of gcd(a, b), counted in pairs up to its square root.


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def common_factors(a, b):
    g = gcd(a, b)
    count = 0
    d = 1
    while d * d <= g:
        if g % d == 0:
            count += 1 if d * d == g else 2
        d += 1
    return count


def main():
    check = 0
    for p in range(5):
        for a in range(1, 1001):
            for b in range(1, 1001):
                other = (b + p - 1) % 1000 + 1
                check = (check * 31 + common_factors(a, other) + p) % 1000000007
    print(f"5 passes over 10^6 pairs: checksum {check}")


main()
