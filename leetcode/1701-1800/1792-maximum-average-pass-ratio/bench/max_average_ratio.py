# LeetCode #1792: Maximum Average Pass Ratio -- the bench in Python: the ★
# arm over 200 random lists of 1000 classes built once, 4000 calls.
import heapq
import math


def gain(p, t):
    return (p + 1) / (t + 1) - p / t


def max_average_ratio(classes, extra_students):
    n = len(classes)
    passing = [c[0] for c in classes]
    total = [c[1] for c in classes]
    queue = [(-gain(passing[i], total[i]), -i) for i in range(n)]
    heapq.heapify(queue)
    for _ in range(extra_students):
        _, i = heapq.heappop(queue)
        i = -i
        passing[i] += 1
        total[i] += 1
        heapq.heappush(queue, (-gain(passing[i], total[i]), -i))
    s = 0.0
    for i in range(n):
        s += passing[i] / total[i]
    return s / n


seed = 1792


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(200):
        classes = []
        for _ in range(1000):
            t = 1 + next_random() % 1000
            p = 1 + next_random() % t
            classes.append([p, t])
        lists.append(classes)
    check = 0
    for call in range(4000):
        classes = lists[(check + call) % 200]
        extra = 1 + check % 1000
        r = max_average_ratio(classes, extra)
        check = (check * 31 + math.floor(r * 100000.0 + 0.5)) % 1000000007
    print(f"4000 calls over 200 lists of 1000 classes: checksum {check}")


main()
