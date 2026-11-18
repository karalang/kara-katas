# LeetCode #2291: Maximum Profit From Trading Stocks -- the ★ arm's
# Python mirror. A 0/1 knapsack over the budget, run downwards.


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


# ---- test harness ---------------------------------------------------------

seed = 2291


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        ([5, 4, 6, 2, 3], [8, 5, 4, 3, 5], 10),
        ([2, 2, 5], [3, 4, 10], 6),
        ([3, 3, 12], [0, 3, 15], 10),
        ([1, 2], [5, 9], 0),
        ([0, 0, 3], [4, 0, 9], 2),
        ([5, 6, 7], [5, 1, 0], 100),
        ([10, 1, 1], [30, 5, 5], 10),
    ]
    for present, future, budget in cases:
        print(f"{len(present)} stocks, budget {budget}: {maximum_profit(present, future, budget)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = next_random() % 10 + 1
        present = []
        future = []
        for _ in range(n):
            present.append(next_random() % 101)
            future.append(next_random() % 101)
        budget = next_random() % 401
        profit = maximum_profit(present, future, budget)
        check = (check * 31 + profit) % 1000000007
        total += profit
    print(f"2000 markets: checksum {check}, {total} profit")


main()
