# LeetCode #1751: Maximum Number of Events That Can Be Attended II --
# mirrors events.kara (the ★ arm): sorted by end, one layer of k at a time.
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
    return next_random() * 32768 + next_random()


def batch(count, most, days, span, top, most_k):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        events = []
        for _ in range(n):
            start = wide() % days + 1
            end = min(start + next_random() % span, days)
            value = wide() % top + 1
            events.append([start, end, value])
        k = next_random() % most_k + 1
        answer = max_value(events, k)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} problems of up to {most} events in {days} days: values add to {total}, checksum {check}")


print(max_value([[1, 2, 4], [3, 4, 3], [2, 3, 1]], 2))
print(max_value([[1, 2, 4], [3, 4, 3], [2, 3, 10]], 2))
print(max_value([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]], 3))
print(max_value([[5, 9, 1000000]], 1))
print(max_value([[1, 3, 5], [3, 5, 6]], 2))
print(max_value([[1, 1, 7], [2, 2, 8]], 9))
batch(3000, 8, 12, 4, 10, 4)
batch(300, 1000, 1000000000, 1000000, 1000000, 1000)
batch(5, 100000, 1000000000, 100000, 1000000, 10)
