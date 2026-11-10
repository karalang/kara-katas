# LeetCode #2054: Two Best Non-Overlapping Events -- Python mirror of the
# ★ arm (two.kara): the events sorted by start, the best value from each
# one on kept from the end, and each event paired with the best of those
# starting after it ends, found by binary search. Output is byte-identical
# to the Kāra arms.

from bisect import bisect_right


def max_two_events(events):
    events = sorted(events)
    n = len(events)
    starts = [e[0] for e in events]
    best_from = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        best_from[i] = max(best_from[i + 1], events[i][2])
    best = 0
    for _, end, value in events:
        nxt = bisect_right(starts, end)
        best = max(best, value + best_from[nxt])
    return best


# ---- test harness ---------------------------------------------------------

seed = 2054


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def draw(n, span, longest, worth):
    events = []
    for _ in range(n):
        start = wide() % span + 1
        end = start + wide() % longest
        value = wide() % worth + 1
        events.append((start, end, value))
    return events


def show(events):
    return "[" + ", ".join(f"({s}, {e}, {v})" for s, e, v in events) + "]"


def main():
    examples = [
        [(1, 3, 2), (4, 5, 2), (2, 4, 3)],
        [(1, 3, 2), (4, 5, 2), (1, 5, 5)],
        [(1, 5, 3), (1, 5, 1), (6, 6, 5)],
        [(1, 1, 4), (1, 1, 6)],
        [(1, 2, 4), (2, 3, 6)],
        [(1, 2, 4), (3, 3, 6)],
        [(5, 9, 1), (1, 4, 7), (10, 12, 2), (2, 11, 9)],
    ]
    for events in examples:
        print(f"{show(events)} -> {max_two_events(events)}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 29 + 2
        span = next_random() % 50 + 5
        longest = next_random() % 10 + 1
        best = max_two_events(draw(n, span, longest, 100))
        total += best
        check = (check * 31 + best) % 1000000007
    print(f"2000 sets: sum {total}, checksum {check}")
    total = check = 0
    for t in range(20):
        longest = [1000, 1000000, 100000000, 500000000][t % 4]
        best = max_two_events(draw(2000, 1000000000 - longest, longest, 1000000))
        total += best
        check = (check * 31 + best) % 1000000007
    print(f"20 sets of 2000: sum {total}, checksum {check}")


main()
