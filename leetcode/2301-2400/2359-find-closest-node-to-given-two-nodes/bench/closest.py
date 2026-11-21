# LeetCode #2359: Find Closest Node to Given Two Nodes -- the bench, the ★
# arm in Python: each start's path walked for its distances, then every
# node both reach scanned for the least of the larger distance.


def distances(edges, start):
    dist = [-1] * len(edges)
    node = start
    d = 0
    while node != -1 and dist[node] == -1:
        dist[node] = d
        node = edges[node]
        d += 1
    return dist


def closest_meeting_node(edges, node1, node2):
    d1 = distances(edges, node1)
    d2 = distances(edges, node2)
    best = -1
    best_dist = -1
    for v in range(len(edges)):
        if d1[v] >= 0 and d2[v] >= 0:
            far = max(d1[v], d2[v])
            if best < 0 or far < best_dist:
                best = v
                best_dist = far
    return best


SEED = [2359]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    # graph a: 10^5 nodes shuffled into one line, each link cut with a
    # chance of 1 in 2^(a + 4), the last node linked back to the first
    # when a is odd; 20 random pairs of starts in each
    n = 100000
    graphs = []
    starts = []
    for a in range(10):
        order = list(range(n))
        for i in range(n - 1, 0, -1):
            j = wide_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        cut = 1 << (a + 4)
        edges = [-1] * n
        for i in range(n - 1):
            if next_random() % cut != 0:
                edges[order[i]] = order[i + 1]
        if a % 2 == 1:
            edges[order[n - 1]] = order[0]
        graphs.append(edges)
        starts.append([wide_random() % n for _ in range(40)])
    check = 0
    for p in range(10):
        for a in range(10):
            for j in range(20):
                m = closest_meeting_node(graphs[a], starts[a][2 * j], starts[a][2 * j + 1])
                check = (check * 31 + m + 2 + p) % 1000000007
    print(f"10 passes over 10 graphs of 10^5 nodes: checksum {check}")


main()
