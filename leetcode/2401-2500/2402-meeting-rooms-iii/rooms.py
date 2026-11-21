# LeetCode #2402: Meeting Rooms III -- the Python mirror of the ★ arm: a
# heap of free rooms and a heap of (end, room) for the rooms in use.

import heapq

seed = 2402


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def meetings(count, span, longest):
    starts = list(range(span))
    for i in range(count):
        hi = next_random()
        j = i + (hi * 32768 + next_random()) % (span - i)
        starts[i], starts[j] = starts[j], starts[i]
    out = []
    for i in range(count):
        s = starts[i]
        out.append((s, s + 1 + next_random() % longest))
    return out


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
    print(most_booked(2, [(0, 10), (1, 5), (2, 7), (3, 4)]))
    print(most_booked(3, [(1, 20), (2, 10), (3, 5), (4, 9), (6, 8)]))
    print(most_booked(1, [(5, 6), (0, 3), (1, 2)]))
    print(most_booked(3, [(i, 100) for i in range(10)]))
    print(most_booked(100, meetings(100000, 500000, 50)))
    print(most_booked(100, meetings(100000, 500000, 5000)))
    print(most_booked(7, meetings(20000, 100000, 100000)))
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 6
        count = 1 + next_random() % 40
        a = most_booked(n, meetings(count, 60, 1 + next_random() % 20))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
