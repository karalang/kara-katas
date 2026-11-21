# LeetCode #2521: Distinct Prime Factors of Product of Array -- benchmark
# mirror of the ★ arm (primes.kara): 200 lists of 1000 numbers built once,
# then the passes, each asking every list cut to a length the checksum
# picks.


def distinct_prime_factors(nums):
    primes = set()
    for x in nums:
        rest = x
        d = 2
        while d * d <= rest:
            if rest % d == 0:
                primes.add(d)
                while rest % d == 0:
                    rest //= d
            d += 1
        if rest > 1:
            primes.add(rest)
    return len(primes)


seed = 2521


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[next_random() % 999 + 2 for _ in range(1000)] for _ in range(200)]
    passes = 110
    check = 0
    for p in range(passes):
        for nums in lists:
            n = check % 1000 + 1
            part = nums[:n]
            check = (check * 31 + distinct_prime_factors(part) + p) % 1000000007
    print(f"{passes} passes over 200 lists of 1000 numbers: checksum {check}")


main()
