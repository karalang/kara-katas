# LeetCode #901: Online Stock Span -- Python mirror of the stack of prices
# and spans in online_stock_span.kara, with the same test harness.
#
# Keep a stack of the earlier prices not yet beaten, each with its span,
# the prices falling from the bottom up. A new price pops every price at
# or below it and takes over their spans; the price is pushed with the
# sum. O(1) a call amortized.


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


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def spans(prices):
    s = StockSpanner()
    return [s.next(p) for p in prices]


def join(v):
    return ", ".join(str(x) for x in v)


def show(prices):
    print(f"next({join(prices)}) -> {join(spans(prices))}")


# `len` prices: random from 1 to 10^5, from 1 to 5, or rising or falling
# by a random step with a random dip or bump
def random_prices(length, kind):
    out = []
    p = 50000
    for _ in range(length):
        if kind == 0:
            hi = next_random()
            lo = next_random()
            p = 1 + (hi * 32768 + lo) % 100000
        elif kind == 1:
            p = 1 + next_random() % 5
        else:
            step = next_random() % 20 - 4
            p = p + step if kind == 2 else p - step
            p = min(max(p, 1), 100000)
        out.append(p)
    return out


def checksum(got, check):
    for x in got:
        check = (check * 1000003 + x) % 1000000007
    return check


def main():
    global seed
    show([100, 80, 60, 70, 60, 75, 85])
    show([7])
    show([5, 5, 5, 5])
    show([1, 2, 3, 4, 5, 6])
    show([6, 5, 4, 3, 2, 1])
    show([3, 1, 2, 1, 3, 4])
    show([31, 41, 48, 59, 79])
    show([100000, 1, 100000, 1, 100000])
    # random cases of up to 1000 prices, a quarter of each kind
    seed = 901
    check = 0
    calls = 0
    span_sum = 0
    for c in range(300):
        length = 1 + next_random() % 1000
        got = spans(random_prices(length, c % 4))
        span_sum += sum(got)
        check = checksum(got, check)
        calls += length
    print(f"300 cases, {calls} calls, spans summing to {span_sum}: checksum {check}")
    # LeetCode's largest: 10^4 random prices, and 10^4 prices rising
    big = spans(random_prices(10000, 0))
    print(f"10000 random prices: spans summing to {sum(big)}, checksum {checksum(big, 0)}")
    rising = spans(random_prices(10000, 2))
    print(f"10000 rising prices: spans summing to {sum(rising)}, checksum {checksum(rising, 0)}")


main()
