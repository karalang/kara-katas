"""LeetCode #1621: Number of Sets of K Non-Overlapping Line Segments -- Python
mirror of the ★ arm (segments.kara): C(n + k - 1, 2k) by factorials and
Fermat's inverse."""

MOD = 1000000007


def number_of_sets(n, k):
    top = n + k - 1
    pick = 2 * k
    fact = [1] * (top + 1)
    for i in range(1, top + 1):
        fact[i] = fact[i - 1] * i % MOD
    below = fact[pick] * fact[top - pick] % MOD
    return fact[top] * pow(below, MOD - 2, MOD) % MOD


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    for n, k in [(4, 2), (3, 1), (30, 7), (2, 1), (1000, 1), (1000, 999)]:
        print(number_of_sets(n, k))
    check = pairs = 0
    for n in range(2, 41):
        for k in range(1, n):
            check = mix(check, number_of_sets(n, k))
            pairs += 1
    print(f"all {pairs} pairs up to 40 points: checksum {check}")
    seed = 1621

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    check = 0
    for _ in range(30):
        n = next_random() % 999 + 2
        k = next_random() % (n - 1) + 1
        check = mix(check, number_of_sets(n, k))
    print(f"30 random pairs up to 1000 points: checksum {check}")


main()
