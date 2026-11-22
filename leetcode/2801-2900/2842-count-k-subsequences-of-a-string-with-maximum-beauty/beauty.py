# LeetCode #2842: Count K-Subsequences of a String With Maximum Beauty
# -- the Python mirror of the ★ arm: the counts sorted, most first, the
# letters above the k-th all taken and the rest chosen among those tied
# with it.

MOD = 1000000007


def choose(n, r):
    top = 1
    bottom = 1
    for i in range(r):
        top = top * (n - i) % MOD
        bottom = bottom * (i + 1) % MOD
    return top * pow(bottom, MOD - 2, MOD) % MOD


def count_k_subsequences_with_max_beauty(s, k):
    count = [0] * 26
    for c in s:
        count[ord(c) - 97] += 1
    freq = [c for c in count if c > 0]
    if k > len(freq):
        return 0
    freq.sort(reverse=True)
    last = freq[k - 1]
    above = sum(1 for f in freq if f > last)
    tied = sum(1 for f in freq if f == last)
    ways = choose(tied, k - above) * pow(last, k - above, MOD) % MOD
    for f in freq[:above]:
        ways = ways * f % MOD
    return ways


# ---- the harness: the same in every arm --------------------------------

seed = 2842


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n, kinds):
    return "".join(chr(97 + next_random() % kinds) for _ in range(n))


def main():
    best = count_k_subsequences_with_max_beauty
    print(f"{best('bcca', 2)} {best('abbcd', 4)} {best('aabb', 3)} {best('z', 1)}")
    long = letters(200000, 26)
    print(f"{best(long, 26)} {best(long, 13)}")
    check = 0
    zero = 0
    for c in range(3100):
        short = c < 3000
        n = next_random() % 10 + 1 if short else next_random() % 20000 + 1
        kinds = 5 if short else next_random() % 24 + 3
        s = letters(n, kinds)
        k = next_random() % 6 + 1 if short else next_random() % 26 + 1
        ways = best(s, k)
        if ways == 0:
            zero += 1
        check = (check * 31 + ways) % 1000000007
        if c == 2999:
            print(f"3000 short strings: {zero} with none, checksum {check}")
            check = 0
            zero = 0
    print(f"100 long strings: {zero} with none, checksum {check}")


main()
