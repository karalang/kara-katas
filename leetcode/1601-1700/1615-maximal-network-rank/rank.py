# LeetCode #1615: Maximal Network Rank -- the Python mirror of rank.kara:
# each city's degree and a table of which pairs share a road, then every
# pair's rank.


def maximal_network_rank(n, roads):
    degree = [0] * n
    joined = [[False] * n for _ in range(n)]
    for a, b in roads:
        degree[a] += 1
        degree[b] += 1
        joined[a][b] = joined[b][a] = True
    best = 0
    for a in range(n):
        for b in range(a + 1, n):
            best = max(best, degree[a] + degree[b] - (1 if joined[a][b] else 0))
    return best


seed = 1615


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, roads_most):
    check = roads_seen = best = 0
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        a = next_random()
        wanted = min((a * 32768 + next_random()) % (roads_most + 1), n * (n - 1) // 2)
        taken = set()
        roads = []
        while len(roads) < wanted:
            a = next_random() % n
            b = next_random() % n
            if a != b and (min(a, b), max(a, b)) not in taken:
                taken.add((min(a, b), max(a, b)))
                roads.append([a, b])
        rank = maximal_network_rank(n, roads)
        check = mix(check, rank)
        best = max(best, rank)
        roads_seen += wanted
    print(f"{count} networks of up to {most} cities: {roads_seen} roads, highest rank {best}, checksum {check}")


examples = [
    (4, [[0, 1], [0, 3], [1, 2], [1, 3]]),
    (5, [[0, 1], [0, 3], [1, 2], [1, 3], [2, 3], [2, 4]]),
    (8, [[0, 1], [1, 2], [2, 3], [2, 4], [5, 6], [5, 7]]),
    (2, []),
    (2, [[1, 0]]),
    (5, [[0, 1], [0, 2], [0, 3], [0, 4]]),
]
for n, roads in examples:
    print(maximal_network_rank(n, roads))
batch(3000, 6, 8)
batch(300, 40, 600)
batch(30, 100, 50)
