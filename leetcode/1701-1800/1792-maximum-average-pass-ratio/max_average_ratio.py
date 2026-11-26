# LeetCode #1792: Maximum Average Pass Ratio -- the ★ arm in Python: each
# student to the class whose ratio it raises most, a heap of the gains.
import heapq


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


def fixed(r):
    import math
    return math.floor(r * 100000.0 + 0.5)


def random_classes(n, most):
    classes = []
    for _ in range(n):
        t = 1 + next_random() % most
        p = 1 + next_random() % t
        classes.append([p, t])
    return classes


def main():
    print(f"{max_average_ratio([[1, 2], [3, 5], [2, 2]], 2):.5f} {max_average_ratio([[2, 4], [3, 9], [4, 5], [2, 10]], 4):.5f}")
    print(f"{max_average_ratio([[3, 3]], 4):.5f} {max_average_ratio([[1, 2]], 1):.5f} {max_average_ratio([[1, 3], [1, 3]], 3):.5f} {max_average_ratio([[5, 5], [1, 5]], 10):.5f}")
    one = [[1, 100000] for _ in range(100000)]
    wide = random_classes(100000, 100000)
    print(f"the most: {max_average_ratio(one, 100000):.5f} {max_average_ratio(wide, 100000):.5f}")
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 12
        classes = random_classes(n, 20)
        extra = 1 + next_random() % 30
        check = (check * 31 + fixed(max_average_ratio(classes, extra))) % 1000000007
    print(f"2000 random cases: checksum {check}")


main()
