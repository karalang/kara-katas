# LeetCode #1175: Prime Arrangements -- the mirror of the Kāra ★ arm: the
# primes up to n counted with a sieve, the answer p! * (n - p)! modulo
# 10^9 + 7. With `lit` as its argument it reads the statement literally
# instead, for n up to 8: every permutation of 1..n tried, the ones with
# every prime value on a prime index counted.
import itertools
import sys

MOD = 1000000007


def factorial(k):
    f = 1
    for i in range(2, k + 1):
        f = f * i % MOD
    return f


def num_prime_arrangements(n):
    composite = [False] * (n + 1)
    primes = 0
    for i in range(2, n + 1):
        if not composite[i]:
            primes += 1
            for j in range(i * i, n + 1, i):
                composite[j] = True
    return factorial(primes) * factorial(n - primes) % MOD


def is_prime(x):
    return x >= 2 and all(x % d for d in range(2, x))


def literal(n):
    return sum(
        all(is_prime(v) == is_prime(i + 1) for i, v in enumerate(p) if is_prime(v))
        for p in itertools.permutations(range(1, n + 1))
    )


def main():
    f = num_prime_arrangements
    print(f"n = 5: {f(5)}")
    print(f"n = 100: {f(100)}")
    print(f"n = 1 to 12: {[f(n) for n in range(1, 13)]}")
    print(f"n = 88, 89, 96, 97, 99: {f(88)} {f(89)} {f(96)} {f(97)} {f(99)}")
    check = 0
    for n in range(1, 101):
        check = (check * 131 + f(n)) % 1000000007
    print(f"n = 1 to 100: checksum {check}")
    if len(sys.argv) > 1 and sys.argv[1] == "lit":
        print(f"literal, n = 1 to 8: {[literal(n) for n in range(1, 9)]}")


main()
