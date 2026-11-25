# LeetCode #1353 -- Python mirror of the ★ arm: a sweep over the days with
# a heap of the open events' last days.
import heapq


def max_events(events):
    by_start = sorted(events, key=lambda e: e[0])
    ends = []
    nxt = 0
    attended = 0
    day = 1
    while nxt < len(by_start) or ends:
        if not ends and by_start[nxt][0] > day:
            day = by_start[nxt][0]
        while nxt < len(by_start) and by_start[nxt][0] == day:
            heapq.heappush(ends, by_start[nxt][1])
            nxt += 1
        while ends and ends[0] < day:
            heapq.heappop(ends)
        if ends:
            heapq.heappop(ends)
            attended += 1
        day += 1
    return attended


seed = [1353]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_events(n, days, span):
    events = []
    for _ in range(n):
        start = 1 + next_random() % days
        end = min(start + next_random() % span, 100000)
        events.append([start, end])
    return events


def main():
    e1 = max_events([[1, 2], [2, 3], [3, 4]])
    e2 = max_events([[1, 2], [2, 3], [3, 4], [1, 2]])
    one = max_events([[5, 5]])
    same = max_events([[7, 7], [7, 7], [7, 7]])
    last = [[100000, 100000] for _ in range(100000)]
    whole = [[1, 100000] for _ in range(100000)]
    rnd = random_events(100000, 100000, 50)
    print(e1, e2, one, same, max_events(last), max_events(whole), max_events(rnd))
    total = 0
    check = 0
    for c in range(2000):
        n = 1 + next_random() % (300 if c % 10 == 0 else 12)
        days = 10 if c % 2 == 0 else 1000
        span = 1 if c % 3 == 0 else 5 if c % 3 == 1 else 100
        got = max_events(random_events(n, days, span))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random sets: {total} events attended in all, checksum {check}")


main()
