# LeetCode #2819: Minimum Relative Loss After Buying Chocolates -- the
# bench's Python mirror of the ★ arm: the prices sorted, prefix sums, and for each
# query a binary search for how many of the m to take from the cheap end.


def minimum_relative_losses(prices, queries):
    s = sorted(prices)
    n = len(s)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + s[i]
    out = []
    for k, m in queries:
        lo, hi = 0, m
        while lo < hi:
            mid = (lo + hi) // 2
            if s[mid] + s[n - m + mid] < 2 * k:
                lo = mid + 1
            else:
                hi = mid
        dear = prefix[n] - prefix[n - m + lo]
        out.append(prefix[lo] + 2 * k * (m - lo) - dear)
    return out


seed = 2819


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 10, 3, 100000
    shops = []
    for _ in range(count):
        prices = [wide() % 1000000000 + 1 for _ in range(n)]
        queries = []
        for _ in range(n):
            k = wide() % 1000000000 + 1
            queries.append([k, wide() % n + 1])
        shops.append((prices, queries))
    negative = 0
    check = 0
    for r in range(rounds):
        for prices, queries in shops:
            for a in minimum_relative_losses(prices, queries):
                if a < 0:
                    negative += 1
                check = (check * 31 + a + r) % 1000000007
    print(f"{count} shops of {n}, {rounds} rounds: {negative} losses below 0, checksum {check}")


main()
