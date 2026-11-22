# LeetCode #2851: String Transformation -- the bench: the ★ arm over 10
# pairs of 5 * 10^5 letters, LeetCode's most, each s a block of up to 8
# letters repeated, half of them with one letter changed, t a rotation of
# s two times in three and otherwise s with one letter changed, k up to
# about 10^15, all drawn first, then each answered 5 times.

MOD = 1000000007


def number_of_ways(s, t, k):
    n = len(s)
    text = s + s
    fail = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and t[i] != t[j]:
            j = fail[j - 1]
        if t[i] == t[j]:
            j += 1
        fail[i] = j
    at_zero = elsewhere = 0
    j = 0
    for i in range(2 * n - 1):
        while j > 0 and text[i] != t[j]:
            j = fail[j - 1]
        if text[i] == t[j]:
            j += 1
        if j == n:
            if i + 1 == n:
                at_zero += 1
            else:
                elsewhere += 1
            j = fail[j - 1]
    all_ = pow(n - 1, k, MOD)
    sign = 1 if k % 2 == 0 else MOD - 1
    inverse = pow(n, MOD - 2, MOD)
    zero_ways = (all_ + (n - 1) * sign) % MOD * inverse % MOD
    other_ways = (all_ - sign + MOD) % MOD * inverse % MOD
    return (at_zero * zero_ways + elsewhere * other_ways) % MOD


def main():
    count, rounds, n = 10, 5, 500000
    seed = 2851

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    pairs = []
    for _ in range(count):
        block = nr() % 8 + 1
        letters = nr() % 3 + 1
        unit = [97 + nr() % letters for _ in range(block)]
        s = [unit[i % block] for i in range(n)]
        if nr() % 2 == 0:
            at = wide() % n
            s[at] = 97 + nr() % 3
        if nr() % 3 < 2:
            r = wide() % n
            t = s[n - r:] + s[:n - r]
        else:
            t = s[:]
            at = wide() % n
            t[at] = 97 + (t[at] - 97 + 1) % 3
        k = wide() * 900000 + 1
        pairs.append((bytes(s).decode(), bytes(t).decode(), k))
    check = 0
    for r in range(rounds):
        for s, t, k in pairs:
            check = (check * 31 + number_of_ways(s, t, k) + r) % MOD
    print(f"{count} pairs of {n}, {rounds} rounds: checksum {check}")


main()
