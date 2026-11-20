# LeetCode #2360: Longest Cycle in a Graph -- the bench, the ★ arm in
# Python: each node stamped with the time it is first visited, and a walk
# that reaches a node stamped since it began has closed a cycle as long as
# the time between the two visits.


def longest_cycle(edges):
    n = len(edges)
    stamp = [-1] * n
    time = 0
    best = -1
    for start in range(n):
        began = time
        node = start
        while node != -1 and stamp[node] == -1:
            stamp[node] = time
            time += 1
            node = edges[node]
        if node != -1 and stamp[node] >= began:
            best = max(best, time - stamp[node])
    return best


SEED = [2360]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    # graph a: 10^5 nodes shuffled into one line, cut into pieces with a
    # chance of 1 in 2^(a + 4) at each link; each piece's last node points
    # back to its first with a chance of 1 in 2, and otherwise at a random
    # node
    n = 100000
    graphs = []
    for a in range(10):
        order = list(range(n))
        for i in range(n - 1, 0, -1):
            j = wide_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        cut = 1 << (a + 4)
        edges = [-1] * n
        first = 0
        for i in range(n):
            if i == n - 1 or next_random() % cut == 0:
                target = order[first] if next_random() % 2 == 0 else wide_random() % n
                if target != order[i]:
                    edges[order[i]] = target
                first = i + 1
            else:
                edges[order[i]] = order[i + 1]
        graphs.append(edges)
    check = 0
    for p in range(50):
        for edges in graphs:
            check = (check * 31 + longest_cycle(edges) + 2 + p) % 1000000007
    print(f"50 passes over 10 graphs of 10^5 nodes: checksum {check}")


main()
