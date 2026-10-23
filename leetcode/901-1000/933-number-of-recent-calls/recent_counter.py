# LeetCode #933: Number of Recent Calls -- a queue of the recent pings
# (Python mirror).

from collections import deque


class RecentCounter:
    def __init__(self):
        self.pings = deque()

    def ping(self, t):
        self.pings.append(t)
        while self.pings[0] < t - 3000:
            self.pings.popleft()
        return len(self.pings)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def answers(times):
    counter = RecentCounter()
    return [counter.ping(t) for t in times]


def join(v):
    return ", ".join(str(x) for x in v)


def show(times):
    print(f"ping({join(times)}) -> {join(answers(times))}")


def random_times(length, gap):
    out = []
    t = 0
    for _ in range(length):
        t += 1 + (next_random() * 32768 + next_random()) % gap
        out.append(t)
    return out


def fold(got, sum_, check):
    for x in got:
        sum_ += x
        check = (check * 1000003 + x) % 1000000007
    return sum_, check


def main():
    global seed
    show([1, 100, 3001, 3002])
    show([1000000000])
    show([1, 3001, 6001])
    show([1, 3002, 6003])
    show([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    show([1, 2, 3, 3003, 3004, 3005])
    show([3000, 6000, 6001, 9001, 9002, 12002])
    seed = 933
    calls = 0
    sum_ = 0
    check = 0
    for _ in range(300):
        length = 1 + next_random() % 2000
        gap = 1 + next_random() % 6000
        got = answers(random_times(length, gap))
        calls += length
        sum_, check = fold(got, sum_, check)
    print(f"300 random streams: {calls} calls, answers summing to {sum_}, checksum {check}")
    dense = list(range(1, 10001))
    sparse = [1000 * i for i in range(1, 10001)]
    wide = random_times(10000, 100000)
    a, _ = fold(answers(dense), 0, 0)
    b, _ = fold(answers(sparse), 0, 0)
    c, _ = fold(answers(wide), 0, 0)
    print(f"10^4 pings: one a millisecond {a}, one every 1000 {b}, random gaps {c} (last ping at {wide[9999]})")


main()
