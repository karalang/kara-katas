# LeetCode #2842: Count K-Subsequences of a String With Maximum Beauty
# -- the bench, mirrored from beauty.kara: the counts sorted, most
# first, the letters above the k-th all taken and the rest chosen
# among those tied with it.

MOD = 1000000007
seed = 2842


def power(base, exp):
    result = 1
    b = base % MOD
    e = exp
    while e > 0:
        if e % 2 == 1:
            result = result * b % MOD
        b = b * b % MOD
        e //= 2
    return result


def choose(n, r):
    top = 1
    bottom = 1
    for i in range(r):
        top = top * (n - i) % MOD
        bottom = bottom * (i + 1) % MOD
    return top * power(bottom, MOD - 2) % MOD


def count_k_subsequences_with_max_beauty(s, k):
    count = [0] * 26
    for b in s:
        count[b - 97] += 1
    freq = [c for c in count if c > 0]
    if k > len(freq):
        return 0
    freq.sort(reverse=True)
    last = freq[k - 1]
    above = sum(1 for f in freq if f > last)
    tied = sum(1 for f in freq if f == last)
    ways = choose(tied, k - above) * power(last, k - above) % MOD
    for f in freq[:above]:
        ways = ways * f % MOD
    return ways


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 100, 200000, 40
    cases = []
    for _ in range(count):
        kinds = next_random() % 24 + 3
        s = bytes(97 + next_random() % kinds for _ in range(n))
        k = next_random() % 26 + 1
        cases.append((s, k))
    zero = 0
    check = 0
    for r in range(rounds):
        for s, k in cases:
            ways = count_k_subsequences_with_max_beauty(s, k)
            if ways == 0:
                zero += 1
            check = (check * 31 + ways + r) % 1000000007
    print(f"{count} strings of {n}, {rounds} rounds: {zero} with none, checksum {check}")


main()
