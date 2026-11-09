# LeetCode #2034: Stock Price Fluctuation -- a Python mirror of the ★ arm
# (stock.kara): a dict of prices, the latest timestamp, and two heaps of
# (price, timestamp) records with stale ones discarded at query time.
import heapq


class StockPrice:
    def __init__(self):
        self.prices = {}
        self.latest = 0
        self.highs = []
        self.lows = []

    def update(self, timestamp, price):
        self.prices[timestamp] = price
        self.latest = max(self.latest, timestamp)
        heapq.heappush(self.highs, (-price, -timestamp))
        heapq.heappush(self.lows, (price, timestamp))

    def current(self):
        return self.prices[self.latest]

    def maximum(self):
        while True:
            price, timestamp = self.highs[0]
            if self.prices[-timestamp] == -price:
                return -price
            heapq.heappop(self.highs)

    def minimum(self):
        while True:
            price, timestamp = self.lows[0]
            if self.prices[timestamp] == price:
                return price
            heapq.heappop(self.lows)


seed = 2034


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def replay(ops):
    stock = StockPrice()
    answers = []
    for kind, timestamp, price in ops:
        if kind == 0:
            stock.update(timestamp, price)
        elif kind == 1:
            answers.append(stock.current())
        elif kind == 2:
            answers.append(stock.maximum())
        else:
            answers.append(stock.minimum())
    return answers


def play(count, span, top, upd):
    stock = StockPrice()
    queries = check = 0
    for i in range(count):
        if i == 0 or next_random() % 10 < upd:
            timestamp = (next_random() * 32768 + next_random()) % span + 1
            price = (next_random() * 32768 + next_random()) % top + 1
            stock.update(timestamp, price)
        else:
            kind = next_random() % 3 + 1
            if kind == 1:
                answer = stock.current()
            elif kind == 2:
                answer = stock.maximum()
            else:
                answer = stock.minimum()
            queries += 1
            check = (check * 31 + answer % 1000000007 + kind) % 1000000007
    return queries, check


def main():
    examples = [
        [(0, 1, 10), (0, 2, 5), (1, 0, 0), (2, 0, 0), (0, 1, 3), (2, 0, 0), (0, 4, 2), (3, 0, 0)],
        [(0, 7, 4), (1, 0, 0), (2, 0, 0), (3, 0, 0)],
        [(0, 5, 9), (0, 5, 1), (2, 0, 0), (3, 0, 0), (1, 0, 0)],
        [(0, 3, 8), (0, 1, 2), (1, 0, 0), (0, 2, 8), (0, 3, 1), (2, 0, 0), (1, 0, 0)],
        [(0, 1, 1000000000), (0, 1000000000, 1), (2, 0, 0), (3, 0, 0), (1, 0, 0), (0, 1000000000, 1000000000), (3, 0, 0)],
        [(0, 2, 6), (0, 1, 6), (0, 2, 3), (2, 0, 0), (3, 0, 0), (0, 1, 3), (2, 0, 0), (3, 0, 0)],
    ]
    for ops in examples:
        print(f"{ops} -> {replay(ops)}")
    queries = check = 0
    for _ in range(3000):
        count = next_random() % 30 + 1
        span = next_random() % 20 + 1
        top = next_random() % 50 + 1
        upd = next_random() % 9 + 1
        q, c = play(count, span, top, upd)
        queries += q
        check = (check * 31 + c) % 1000000007
    print(f"3000 small sessions: {queries} queries, checksum {check}")
    queries = check = 0
    for a in range(5):
        span = [1000000000, 100, 1000000000, 10, 50000][a]
        top = [1000000000, 1000000000, 5, 1000000000, 1000][a]
        upd = [5, 5, 8, 2, 9][a]
        q, c = play(100000, span, top, upd)
        queries += q
        check = (check * 31 + c) % 1000000007
    print(f"5 sessions of 100000 operations: {queries} queries, checksum {check}")


main()
