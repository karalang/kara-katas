# LeetCode #2830: Maximize the Profit as the Salesman -- the
# bench's Python mirror of the ★ arm: the offers filed by their last
# house, and best[i] the most gold from the first i houses.


def maximize_the_profit(n, offers):
    ending = [[] for _ in range(n)]
    for s, e, g in offers:
        ending[e].append((s, g))
    best = [0] * (n + 1)
    for i in range(n):
        best[i + 1] = best[i]
        for s, g in ending[i]:
            best[i + 1] = max(best[i + 1], best[s] + g)
    return best[n]


seed = 2830


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 20, 10, 100000
    streets = []
    for _ in range(count):
        offers = []
        for _ in range(n):
            start = wide() % n
            end = min(start + next_random() % 100, n - 1)
            offers.append([start, end, next_random() % 1000 + 1])
        streets.append(offers)
    total = 0
    check = 0
    for r in range(rounds):
        for offers in streets:
            a = maximize_the_profit(n, offers)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} streets of {n}, {rounds} rounds: gold totals {total}, checksum {check}")


main()
