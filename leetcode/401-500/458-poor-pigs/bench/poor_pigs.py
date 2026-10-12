# Benchmark for #458: mirror of poor_pigs.kara (the star arm, growing the
# number of outcomes) on the same workload.


def poor_pigs(buckets, minutes_to_die, minutes_to_test):
    states = minutes_to_test // minutes_to_die + 1
    pigs = 0
    covered = 1
    while covered < buckets:
        covered *= states
        pigs += 1
    return pigs


def main():
    n = 1000000
    rounds = 20
    seed = 458

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    buckets = []
    die = []
    test = []
    for _ in range(n):
        digits = next_random() % 13
        top = 10 ** digits
        a = next_random()
        b = next_random()
        c = next_random()
        r = (a * 65536 + b) * 65536 + c
        buckets.append(1 + r % top)
        d = 1 + next_random() % 100
        die.append(d)
        test.append(d + next_random() % (101 - d))
    total = 0
    checksum = 0
    for _ in range(rounds):
        hi = next_random()
        lo = next_random()
        k = (hi * 65536 + lo) % n
        hi = next_random()
        lo = next_random()
        buckets[k] = 1 + (hi * 65536 + lo) % 1000000000000
        s = 0
        for i in range(n):
            s += poor_pigs(buckets[i], die[i], test[i])
        total += s
        checksum = (checksum * 31 + s) % 1000000007
    print(f"{rounds} rounds on {n} queries: {total} pigs, checksum {checksum}")


main()
