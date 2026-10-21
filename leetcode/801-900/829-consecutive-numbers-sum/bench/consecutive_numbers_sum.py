# Benchmark for #829: Consecutive Numbers Sum -- the ★ arm (each length).
#
# Mirrors consecutive_numbers_sum.kara: n has a run of k consecutive
# numbers exactly when n - k * (k - 1) / 2 is a positive multiple of k,
# and k runs while 1 + 2 + ... + k fits.


def consecutive_numbers_sum(n):
    count = 0
    k = 1
    while k * (k + 1) // 2 <= n:
        if (n - k * (k - 1) // 2) % k == 0:
            count += 1
        k += 1
    return count


def main():
    count, rounds = 64, 16000
    seed = 829

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    numbers = []
    for _ in range(count):
        a = next_random()
        r = a * 32768 + next_random()
        numbers.append(500000000 + r % 500000001)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        r = consecutive_numbers_sum(numbers[rnd % count])
        total += r
        checksum = (checksum * 131 + r) % 1000000007
    print(f"{rounds} rounds of {count} numbers: total {total}, checksum {checksum}")


main()
