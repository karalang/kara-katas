"""LeetCode #121: Best Time to Buy and Sell Stock — one-pass O(n).

Algorithmic mirror of one_pass.kara. Output format matches line-for-line so
the two can be diffed directly.
"""

from __future__ import annotations


def max_profit(prices: list[int]) -> int:
    # Walk once, tracking the minimum price seen so far. Best profit ending at
    # day k is prices[k] - min_so_far; the answer is the max over all k.
    if not prices:
        return 0
    min_price = prices[0]
    best = 0
    for p in prices[1:]:
        if p < min_price:
            min_price = p
        profit = p - min_price
        if profit > best:
            best = profit
    return best


def report(prices: list[int]) -> None:
    print(max_profit(prices))


def main() -> None:
    report([7, 1, 5, 3, 6, 4])  # expect: 5
    report([7, 6, 4, 3, 1])     # expect: 0
    report([5])                 # expect: 0


if __name__ == "__main__":
    main()
