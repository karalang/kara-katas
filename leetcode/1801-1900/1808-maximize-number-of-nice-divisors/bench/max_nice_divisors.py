# LeetCode #1808: Maximize Number of Nice Divisors -- the bench in Python:
# the ★ arm over 2 * 10^6 calls, each count of prime factors drawn from the
# checksum so far.
MOD = 1000000007


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


def max_nice_divisors(prime_factors):
    n = prime_factors
    if n <= 3:
        return n
    if n % 3 == 0:
        return power(3, n // 3)
    if n % 3 == 1:
        return power(3, n // 3 - 1) * 4 % MOD
    return power(3, n // 3) * 2 % MOD


def main():
    check = 0
    for call in range(2000000):
        n = 1 + (check * 7919 + call) % 1000000000
        check = (check * 31 + max_nice_divisors(n)) % 1000000007
    print(f"2000000 calls: checksum {check}")


main()
