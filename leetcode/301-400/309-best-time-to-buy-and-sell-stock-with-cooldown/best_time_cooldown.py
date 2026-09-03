"""LeetCode 309 - Best Time to Buy and Sell Stock with Cooldown.

Mirror of best_time_cooldown.kara: a three-state machine carried as three
rolling scalars.

    hold  best profit while holding stock at the end of day i
    sold  best profit having sold on day i        (tomorrow is a cooldown)
    rest  best profit holding nothing and free to buy

The cooldown lives entirely in `rest = max(rest, prev_sold)`: a sale on day
i-1 reaches `rest` only on day i, so a buy cannot see it until day i+1.
"""


def max_profit(prices: list[int]) -> int:
    n = len(prices)
    if n == 0:
        return 0
    hold, sold, rest = -prices[0], 0, 0
    for i in range(1, n):
        # Snapshot yesterday before any of the three is overwritten.
        prev_hold, prev_sold, prev_rest = hold, sold, rest
        hold = max(prev_hold, prev_rest - prices[i])
        sold = prev_hold + prices[i]
        rest = max(prev_rest, prev_sold)
    return max(sold, rest)


def report(prices: list[int]) -> None:
    body = ", ".join(str(v) for v in prices)
    print(f"[{body}] -> {max_profit(prices)}")


def main() -> None:
    # The example from the LeetCode statement: buy, sell, cooldown, buy, sell.
    report([1, 2, 3, 0, 2])
    # The second statement example.
    report([1])
    # Empty.
    report([])
    # Strictly decreasing — never profitable, answer 0.
    report([5, 4, 3, 2, 1])
    # Strictly increasing — one buy and one sell beats churning under cooldown.
    report([1, 2, 3, 4, 5])
    # A saw-tooth, where the cooldown actually costs something.
    report([1, 4, 1, 4, 1, 4])
    # Two clean humps separated by a trough.
    report([2, 8, 1, 9])
    # Flat prices — no profit anywhere.
    report([7, 7, 7, 7])
    # A single spike late.
    report([3, 3, 3, 100])
    # Negative prices are not in the statement's domain, but the recurrence is
    # defined over any integers, and every arm must still agree.
    report([-5, -1, -8, -2])


if __name__ == "__main__":
    main()
