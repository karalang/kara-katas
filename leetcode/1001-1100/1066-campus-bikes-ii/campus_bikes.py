# LeetCode #1066: Campus Bikes II -- the Python mirror of campus_bikes.kara
# (the ★ arm): the best total for each set of bikes taken, the workers
# taking them in order, over every set built up one bike at a time.


def assign_bikes(workers, bikes):
    n, m = len(workers), len(bikes)
    INF = float("inf")
    best = [INF] * (1 << m)
    best[0] = 0
    answer = INF
    for mask in range(1 << m):
        if best[mask] == INF:
            continue
        w = bin(mask).count("1")
        if w == n:
            answer = min(answer, best[mask])
            continue
        for b in range(m):
            if mask & (1 << b) == 0:
                d = abs(workers[w][0] - bikes[b][0]) + abs(workers[w][1] - bikes[b][1])
                nxt = mask | (1 << b)
                best[nxt] = min(best[nxt], best[mask] + d)
    return answer


seed = 1066


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_points(n, side, taken):
    points = []
    while len(points) < n:
        p = (next_random() % side, next_random() % side)
        if p not in taken:
            taken.append(p)
            points.append(p)
    return points


def show(points):
    return "[" + ", ".join(f"({x}, {y})" for x, y in points) + "]"


def main():
    examples = [
        ([(0, 0), (2, 1)], [(1, 2), (3, 3)]),
        ([(0, 0), (1, 1), (2, 0)], [(1, 0), (2, 2), (2, 1)]),
        ([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], [(0, 999), (1, 999), (2, 999), (3, 999), (4, 999)]),
        ([(5, 5)], [(5, 6)]),
        ([(0, 0)], [(9, 9), (3, 4), (1, 1)]),
        ([(0, 0), (10, 10)], [(10, 9), (0, 1)]),
        ([(0, 0), (0, 2)], [(0, 1), (100, 100), (0, 3)]),
    ]
    for workers, bikes in examples:
        print(f"{show(workers)} {show(bikes)} -> {assign_bikes(workers, bikes)}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 4 + 1
        m = n + next_random() % (7 - n)
        taken = []
        workers = random_points(n, 10, taken)
        bikes = random_points(m, 10, taken)
        answer = assign_bikes(workers, bikes)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"2000 problems of 1 to 4 workers, 1 to 6 bikes: sum {total}, checksum {check}")
    total = check = 0
    for _ in range(100):
        n = next_random() % 8 + 1
        m = n + next_random() % (11 - n)
        taken = []
        workers = random_points(n, 1000, taken)
        bikes = random_points(m, 1000, taken)
        answer = assign_bikes(workers, bikes)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"100 problems of 1 to 8 workers, 1 to 10 bikes: sum {total}, checksum {check}")
    taken = []
    workers = random_points(10, 1000, taken)
    bikes = random_points(10, 1000, taken)
    print(f"10 and 10 at random: {assign_bikes(workers, bikes)}")
    print(f"10 and 10 on a line: {assign_bikes([(i * 10, 0) for i in range(10)], [(i * 10 + 5, 0) for i in range(10)])}")
    print(f"10 and 10 shifted: {assign_bikes([(i * 100, 500) for i in range(10)], [((i * 100 + 160) % 1000, 499 - i) for i in range(10)])}")


main()
