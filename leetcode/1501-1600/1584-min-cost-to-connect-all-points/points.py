# LeetCode #1584: Min Cost to Connect All Points -- the Python mirror of the
# ★ arm: Prim's algorithm on the complete graph with no edge list, each
# point outside the tree keeping its distance to the nearest inside. O(n^2)

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


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, span):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        seen = set()
        points = []
        while len(points) < n:
            x = (next_random() * 32768 + next_random()) % (2 * span + 1) - span
            y = (next_random() * 32768 + next_random()) % (2 * span + 1) - span
            if (x, y) not in seen:
                seen.add((x, y))
                points.append([x, y])
        cost = min_cost_connect_points(points)
        total += cost
        check = mix(check, cost)
    print(f"{count} problems of up to {most} points: cost {total}, checksum {check}")


def show(rows):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in r) + "]" for r in rows) + "]"


def main():
    global seed
    examples = [
        [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]],
        [[3, 12], [-2, 5], [-4, 1]],
        [[0, 0]],
        [[0, 0], [1, 1], [1, 0], [-1, 1]],
        [[-1000000, -1000000], [1000000, 1000000]],
    ]
    for points in examples:
        print(f"{show(points)} -> {min_cost_connect_points(points)}")
    seed = 1584
    batch(3000, 6, 5)
    batch(300, 100, 1000)
    batch(3, 1000, 1000000)


main()
