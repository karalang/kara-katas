# LeetCode #2521: Distinct Prime Factors of Product of Array -- Python
# mirror of the ★ arm (primes.kara): each number split by trial division,
# every prime into a set; the same harness and output.


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
    fixed = [
        [2, 4, 3, 7, 10, 6],
        [2, 4, 8, 16],
        [1000],
        [997],
        [30, 30, 30],
        [961, 31, 2],
        [512, 729, 625, 343],
        [210, 770, 858],
    ]
    for nums in fixed:
        print(f"[{', '.join(map(str, nums))}] -> {distinct_prime_factors(nums)}")
    for most, top in [(10, 50), (100, 1000)]:
        total = 0
        check = 0
        for _ in range(2000):
            n = next_random() % most + 1
            nums = [next_random() % (top - 1) + 2 for _ in range(n)]
            a = distinct_prime_factors(nums)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"2000 random lists of up to {most} numbers to {top}: total {total}, checksum {check}")
    every = [i % 999 + 2 for i in range(10000)]
    print(f"10^4 numbers cycling 2 to 1000: {distinct_prime_factors(every)}")
    print(f"10^4 of 1000: {distinct_prime_factors([1000] * 10000)}")
    random = [next_random() % 999 + 2 for _ in range(10000)]
    print(f"10^4 random to 1000: {distinct_prime_factors(random)}")


main()
