# LeetCode #2374: Node With Highest Edge Score -- the Python mirror of the
# ★ arm: each node adds its label to the score of the node its edge points
# to, and the answer is the highest score's node, the smallest on a tie.


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
    # LeetCode's two examples; two nodes; 10^5 nodes all pointing at node
    # 0, node 0 at node 1; 10^5 nodes each pointing at half its label;
    # 10^5 nodes each pointing at the next, around; then 2000 random
    # graphs of 2 to 40 nodes, each edge to any other node or, with a
    # chance of 1 in 2, to one of the first three
    print(edge_score([1, 0, 0, 0, 0, 7, 7, 5]))
    print(edge_score([2, 0, 0, 2]))
    print(edge_score([1, 0]))
    n = 100000
    star = [1 if i == 0 else 0 for i in range(n)]
    halves = [1 if i == 0 else i // 2 for i in range(n)]
    around = [(i + 1) % n for i in range(n)]
    print(f"{edge_score(star)} {edge_score(halves)} {edge_score(around)}")
    check = 0
    zero = 0
    for _ in range(2000):
        n = 2 + next_random() % 39
        edges = []
        for i in range(n):
            if next_random() % 2 == 0:
                e = next_random() % 3 % n
            else:
                e = next_random() % n
            if e == i:
                e = (e + 1) % n
            edges.append(e)
        t = edge_score(edges)
        check = (check * 31 + t) % 1000000007
        if t == 0:
            zero += 1
    print(f"2000 graphs: checksum {check}, {zero} with node 0 the answer")


main()
