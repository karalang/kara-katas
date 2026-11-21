# LeetCode #2402: Meeting Rooms III -- the bench, the ★ arm in Python: a
# heap of free rooms and one of (end, room) for the rooms in use, over the
# meetings sorted by start.

import heapq

seed = 2402


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def most_booked(n, meetings):
    order = sorted(meetings)
    free = list(range(n))
    heapq.heapify(free)
    busy = []
    count = [0] * n
    for start, end in order:
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(free, room)
        if free:
            room = heapq.heappop(free)
            count[room] += 1
            heapq.heappush(busy, (end, room))
        else:
            at, room = heapq.heappop(busy)
            count[room] += 1
            heapq.heappush(busy, (at + end - start, room))
    best = 0
    for room in range(1, n):
        if count[room] > count[best]:
            best = room
    return best


def main():
    cases = []
    for c in range(10):
        starts = list(range(500000))
        for i in range(100000):
            hi = next_random()
            j = i + (hi * 32768 + next_random()) % (500000 - i)
            starts[i], starts[j] = starts[j], starts[i]
        cases.append([(starts[i], starts[i] + 1 + next_random() % (1 + 500 * c)) for i in range(100000)])
    check = 0
    for p in range(10):
        for meetings in cases:
            check = (check * 31 + most_booked(100, meetings) + p) % 1000000007
    print(f"10 passes over 10 cases of 10^5 meetings in 100 rooms: checksum {check}")


main()
