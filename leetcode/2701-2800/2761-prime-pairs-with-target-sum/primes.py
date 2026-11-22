# LeetCode #2761: Prime Pairs With Target Sum -- the ★ arm in Python
# (primes.kara): a sieve of Eratosthenes up to n, then each x up to n / 2
# with x and n - x both prime.


def find_prime_pairs(n):
    prime = [True] * (n + 1)
    prime[0] = False
    if n >= 1:
        prime[1] = False
    p = 2
    while p * p <= n:
        if prime[p]:
            for m in range(p * p, n + 1, p):
                prime[m] = False
        p += 1
    return [[x, n - x] for x in range(2, n // 2 + 1) if prime[x] and prime[n - x]]


seed = 2761


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(pairs, acc):
    acc[0] += len(pairs)
    acc[1] = (acc[1] * 31 + len(pairs)) % 1000000007
    for a, b in pairs:
        acc[1] = (acc[1] * 31 + a * 1000003 + b) % 1000000007


def show(pairs):
    return "[" + ", ".join(f"[{a}, {b}]" for a, b in pairs) + "]"


def main():
    for n in [10, 2, 4, 9, 11, 100]:
        print(show(find_prime_pairs(n)))
    acc = [0, 0]
    for n in range(1, 2001):
        fold(find_prime_pairs(n), acc)
    print(f"n from 1 to 2000: {acc[0]} pairs, checksum {acc[1]}")
    acc = [0, 0]
    for _ in range(20):
        n = (next_random() * 32768 + next_random()) % 1000000 + 1
        fold(find_prime_pairs(n), acc)
    fold(find_prime_pairs(1000000), acc)
    print(f"21 n up to 10^6: {acc[0]} pairs, checksum {acc[1]}")


main()
