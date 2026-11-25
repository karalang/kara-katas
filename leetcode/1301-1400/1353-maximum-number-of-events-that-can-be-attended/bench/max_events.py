# LeetCode #1353 bench -- Python: a sweep over the days with a heap of the
# open events' last days.
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


def main():
    seed = 1353
    sets = []
    for _ in range(20):
        events = []
        for _ in range(10000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            start = 1 + (seed // 65536) % 10000
            seed = (seed * 1103515245 + 12345) % 2147483648
            events.append([start, start + (seed // 65536) % 30])
        sets.append(events)
    check = 0
    for r in range(600):
        k = check % 20
        at = (check // 20) % 10000
        start = 1 + (check // 7) % 10000
        sets[k][at] = [start, start + (check // 11) % 30]
        check = (check * 31 + max_events(sets[k]) + r) % 1000000007
    print(f"600 rounds over 20 sets of 10^4 events: checksum {check}")


main()
