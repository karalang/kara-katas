# Benchmark for #461: mirror of hamming_distance.kara (the star arm,
# clearing the lowest set bit) on the same workload.


def hamming_distance(x, y):
    z = x ^ y
    count = 0
    while z != 0:
        z &= z - 1
        count += 1
    return count


def main():
    n = 1000000
    rounds = 20
    seed = 461

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def random31():
        a = next_random()
        b = next_random()
        c = next_random()
        return ((a * 32768 + b) * 2 + c % 2) % 2147483648

    nums = [random31() for _ in range(n)]
    total = 0
    checksum = 0
    for _ in range(rounds):
        hi = next_random()
        lo = next_random()
        k = (hi * 65536 + lo) % n
        nums[k] = random31()
        s = 0
        for i in range(1, n):
            s += hamming_distance(nums[i - 1], nums[i])
        total += s
        checksum = (checksum * 31 + s) % 1000000007
    print(f"{rounds} rounds on {n} numbers: total distance {total}, checksum {checksum}")


main()
