# LeetCode #1808: Maximize Number of Nice Divisors -- the ★ arm in Python:
# the largest product of parts summing to `prime_factors`, all 3s with a 4
# or a 2 for what is left over, the power of 3 taken by squaring.
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


seed = 1808


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # LeetCode's two examples
    print(max_nice_divisors(5), max_nice_divisors(8))
    # the edges
    small = [str(max_nice_divisors(n)) for n in range(1, 8)]
    print(" ".join(small), max_nice_divisors(1000000000), max_nice_divisors(999999999), max_nice_divisors(999999998))
    # 1 to 2000 in turn, and 3000 at random to 10^9
    check = 0
    for n in range(1, 2001):
        check = (check * 31 + max_nice_divisors(n)) % 1000000007
    print(f"1 to 2000: checksum {check}")
    check = 0
    for _ in range(3000):
        hi = next_random()
        n = 1 + (hi * 32768 + next_random()) % 1000000000
        check = (check * 31 + max_nice_divisors(n)) % 1000000007
    print(f"3000 at random to 10^9: checksum {check}")


main()
