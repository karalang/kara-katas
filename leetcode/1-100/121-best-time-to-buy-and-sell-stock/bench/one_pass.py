"""Benchmark workload — one-pass O(n) Best Time to Buy and Sell Stock.

Algorithmic mirror of bench/one_pass.kara. See ../README.md § Benchmarks
for the choice of N / K and the deterministic LCG generator.
"""

from __future__ import annotations


def max_profit(prices: list[int]) -> int:
    n = len(prices)
    if n == 0:
        return 0
    min_price = prices[0]
    best = 0
    for i in range(1, n):
        p = prices[i]
        if p < min_price:
            min_price = p
        profit = p - min_price
        if profit > best:
            best = profit
    return best


def main() -> None:
    N = 2_000_000
    data: list[int] = []
    state = 12345
    for _ in range(N):
        state = (state * 1103515245 + 12345) & 2147483647
        data.append((state & 4095) + 1)

    sum_result = 0
    for _ in range(10):
        sum_result += max_profit(data)
    print(sum_result)


if __name__ == "__main__":
    main()
