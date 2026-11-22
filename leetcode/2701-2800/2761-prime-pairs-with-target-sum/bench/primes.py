# LeetCode #2761: Prime Pairs With Target Sum -- the bench (primes.kara in
# Python): a sieve of Eratosthenes up to n, then each x up to n / 2 with x
# and n - x both prime.


def find_prime_pairs(n):
    prime = [True] * (n + 1)
    prime[0] = False
    if n >= 1:
        prime[1] = False
    p = 2
    while p * p <= n:
        if prime[p]:
            m = p * p
            while m <= n:
                prime[m] = False
                m += p
        p += 1
    return [[x, n - x] for x in range(2, n // 2 + 1) if prime[x] and prime[n - x]]


seed = 2761


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 20, 3
    targets = [(next_random() * 32768 + next_random()) % 100000 + 900001 for _ in range(count)]
    pairs_seen = check = 0
    for r in range(rounds):
        for n in targets:
            pairs = find_prime_pairs(n)
            pairs_seen += len(pairs)
            check = (check * 31 + len(pairs) + r) % 1000000007
            for pair in pairs:
                check = (check * 31 + pair[0]) % 1000000007
    print(f"{count} n near 10^6, {rounds} rounds: {pairs_seen} pairs, checksum {check}")


main()
