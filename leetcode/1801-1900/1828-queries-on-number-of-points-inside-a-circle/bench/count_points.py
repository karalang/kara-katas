# LeetCode #1828: Queries on Number of Points Inside a Circle -- the bench in
# Python: the ★ arm over 200 calls on runs of 250 to 499 points and 250 to 499
# queries cut from one list of 1000 points and one of 1000 queries of radius 1
# to 500, built once, each run's start and lengths drawn from the checksum so
# far. Each call copies its runs, as the arm takes its lists by value.


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


points = []
for _ in range(1000):
    x = next_random() % 501
    points.append([x, next_random() % 501])
queries = []
for _ in range(1000):
    x = next_random() % 501
    y = next_random() % 501
    queries.append([x, y, 1 + next_random() % 500])
check = 0
for call in range(200):
    start = (check + call) % 500
    n = 250 + (check * 7 + call) % 250
    m = 250 + (check * 13 + call) % 250
    answer = count_points([p[:] for p in points[start:start + n]], [q[:] for q in queries[start:start + m]])
    for c in answer:
        check = (check * 31 + c) % 1000000007
print(f"200 calls: checksum {check}")
