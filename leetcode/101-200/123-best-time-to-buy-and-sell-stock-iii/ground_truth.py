#!/usr/bin/env python3
"""Ground-truth check for LeetCode #123 — max profit with at most TWO transactions, three ways.

  1. Four-state relaxation — buy1/sell1/buy2/sell2 in one pass (`max_profit.kara`, the ★).
  2. General at-most-k DP — the O(n·k) table specialised to k=2, an independent formulation.
  3. Brute force — the exact best over ALL ≤2-transaction buy/sell schedules (feasible only for short
     series, the definitional oracle).

Checked on many random series per length for lengths 1..11 (brute force caps the length), plus
four-state == general-k on longer series. Zero disagreements is the pass."""

import random


def four_state(prices):
    if not prices:
        return 0
    buy1, sell1, buy2, sell2 = -prices[0], 0, -prices[0], 0
    for p in prices[1:]:
        buy1 = max(buy1, -p)
        sell1 = max(sell1, buy1 + p)
        buy2 = max(buy2, sell1 - p)
        sell2 = max(sell2, buy2 + p)
    return sell2


def general_k(prices, k=2):
    n = len(prices)
    if n == 0:
        return 0
    # dp[t] = best profit using at most t transactions up to today.
    buy = [-prices[0]] * (k + 1)   # buy[t] = best balance after opening the t-th position
    sell = [0] * (k + 1)
    for p in prices[1:]:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - p)
            sell[t] = max(sell[t], buy[t] + p)
    return sell[k]


def brute(prices):
    n = len(prices)
    best = [0]

    def go(i, holding, done, profit):
        if profit > best[0]:
            best[0] = profit
        if i == n:
            return
        go(i + 1, holding, done, profit)                       # idle
        if holding:
            go(i + 1, False, done + 1, profit + prices[i])     # sell (completes a transaction)
        elif done < 2:
            go(i + 1, True, done, profit - prices[i])          # buy (only if < 2 done)

    go(0, False, 0, 0)
    return best[0]


def main():
    random.seed(123)
    fails = 0
    for length in range(1, 12):
        for _ in range(60):
            prices = [random.randint(1, 25) for _ in range(length)]
            a, b, c = four_state(prices), general_k(prices), brute(prices)
            if not (a == b == c):
                fails += 1
                if fails <= 5:
                    print(f"FAIL len={length}: four_state={a} general_k={b} brute={c} prices={prices}")
    for length in [100, 1000, 100000]:
        for _ in range(10):
            prices = [random.randint(1, 4096) for _ in range(length)]
            a, b = four_state(prices), general_k(prices)
            if a != b:
                fails += 1
                if fails <= 5:
                    print(f"FAIL len={length}: four_state={a} general_k={b}")
    if fails == 0:
        print("ground truth OK: four-state == general-k DP == brute force (0 disagreements)")
    else:
        print(f"GROUND TRUTH FAILED: {fails} disagreements")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
