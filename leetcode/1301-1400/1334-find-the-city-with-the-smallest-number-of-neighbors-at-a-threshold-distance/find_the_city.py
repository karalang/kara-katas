# LeetCode #1334: Find the City With the Smallest Number of Neighbors at a
# Threshold Distance -- Python mirror of the ★ arm: Floyd-Warshall, then
# each city's count within the threshold, the later city on a tie.


def find_the_city(n, edges, distance_threshold):
    far = 1000000000
    dist = [[far] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for a, b, w in edges:
        dist[a][b] = w
        dist[b][a] = w
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    best = 0
    fewest = n + 1
    for i in range(n):
        near = sum(1 for j in range(n) if j != i and dist[i][j] <= distance_threshold)
        if near <= fewest:
            fewest = near
            best = i
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, percent, heaviest):
    edges = []
    for a in range(n):
        for b in range(a + 1, n):
            if next_random() % 100 < percent:
                edges.append([a, b, 1 + next_random() % heaviest])
    return edges


def main():
    global seed
    a = find_the_city(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4)
    b = find_the_city(5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2)
    print(f"{a} {b} {find_the_city(2, [], 1)} {find_the_city(2, [[0, 1, 5]], 4)}")
    seed = 1334
    full = draw(100, 100, 10000)
    line = [[i, i + 1, 1 + i % 7] for i in range(99)]
    print(f"100 cities: {len(full)} roads {find_the_city(100, full, 150)} {find_the_city(100, full, 500)}, a line {find_the_city(100, line, 3)}")
    check = 0
    for t in range(300):
        n = 2 + next_random() % 99 if t % 30 == 0 else 2 + next_random() % 9
        percent = 20 if t % 2 == 0 else 70
        heaviest = 10000 if t % 3 == 0 else 10
        edges = draw(n, percent, heaviest)
        threshold = 1 + next_random() % (2 * heaviest)
        check = (check * 131 + find_the_city(n, edges, threshold) + n) % 1000000007
    print(f"300 random maps: checksum {check}")


main()
