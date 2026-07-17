#!/usr/bin/env python3
"""Ground-truth check for LeetCode #122 — max profit with unlimited transactions, three ways.

  1. Greedy — sum every positive consecutive gain (`max_profit.kara`, the ★).
  2. DP state machine — track the best cash-in-hand vs holding-a-share value each day; the standard
     O(n) recurrence, an independent formulation.
  3. Brute force — the exact best over ALL buy/sell decision sequences (feasible only for short
     series, the definitional oracle).

Checked on many random price series per length for lengths 1..12 (brute force caps the length), plus
greedy == DP on longer series. Zero disagreements is the pass."""

import random


def greedy(prices):
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))


def dp(prices):
    if not prices:
        return 0
    cash, hold = 0, -prices[0]
    for p in prices[1:]:
        cash = max(cash, hold + p)   # sell today (or stay in cash)
        hold = max(hold, cash - p)   # buy today (or keep holding)
    return cash


def brute(prices):
    n = len(prices)
    best = [0]

    def go(i, holding, profit):
        if i == n:
            if profit > best[0]:
                best[0] = profit
            return
        go(i + 1, holding, profit)                      # do nothing
        if holding:
            go(i + 1, False, profit + prices[i])        # sell
        else:
            go(i + 1, True, profit - prices[i])         # buy

    go(0, False, 0)
    return best[0]


def main():
    random.seed(122)
    fails = 0
    for length in range(1, 13):
        for _ in range(80):
            prices = [random.randint(1, 30) for _ in range(length)]
            g, d, b = greedy(prices), dp(prices), brute(prices)
            if not (g == d == b):
                fails += 1
                if fails <= 5:
                    print(f"FAIL len={length}: greedy={g} dp={d} brute={b} prices={prices}")
    for length in [100, 1000, 100000]:
        for _ in range(10):
            prices = [random.randint(1, 4096) for _ in range(length)]
            g, d = greedy(prices), dp(prices)
            if g != d:
                fails += 1
                if fails <= 5:
                    print(f"FAIL len={length}: greedy={g} dp={d}")
    if fails == 0:
        print("ground truth OK: greedy == DP state machine == brute force (0 disagreements)")
    else:
        print(f"GROUND TRUTH FAILED: {fails} disagreements")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
