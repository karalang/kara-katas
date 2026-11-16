# LeetCode #1175: Prime Arrangements -- the ★ arm's bench in Python: a sieve
# of Eratosthenes counts the primes up to n, and the answer is
# p! * (n - p)! modulo 10^9 + 7. The same million calls.
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
            j = i * i
            while j <= n:
                composite[j] = True
                j += i
    return factorial(primes) * factorial(n - primes) % MOD


seed = 1175


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    calls = 1000000
    check = 0
    for _ in range(calls):
        n = 1 + next_random() % 100
        check = (check * 131 + num_prime_arrangements(n)) % 1000000007
    print(f"{calls} calls: checksum {check}")


main()
