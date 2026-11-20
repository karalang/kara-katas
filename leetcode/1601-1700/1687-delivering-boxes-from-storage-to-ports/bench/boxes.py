# LeetCode #1687: Delivering Boxes from Storage to Ports -- the bench's
# Python mirror: the ★ arm on 50 random problems of 100000 boxes, all drawn
# first, each answered 20 times.
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


seed = 1687


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, size, rounds = 50, 100000, 20
    problems = []
    for _ in range(count):
        ports_count = next_random() % 100 + 1
        max_boxes = next_random() % 1000 + 1
        max_weight = next_random() % 99001 + 1000
        boxes = []
        for _ in range(size):
            port = next_random() % ports_count + 1
            weight = next_random() % 1000 + 1
            boxes.append([port, weight])
        problems.append((boxes, ports_count, max_boxes, max_weight))
    total = 0
    check = 0
    for r in range(rounds):
        for boxes, ports_count, max_boxes, max_weight in problems:
            answer = deliver(boxes, ports_count, max_boxes, max_weight)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {size} boxes, {rounds} rounds: {total} trips, checksum {check}")


main()
