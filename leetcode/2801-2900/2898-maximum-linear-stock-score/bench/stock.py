# LeetCode #2898: Maximum Linear Stock Score -- the bench's Python mirror
# (stock.kara): the same draw, the prices summed under prices[i] - i in a
# dict.


def max_score(prices):
    sums = {}
    for i, p in enumerate(prices):
        sums[p - i] = sums.get(p - i, 0) + p
    return max(sums.values())


seed = 2898


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 20, 20, 100000
    cases = []
    for c in range(count):
        prices = []
        for i in range(n):
            if c % 2 == 0:
                prices.append(wide() % 1000000000 + 1)
            else:
                prices.append(1000000 + i - next_random() % 50)
        cases.append(prices)
    total = 0
    check = 0
    for r in range(rounds):
        for prices in cases:
            score = max_score(prices)
            total += score
            check = (check * 31 + score % 1000000007 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: scores total {total}, checksum {check}")


main()
