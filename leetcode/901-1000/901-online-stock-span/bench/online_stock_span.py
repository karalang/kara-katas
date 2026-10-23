# LeetCode #901: Online Stock Span -- bench program, Python.
#
# The stack of prices and their spans over 1,000,000 prices built once, a
# random walk between 1 and 10^5 taking steps of -50 to 50. Each round
# gives every price to a fresh spanner, folds the spans into a checksum
# and changes one price.


class StockSpanner:
    def __init__(self):
        self.prices = []
        self.spans = []

    def next(self, price):
        span = 1
        while len(self.prices) > 0 and self.prices[-1] <= price:
            span += self.spans[-1]
            self.prices.pop()
            self.spans.pop()
        self.prices.append(price)
        self.spans.append(span)
        return span


seed = 901


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    days = 1000000
    rounds = 50
    prices = []
    p = 50000
    for _ in range(days):
        p = min(max(p + next_random() % 101 - 50, 1), 100000)
        prices.append(p)
    check = 0
    total = 0
    for rnd in range(rounds):
        s = StockSpanner()
        for d in range(days):
            span = s.next(prices[d])
            total += span
            check = (check * 31 + span) % 1000000007
        prices[rnd * 7919 % days] = 1 + next_random() % 100000
    print(f"{rounds} rounds over {days} prices: spans summing to {total}, checksum {check}")


main()
