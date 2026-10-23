# LeetCode #933: Number of Recent Calls -- bench: a queue of the recent
# pings. Mirrors recent_counter.kara, .c, .rs and go-seq/.

from collections import deque


class RecentCounter:
    def __init__(self):
        self.pings = deque()

    def ping(self, t):
        self.pings.append(t)
        while self.pings[0] < t - 3000:
            self.pings.popleft()
        return len(self.pings)


seed = 933


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 50
    count = 100
    length = 10000
    # count streams of length pings, each from 1 to gap after the one
    # before, gap from 1 to 600 a stream, built once
    streams = []
    for _ in range(count):
        gap = 1 + next_random() % 600
        times = []
        t = 0
        for _ in range(length):
            t += 1 + next_random() % gap
            times.append(t)
        streams.append(times)
    total = 0
    check = 0
    for r in range(rounds):
        # each round plays every stream into a new counter, starting from
        # a different one
        for i in range(count):
            counter = RecentCounter()
            last = 0
            for t in streams[(r + i) % count]:
                last = counter.ping(t)
                total += last
            check = (check * 1000003 + last) % 1000000007
    print(f"{rounds} rounds over {count} streams of {length} pings: answers summing to {total}, checksum {check}")


main()
