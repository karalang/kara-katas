"""LeetCode #1621: Number of Sets of K Non-Overlapping Line Segments -- the
bench in Python, mirroring segments.kara: C(n + k - 1, 2k) by factorials
and Fermat's inverse, the factorials made afresh for every query."""

MOD = 1000000007


def number_of_sets(n, k):
    top = n + k - 1
    pick = 2 * k
    fact = [1] * (top + 1)
    for i in range(1, top + 1):
        fact[i] = fact[i - 1] * i % MOD
    below = fact[pick] * fact[top - pick] % MOD
    return fact[top] * pow(below, MOD - 2, MOD) % MOD


def main():
    seed = 1621

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    pairs = []
    for _ in range(400000):
        n = next_random() % 999 + 2
        k = next_random() % (n - 1) + 1
        pairs.append((n, k))
    check = total = 0
    for n, k in pairs:
        ways = number_of_sets(n, k)
        total = (total + ways) % MOD
        check = (check * 31 + ways + 1) % 1000000007
    print(f"400000 random pairs: counts sum to {total} mod 10^9 + 7, checksum {check}")


main()
