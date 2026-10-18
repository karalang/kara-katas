# LeetCode #742: Closest Leaf in a Binary Tree -- breadth first from k.
# Benchmark mirror of the Kara star arm: treat the tree as an undirected
# graph, each node's neighbours its children and its parent, and search
# outward from k a layer at a time; the first layer holding a leaf holds
# the nearest ones, and the smallest value of those is returned.


def find_closest_leaf(nodes, k):
    n = len(nodes)
    parent = []
    start = 0
    for i in range(n):
        parent.append(-1)
        if nodes[i][0] == k:
            start = i
    for i in range(n):
        if nodes[i][1] != -1:
            parent[nodes[i][1]] = i
        if nodes[i][2] != -1:
            parent[nodes[i][2]] = i
    seen = []
    for _ in range(n):
        seen.append(False)
    seen[start] = True
    layer = [start]
    while True:
        best = -1
        for x in layer:
            val, left, right = nodes[x]
            if left == -1 and right == -1 and (best == -1 or val < best):
                best = val
        if best != -1:
            return best
        nxt = []
        for x in layer:
            for y in (nodes[x][1], nodes[x][2], parent[x]):
                if y != -1 and not seen[y]:
                    seen[y] = True
                    nxt.append(y)
        layer = nxt


def main():
    seed = 742
    n = 1000

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    values = list(range(1, n + 1))
    for i in range(n):
        j = i + next_random() % (n - i)
        values[i], values[j] = values[j], values[i]
    nodes = [[values[0], -1, -1]]
    for i in range(1, n):
        while True:
            p = next_random() % i
            if next_random() % 2 == 0:
                if nodes[p][1] == -1:
                    nodes[p][1] = i
                    break
            elif nodes[p][2] == -1:
                nodes[p][2] = i
                break
        nodes.append([values[i], -1, -1])
    total = 0
    for _ in range(60):
        a = next_random() % n
        b = next_random() % n
        nodes[a][0], nodes[b][0] = nodes[b][0], nodes[a][0]
        for k in range(1, n + 1):
            total += find_closest_leaf(nodes, k)
    print(f"60 rounds of 1000 queries on a 1000-node tree: answers sum to {total}")


main()
