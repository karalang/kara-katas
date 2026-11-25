# LeetCode #1375 bench -- Python: the ★ arm: after step i the string is
# aligned exactly when the largest bit flipped so far is i.

seed = 1375


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def num_times_all_blue(flips):
    largest = 0
    aligned = 0
    for i, f in enumerate(flips):
        largest = max(largest, f)
        if largest == i + 1:
            aligned += 1
    return aligned


def main():
    # 20 orders of 5 * 10^4 bits, 1 to n shuffled within runs of 2 to 8,
    # built once; then 1000 rounds, each trading two neighbouring flips
    # of one order, both drawn from the checksum so far, and counting
    # that order's aligned steps
    n = 50000
    orders = []
    for _ in range(20):
        flips = list(range(1, n + 1))
        start = 0
        while start < n:
            end = min(start + 2 + next_random() % 7, n)
            for i in range(end - 1, start, -1):
                j = start + next_random() % (i - start + 1)
                flips[i], flips[j] = flips[j], flips[i]
            start = end
        orders.append(flips)
    check = 0
    for r in range(1000):
        flips = orders[check % 20]
        k = (check // 20) % (n - 1)
        flips[k], flips[k + 1] = flips[k + 1], flips[k]
        got = num_times_all_blue(flips)
        check = (check * 31 + got + r) % 1000000007
    print(f"1000 rounds over 20 orders of 50000 bits: checksum {check}")


main()
