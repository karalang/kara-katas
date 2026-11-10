# LeetCode #2054: Two Best Non-Overlapping Events -- Python mirror of the
# ★ arm's benchmark (two.kara): the same 50 sets of 100000 events, the
# same sort by start, best value from each event on, and binary search for
# each event.
from bisect import bisect_right

seed = 2054


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def max_two_events(events):
    events = sorted(events)
    n = len(events)
    starts = [e[0] for e in events]
    best_from = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        best_from[i] = max(best_from[i + 1], events[i][2])
    best = 0
    for _, end, value in events:
        best = max(best, value + best_from[bisect_right(starts, end)])
    return best


def main():
    total = check = 0
    for t in range(50):
        longest = [1000, 1000000, 100000000, 500000000][t % 4]
        span = 1000000000 - longest
        events = []
        for _ in range(100000):
            start = wide() % span + 1
            end = start + wide() % longest
            value = wide() % 1000000 + 1
            events.append((start, end, value))
        best = max_two_events(events)
        total += best
        check = (check * 31 + best) % 1000000007
    print(f"50 sets: sum {total}, checksum {check}")


main()
