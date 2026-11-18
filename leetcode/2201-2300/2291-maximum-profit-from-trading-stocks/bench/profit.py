# LeetCode #2291: Maximum Profit From Trading Stocks -- the bench, the ★
# arm's Python mirror. A 0/1 knapsack row over the budget, run downwards
# for each stock that gains.


def maximum_profit(present, future, budget):
    best = [0] * (budget + 1)
    for i in range(len(present)):
        cost = present[i]
        gain = future[i] - present[i]
        if gain <= 0:
            continue
        for b in range(budget, cost - 1, -1):
            best[b] = max(best[b], best[b - cost] + gain)
    return best[budget]


# ---- bench harness ---------------------------------------------------------

seed = 2291


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    markets = []
    for _ in range(100):
        present = []
        future = []
        for _ in range(500):
            present.append(next_random() % 101)
            future.append(next_random() % 101)
        markets.append((present, future))
    check = 0
    for present, future in markets:
        check = (check * 31 + maximum_profit(present, future, 1000)) % 1000000007
    print(f"100 markets of 500 stocks, budget 1000: checksum {check}")


main()
