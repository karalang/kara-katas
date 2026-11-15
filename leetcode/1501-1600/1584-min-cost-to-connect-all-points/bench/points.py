# LeetCode #1584 bench: the same Prim's algorithm with no edge list, in
# Python.

INF = 2**63 - 1


def min_cost_connect_points(points):
    n = len(points)
    nearest = [INF] * n
    inside = [False] * n
    nearest[0] = 0
    cost = 0
    for _ in range(n):
        nxt = -1
        for i in range(n):
            if not inside[i] and (nxt < 0 or nearest[i] < nearest[nxt]):
                nxt = i
        inside[nxt] = True
        cost += nearest[nxt]
        for i in range(n):
            if not inside[i]:
                d = abs(points[i][0] - points[nxt][0]) + abs(points[i][1] - points[nxt][1])
                nearest[i] = min(nearest[i], d)
    return cost


seed = 1584


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    problems = []
    for _ in range(100):
        seen = set()
        points = []
        while len(points) < 1000:
            x = (next_random() * 32768 + next_random()) % 2000001 - 1000000
            y = (next_random() * 32768 + next_random()) % 2000001 - 1000000
            if (x, y) not in seen:
                seen.add((x, y))
                points.append([x, y])
        problems.append(points)
    check = 0
    total = 0
    for points in problems:
        cost = min_cost_connect_points(points)
        total += cost
        check = mix(check, cost)
    print(f"100 problems of 1000 points: cost {total}, checksum {check}")


main()
