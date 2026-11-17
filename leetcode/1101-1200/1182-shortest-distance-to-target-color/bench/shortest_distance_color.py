# LeetCode #1182: Shortest Distance to Target Color -- the ★ arm in Python:
# a nearest-distance table per colour, filled from each side, then a lookup
# a query.


def shortest_distance_color(colors, queries):
    n = len(colors)
    far = n + 1
    nearest = []
    for c in range(1, 4):
        dist = [far] * n
        last = -1
        for i in range(n):
            if colors[i] == c:
                last = i
            if last >= 0:
                dist[i] = i - last
        last = -1
        for i in range(n - 1, -1, -1):
            if colors[i] == c:
                last = i
            if last >= 0 and last - i < dist[i]:
                dist[i] = last - i
        nearest.append(dist)
    answer = []
    for q in queries:
        d = nearest[q[1] - 1][q[0]]
        answer.append(-1 if d == far else d)
    return answer


seed = 1182


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays, asks = [], []
    for _ in range(4):
        arrays.append([3 if next_random() % 997 == 0 else 1 + next_random() % 2 for _ in range(50000)])
        asks.append([[next_random() % 50000, 1 + next_random() % 3] for _ in range(50000)])
    rounds = 40
    check = 0
    for rnd in range(rounds):
        for a in range(4):
            for d in shortest_distance_color(arrays[a], asks[a]):
                check = (check * 131 + d + 2 + rnd) % 1000000007
    print(f"{rounds} rounds of 4 arrays of 50000 queries: checksum {check}")


main()
