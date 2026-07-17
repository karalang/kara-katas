#!/usr/bin/env python3
"""Benchmark workload — greedy O(n) Best Time to Buy and Sell Stock II (Python mirror).
Same N, K, LCG generator as max_profit.kara. Timed separately; K matches the compiled mirrors."""
def max_profit(prices):
    profit = 0
    for i in range(1, len(prices)):
        d = prices[i] - prices[i - 1]
        if d > 0:
            profit += d
    return profit
def main():
    n = 2000000
    data = [0] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        data[i] = (state & 4095) + 1
    total = 0
    for _ in range(10):
        total += max_profit(data)
    print(total)
if __name__ == "__main__":
    main()
