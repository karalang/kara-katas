# LeetCode #991: Broken Calculator -- bench, the ★ arm (greedy from the
# target back), the same algorithm and workload as broken_calc.kara.


def broken_calc(start_value, target):
    ops = 0
    t = target
    while t > start_value:
        if t % 2 == 1:
            t += 1
        else:
            t //= 2
        ops += 1
    return ops + start_value - t


seed = 991


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 5000
    starts = []
    targets = []
    for _ in range(1000):
        starts.append(1 + (next_random() * 32768 + next_random()) % 1000)
        targets.append(1 + (next_random() * 32768 + next_random()) % 1000000000)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(1000):
            got = broken_calc(starts[(r + i) % 1000], targets[i])
            total += got
            check = (check * 31 + got + 1) % 1000000007
    print(f"{rounds} rounds over 1000 pairs: {total} operations, checksum {check}")


main()
