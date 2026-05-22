"""LeetCode 204 — bench mirror in Python. Sequential implementation;
matches the kara/rust/c sinks for N = 10_000_000.

Python is the *correctness* oracle for bench.sh's sink-agreement check.
Timing-wise it's expected to be the slowest by orders of magnitude — the
interpreter overhead per is_prime() call drowns the algorithmic cost.
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


if __name__ == "__main__":
    n = 10_000_000

    primes: list[int] = []
    for k in range(n):
        if is_prime(k):
            primes.append(k)

    print(len(primes))
    print(sum(primes))
