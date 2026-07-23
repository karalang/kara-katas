"""Benchmark workload for LeetCode #188 — Best Time to Buy and Sell Stock IV (Python; scale lane)."""


def max_profit(k, prices):
    n = len(prices)
    if n == 0 or k == 0:
        return 0
    if k >= n // 2:
        profit = 0
        for i in range(1, n):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]
        return profit

    neg = -1000000000
    buy = [neg] * (k + 1)
    sell = [0] * (k + 1)
    for d in range(n):
        price = prices[d]
        for t in range(1, k + 1):
            b = sell[t - 1] - price
            if b > buy[t]:
                buy[t] = b
            s = buy[t] + price
            if s > sell[t]:
                sell[t] = s
    return sell[k]


def main():
    n = 2000
    kmax = 50
    rounds = 5000
    prices = [0] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        prices[i] = (state >> 16) % 1000
    sink = 0
    for _ in range(rounds):
        state = (state * 1103515245 + 12345) & 2147483647
        k = 1 + state % kmax
        state = (state * 1103515245 + 12345) & 2147483647
        idx = state % n
        prices[idx] = (state >> 16) % 1000
        sink += max_profit(k, prices)
    print(sink)


main()
