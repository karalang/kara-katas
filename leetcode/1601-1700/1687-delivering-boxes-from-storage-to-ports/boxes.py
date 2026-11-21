# LeetCode #1687: Delivering Boxes from Storage to Ports -- mirrors
# boxes.kara, the ★ arm: the cheapest start of the last trip, kept in a
# monotone deque.
from collections import deque


def deliver(boxes, ports_count, max_boxes, max_weight):
    n = len(boxes)
    changes = [0] * n
    weight = [0] * (n + 1)
    for k in range(n):
        weight[k + 1] = weight[k] + boxes[k][1]
        if k > 0:
            changes[k] = changes[k - 1] + (1 if boxes[k][0] != boxes[k - 1][0] else 0)
    trips = [0] * (n + 1)
    starts = deque()
    for i in range(1, n + 1):
        j = i - 1
        cost = trips[j] - changes[j]
        while starts and trips[starts[-1]] - changes[starts[-1]] >= cost:
            starts.pop()
        starts.append(j)
        while starts and (i - starts[0] > max_boxes or weight[i] - weight[starts[0]] > max_weight):
            starts.popleft()
        front = starts[0]
        trips[i] = trips[front] - changes[front] + changes[i - 1] + 2
    return trips[n]


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, ports, limit, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = (seed.next() * 32768 + seed.next()) % most + 1
        ports_count = (seed.next() * 32768 + seed.next()) % ports + 1
        max_boxes = (seed.next() * 32768 + seed.next()) % limit + 1
        max_weight = (seed.next() * 32768 + seed.next()) % limit + 1
        boxes = []
        for _ in range(n):
            port = seed.next() % ports_count + 1
            weight = seed.next() % max_weight + 1
            boxes.append([port, weight])
        answer = deliver(boxes, ports_count, max_boxes, max_weight)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} problems of up to {most} boxes, {ports} ports, caps up to {limit}: {total} trips, checksum {check}")


def main():
    print(deliver([[1, 1], [2, 1], [1, 1]], 2, 3, 3))
    print(deliver([[1, 2], [3, 3], [3, 1], [3, 1], [2, 4]], 3, 3, 6))
    print(deliver([[1, 4], [1, 2], [2, 1], [2, 1], [3, 2], [3, 4]], 3, 6, 7))
    print(deliver([[1, 1]], 1, 1, 1))
    print(deliver([[5, 1], [5, 1], [5, 1], [5, 1]], 5, 4, 4))
    seed = Seed(1687)
    batch(3000, 10, 3, 5, seed)
    batch(300, 1000, 10, 50, seed)
    batch(10, 100000, 100000, 100000, seed)


main()
