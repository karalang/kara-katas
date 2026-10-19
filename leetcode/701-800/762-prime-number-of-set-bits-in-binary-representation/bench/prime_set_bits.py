# LeetCode 762 — Prime Number of Set Bits in Binary Representation:
# benchmark, the ★ arm in Python.

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19)


def count_prime_set_bits(left, right):
    count = 0
    for n in range(left, right + 1):
        bits = 0
        rest = n
        while rest > 0:
            rest &= rest - 1
            bits += 1
        if bits in PRIMES:
            count += 1
    return count


def main():
    seed = 762

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    rounds = 10000
    total = 0
    check = 0
    for _ in range(rounds):
        high = next_random()
        left = 1 + (high * 32768 + next_random()) % 990000
        count = count_prime_set_bits(left, left + 10000)
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"{rounds} ranges of 10001 numbers: {total} counted, checksum {check}")


main()
