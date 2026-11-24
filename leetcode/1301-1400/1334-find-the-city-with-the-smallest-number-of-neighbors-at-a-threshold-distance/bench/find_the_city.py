# LeetCode #1334 bench, Python mirror of the Kāra bench: the ★ arm on 10
# maps of 100 cities built once, then 30 passes, each setting one road's
# weight of every map and the threshold from the checksum so far,
# answering every map.


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


seed = 1334


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100
    maps = []
    for _ in range(10):
        edges = []
        for a in range(n):
            for b in range(a + 1, n):
                if next_random() % 2 == 0:
                    edges.append([a, b, 1 + next_random() % 10000])
        maps.append(edges)
    check = 0
    for p in range(30):
        threshold = 200 + check % 800
        for t in range(10):
            at = check % len(maps[t])
            maps[t][at][2] = 1 + check // 3 % 10000
            city = find_the_city(n, maps[t], threshold)
            check = (check * 31 + city + p) % 1000000007
    print(f"30 passes over 10 maps of 100 cities: checksum {check}")


main()
