# LeetCode #2034: Stock Price Fluctuation -- the ★ arm in Python, the same
# algorithm and workload as stock.kara.
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


def main():
    sessions = []
    for a in range(10):
        span = [1000000000, 100000, 1000, 1000000000, 50000][a % 5]
        top = [1000000000, 1000, 1000000000, 100, 1000000][a % 5]
        upd = a % 7 + 2
        ops = []
        for i in range(100000):
            if i == 0 or next_random() % 10 < upd:
                timestamp = (next_random() * 32768 + next_random()) % span + 1
                price = (next_random() * 32768 + next_random()) % top + 1
                ops.append((0, timestamp, price))
            else:
                ops.append((next_random() % 3 + 1, 0, 0))
        sessions.append(ops)
    runs = queries = check = 0
    for _ in range(15):
        for ops in sessions:
            stock = StockPrice()
            for kind, timestamp, price in ops:
                if kind == 0:
                    stock.update(timestamp, price)
                else:
                    if kind == 1:
                        answer = stock.current()
                    elif kind == 2:
                        answer = stock.maximum()
                    else:
                        answer = stock.minimum()
                    queries += 1
                    check = (check * 31 + answer % 1000000007 + kind) % 1000000007
            runs += 1
    print(f"{runs} sessions: {queries} queries, checksum {check}")


main()
