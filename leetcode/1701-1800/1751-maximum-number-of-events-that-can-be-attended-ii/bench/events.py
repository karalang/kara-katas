# LeetCode #1751: Maximum Number of Events That Can Be Attended II -- the
# bench (events.kara in Python): sorted by end, one layer of k at a time.
from bisect import bisect_left


def max_value(events, k):
    events = sorted(events, key=lambda e: e[1])
    n = len(events)
    ends = [e[1] for e in events]
    before = [bisect_left(ends, e[0]) for e in events]
    previous = [0] * (n + 1)
    for _ in range(k):
        current = [0] * (n + 1)
        for i in range(n):
            current[i + 1] = max(current[i], previous[before[i]] + events[i][2])
        previous = current
    return previous[n]


seed = 1751


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


count, rounds, n, k = 10, 5, 100000, 10
problems = []
for _ in range(count):
    events = []
    for _ in range(n):
        start = wide() % 1000000000 + 1
        end = min(start + wide() % 100000000, 1000000000)
        value = wide() % 1000000 + 1
        events.append([start, end, value])
    problems.append(events)
total = 0
check = 0
for r in range(rounds):
    for events in problems:
        answer = max_value(events, k)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} problems of {n} events, k = {k}, {rounds} rounds: values add to {total}, checksum {check}")
