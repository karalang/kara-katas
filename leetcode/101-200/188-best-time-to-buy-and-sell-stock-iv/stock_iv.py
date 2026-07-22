"""LeetCode 188 — Best Time to Buy and Sell Stock IV (Python mirror / oracle).

At most k transactions. Greedy sum of positive deltas when k >= n/2; otherwise an
O(n*k) DP over rolling buy[]/sell[] arrays. Mirrors the Kāra version.
"""


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
    for price in prices:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - price)
            sell[t] = max(sell[t], buy[t] + price)
    return sell[k]


def report(k, prices):
    print(max_profit(k, prices))


def main():
    report(2, [2, 4, 1])
    report(2, [3, 2, 6, 5, 0, 3])
    report(2, [1, 2, 3, 4, 5, 6])
    report(2, [6, 5, 4, 3, 2, 1])
    report(3, [1, 4, 2, 8, 3, 9, 1, 7])
    report(0, [1, 2, 4, 2])


main()
