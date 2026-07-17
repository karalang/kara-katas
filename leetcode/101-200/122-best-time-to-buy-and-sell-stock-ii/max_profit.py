#!/usr/bin/env python3
"""LeetCode #122 — Python mirror of the greedy `max_profit.kara`.
Same algorithm: sum every positive consecutive gain. Produces byte-identical output to the Kara solver."""


def max_profit(prices):
    profit = 0
    for i in range(1, len(prices)):
        d = prices[i] - prices[i - 1]
        if d > 0:
            profit += d
    return profit


def main():
    print(max_profit([7, 1, 5, 3, 6, 4]))  # 7
    print(max_profit([1, 2, 3, 4, 5]))      # 4
    print(max_profit([7, 6, 4, 3, 1]))      # 0
    print(max_profit([5]))                  # 0


if __name__ == "__main__":
    main()
