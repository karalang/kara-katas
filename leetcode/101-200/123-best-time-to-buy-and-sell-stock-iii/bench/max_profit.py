#!/usr/bin/env python3
"""Benchmark workload — at-most-two-transactions DP, Best Time to Buy and Sell Stock III (Python mirror).
Same N, K, LCG, serial K-loop as max_profit.kara. Timed separately."""
def max_profit(prices):
    if not prices: return 0
    buy1, sell1, buy2, sell2 = -prices[0], 0, -prices[0], 0
    for i in range(1, len(prices)):
        p = prices[i]
        if -p > buy1: buy1 = -p
        if buy1 + p > sell1: sell1 = buy1 + p
        if sell1 - p > buy2: buy2 = sell1 - p
        if buy2 + p > sell2: sell2 = buy2 + p
    return sell2
def main():
    n = 2000000
    data = [0]*n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        data[i] = (state & 4095) + 1
    total = 0
    for _ in range(10):
        r = max_profit(data)
        total += r
        data[0] = ((data[0] + r) & 4095) + 1
    print(total)
if __name__ == "__main__":
    main()
