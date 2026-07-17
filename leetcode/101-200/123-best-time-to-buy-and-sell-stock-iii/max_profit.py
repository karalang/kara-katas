#!/usr/bin/env python3
"""LeetCode #123 — Python mirror of the four-state `max_profit.kara`.
Same algorithm: relax buy1/sell1/buy2/sell2 across one pass. Byte-identical output to the Kara solver."""


def max_profit(prices):
    if not prices:
        return 0
    buy1, sell1, buy2, sell2 = -prices[0], 0, -prices[0], 0
    for i in range(1, len(prices)):
        p = prices[i]
        if -p > buy1:
            buy1 = -p
        if buy1 + p > sell1:
            sell1 = buy1 + p
        if sell1 - p > buy2:
            buy2 = sell1 - p
        if buy2 + p > sell2:
            sell2 = buy2 + p
    return sell2


def main():
    print(max_profit([3, 3, 5, 0, 0, 3, 1, 4]))  # 6
    print(max_profit([1, 2, 3, 4, 5]))            # 4
    print(max_profit([7, 6, 4, 3, 1]))            # 0
    print(max_profit([5]))                        # 0


if __name__ == "__main__":
    main()
