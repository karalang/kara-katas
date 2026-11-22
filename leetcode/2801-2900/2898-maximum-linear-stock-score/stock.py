# LeetCode #2898: Maximum Linear Stock Score -- the Python mirror of the
# ★ arm (stock.kara): the prices summed under prices[i] - i, and the
# largest sum.


def max_score(prices):
    sums = {}
    for i, p in enumerate(prices):
        sums[p - i] = sums.get(p - i, 0) + p
    return max(sums.values())


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(f"{max_score([1, 5, 3, 7, 8])} {max_score([5, 6, 7, 8, 9])}")
    n = 100000
    rising = [1000000000 - n + 1 + i for i in range(n)]
    falling = [1000000000 - i for i in range(n)]
    print(f"{max_score([1000000000] * n)} {max_score(rising)} {max_score(falling)}")
    seed = 2898
    total = 0
    check = 0
    for c in range(3100):
        small = c < 3000
        n = next_random() % 8 + 1 if small else wide() % 99001 + 1000
        prices = []
        for i in range(n):
            if small:
                prices.append(next_random() % 10 + 1)
            elif c % 2 == 1:
                prices.append(1000000 + i - next_random() % 50)
            else:
                prices.append(wide() % 1000000000 + 1)
        best = max_score(prices)
        total += best
        check = (check * 31 + best) % 1000000007
        if c == 2999:
            print(f"3000 small arrays: scores total {total}, checksum {check}")
            total = 0
            check = 0
    print(f"100 large arrays: scores total {total}, checksum {check}")


main()
