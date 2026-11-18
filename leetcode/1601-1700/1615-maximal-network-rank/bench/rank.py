# LeetCode #1615: Maximal Network Rank -- the bench in Python, mirroring
# rank.kara: each city's degree and a table of which pairs share a road,
# then every pair's rank.


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


def main():
    seed = 1615

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    n = 100
    networks = []
    for _ in range(2000):
        roads = []
        for a in range(n):
            for b in range(a + 1, n):
                if next_random() % 4 == 0:
                    roads.append([a, b])
        networks.append(roads)
    check = roads_seen = 0
    for roads in networks:
        check = (check * 31 + maximal_network_rank(n, roads) + 1) % 1000000007
        roads_seen += len(roads)
    print(f"2000 networks of 100 cities: {roads_seen} roads, checksum {check}")


main()
