# LeetCode #2285: Maximum Total Importance of Roads -- the bench, the ★
# arm's Python mirror. The degrees sorted, the k-th smallest valued k.


def maximum_importance(n, roads):
    degree = [0] * n
    for a, b in roads:
        degree[a] += 1
        degree[b] += 1
    degree.sort()
    total = 0
    for i, d in enumerate(degree):
        total += d * (i + 1)
    return total


# ---- bench harness ---------------------------------------------------------

seed = 2285


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    graphs = []
    for _ in range(200):
        roads = []
        while len(roads) < 5000:
            a = (next_random() * 32768 + next_random()) % 5000
            b = (next_random() * 32768 + next_random()) % 5000
            if a != b:
                roads.append((a, b))
        graphs.append(roads)
    check = 0
    for _ in range(20):
        for roads in graphs:
            check = (check * 31 + maximum_importance(5000, roads)) % 1000000007
    print(f"20 passes over 200 graphs of 5000 cities: checksum {check}")


main()
