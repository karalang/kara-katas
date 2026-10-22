# Benchmark for #850: Rectangle Area II -- Python twin of the Kāra
# segment-tree arm (a sweep line over a segment tree).
from bisect import bisect_left
import sys

sys.setrecursionlimit(10000)


def update(ys, count, length, node, lo, hi, a, b, delta):
    if b <= lo or hi <= a:
        return
    if a <= lo and hi <= b:
        count[node] += delta
    else:
        mid = (lo + hi) // 2
        update(ys, count, length, 2 * node, lo, mid, a, b, delta)
        update(ys, count, length, 2 * node + 1, mid, hi, a, b, delta)
    if count[node] > 0:
        length[node] = ys[hi] - ys[lo]
    elif hi - lo == 1:
        length[node] = 0
    else:
        length[node] = length[2 * node] + length[2 * node + 1]


def rectangle_area(rectangles):
    ys = []
    events = []
    for r in rectangles:
        ys.append(r[1])
        ys.append(r[3])
        events.append((r[0], 1, r[1], r[3]))
        events.append((r[2], -1, r[1], r[3]))
    ys = sorted(set(ys))
    events.sort()
    segments = len(ys) - 1
    count = [0] * (4 * len(ys))
    length = [0] * (4 * len(ys))
    area = 0
    prev_x = 0
    for x, delta, y1, y2 in events:
        area += length[1] * (x - prev_x)
        prev_x = x
        if segments > 0:
            update(ys, count, length, 1, 0, segments, bisect_left(ys, y1), bisect_left(ys, y2), delta)
    return area % 1000000007


seed = 850


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 8000
    n = 200
    limit = 1000000000
    sets = []
    for g in range(count):
        size = limit >> (g % 8)
        rectangles = []
        for _ in range(n):
            a = (next_random() * 32768 + next_random()) % (size + 1)
            b = (next_random() * 32768 + next_random()) % (size + 1)
            c = (next_random() * 32768 + next_random()) % (size + 1)
            d = (next_random() * 32768 + next_random()) % (size + 1)
            rectangles.append([min(a, b), min(c, d), max(a, b), max(c, d)])
        sets.append(rectangles)
    total = 0
    checksum = 0
    for round_ in range(rounds):
        a = rectangle_area(sets[round_ % count])
        total += a
        checksum = (checksum * 31 + a) % 1000000007
    print(f"{rounds} rounds of {count} sets: areas sum to {total}, checksum {checksum}")


main()
