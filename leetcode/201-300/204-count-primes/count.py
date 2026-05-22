"""LeetCode 204 — Count Primes (Python mirror).

Same algorithm as count.kara: trial division up to sqrt(n), skipping
even factors after the 2-special-case. Used by bench.sh as the
correctness oracle (kara, rust, c, py must all emit identical sinks).
"""


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def list_primes_under(n: int) -> list[int]:
    return [k for k in range(n) if is_prime(k)]


def count_primes(n: int) -> int:
    return len(list_primes_under(n))


if __name__ == "__main__":
    for n in (10, 100, 1000, 10000, 100000):
        print(count_primes(n))
