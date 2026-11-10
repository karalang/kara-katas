# LeetCode #2110: Number of Smooth Descent Periods of a Stock -- the
# benchmark, the same algorithm as descent.kara: the descent run's length
# up to each day, summed.


def get_descent_periods(prices):
    run = 1
    total = 1
    for i in range(1, len(prices)):
        if prices[i - 1] - prices[i] == 1:
            run += 1
        else:
            run = 1
        total += run
    return total


seed = 2110


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(20):
        p = 5000000
        prices = []
        for _ in range(100000):
            prices.append(p)
            p = p - 1 if next_random() % 4 != 0 else p + next_random() % 20
        arrays.append(prices)
    total = 0
    check = 0
    for rnd in range(10):
        for a in range(20):
            arrays[a][rnd * 9973] += 1
            got = get_descent_periods(arrays[a])
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"200 counts: {total} periods, checksum {check}")


main()
