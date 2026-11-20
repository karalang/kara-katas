# LeetCode #2400: Number of Ways to Reach a Position After Exactly k
# Steps -- the bench, the ★ arm in Python: C(k, (k + d) / 2) from
# factorials modulo 10^9 + 7 and Fermat's inverse.

MOD = 1000000007
seed = 2400


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number_of_ways(start_pos, end_pos, k):
    d = abs(end_pos - start_pos)
    if d > k or (k - d) % 2 == 1:
        return 0
    toward = (k + d) // 2
    factorial = [1] * (k + 1)
    for i in range(1, k + 1):
        factorial[i] = factorial[i - 1] * i % MOD
    return factorial[k] * pow(factorial[toward], MOD - 2, MOD) % MOD * pow(factorial[k - toward], MOD - 2, MOD) % MOD


def main():
    check = 0
    zeros = 0
    for _ in range(300000):
        k = 1 + next_random() % 1000
        start = 1 + next_random() % 1000
        end = min(max(start - k + 2 * (next_random() % (k + 1)), 1), 1000)
        w = number_of_ways(start, end, k)
        if w == 0:
            zeros += 1
        check = (check * 31 + w) % MOD
    print(f"300000 queries of k up to 1000: checksum {check}, {zeros} zeros")


main()
