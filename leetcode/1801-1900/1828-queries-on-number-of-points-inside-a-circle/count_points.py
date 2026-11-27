# LeetCode #1828: Queries on Number of Points Inside a Circle -- the ★ arm
# in Python


def count_points(points, queries):
    answer = []
    for x, y, r in queries:
        inside = 0
        for px, py in points:
            dx, dy = px - x, py - y
            if dx * dx + dy * dy <= r * r:
                inside += 1
        answer.append(inside)
    return answer


seed = 1828


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def pairs(k):
    out = []
    for _ in range(k):
        a = next_random() % 501
        out.append((a, next_random() % 501))
    return out


print(show(count_points([(1, 3), (3, 3), (5, 3), (2, 2)], [(2, 3, 1), (4, 3, 1), (1, 1, 2)])), show(count_points([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], [(1, 2, 2), (2, 2, 2), (4, 3, 2), (4, 3, 3)])))
edge = [(3, 4), (0, 5), (5, 0), (4, 4), (0, 0), (500, 500), (500, 500), (500, 500)]
print(show(count_points(edge, [(0, 0, 5), (0, 0, 1), (500, 500, 1), (0, 0, 500), (250, 250, 3)])))
many = pairs(500)
wide = [(a, b, 500) for a, b in pairs(500)]
narrow = [(a, b, 1) for a, b in pairs(500)]
print(f"the most: {sum(count_points(many, wide))} {sum(count_points(many, narrow))}")
check = 0
for _ in range(3000):
    n = 1 + next_random() % 8
    points = []
    for _ in range(n):
        a = next_random() % 11
        points.append((a, next_random() % 11))
    m = 1 + next_random() % 5
    queries = []
    for _ in range(m):
        a = next_random() % 11
        b = next_random() % 11
        queries.append((a, b, 1 + next_random() % 6))
    for c in count_points(points, queries):
        check = (check * 31 + c) % 1000000007
print(f"3000 random cases: checksum {check}")
