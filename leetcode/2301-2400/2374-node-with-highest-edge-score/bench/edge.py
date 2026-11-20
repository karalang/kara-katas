# LeetCode #2374: Node With Highest Edge Score -- the bench, the ★ arm in
# Python: each node adds its label to the score of the node its edge
# points to, and the answer is the highest score's node, the smallest on
# a tie.


def edge_score(edges):
    n = len(edges)
    score = [0] * n
    for i in range(n):
        score[edges[i]] += i
    best = 0
    for v in range(1, n):
        if score[v] > score[best]:
            best = v
    return best


SEED = [2374]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # graph a: 10^5 nodes, each edge to one of the first 4^(a + 1) nodes
    # (at most all of them), another node than its own
    n = 100000
    graphs = []
    width = 4
    for _ in range(10):
        edges = []
        for i in range(n):
            hi = next_random()
            e = (hi * 32768 + next_random()) % min(width, n)
            edges.append((e + 1) % n if e == i else e)
        graphs.append(edges)
        width *= 4
    check = 0
    for p in range(50):
        for edges in graphs:
            check = (check * 31 + edge_score(edges) + p) % 1000000007
    print(f"50 passes over 10 graphs of 10^5 nodes: checksum {check}")


main()
