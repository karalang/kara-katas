# Benchmark for #650: the sum of the prime factors, as the Kara ★ arm.


def min_steps(n):
    rest = n
    steps = 0
    p = 2
    while p * p <= rest:
        while rest % p == 0:
            steps += p
            rest //= p
        p += 1
    if rest > 1:
        steps += rest
    return steps


def main():
    limit = 1000000
    total = 0
    checksum = 0
    for n in range(1, limit + 1):
        steps = min_steps(n)
        total += steps
        checksum = (checksum * 31 + steps) % 1000000007
    print(f"1 to {limit}: total {total}, checksum {checksum}")


main()
