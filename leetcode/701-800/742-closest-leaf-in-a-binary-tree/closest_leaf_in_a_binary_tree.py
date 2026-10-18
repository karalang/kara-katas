# LeetCode #742: Closest Leaf in a Binary Tree -- breadth first from k.
# Mirror of the Kara star arm: treat the tree as an undirected graph,
# each node's neighbours its children and its parent, and search
# outward from k a layer at a time; the first layer holding a leaf
# holds the nearest ones, and the smallest value of those is returned.

NULL = -1000000007


def find_closest_leaf(nodes, k):
    n = len(nodes)
    parent = [-1] * n
    start = 0
    for i in range(n):
        if nodes[i][0] == k:
            start = i
    for i in range(n):
        if nodes[i][1] != -1:
            parent[nodes[i][1]] = i
        if nodes[i][2] != -1:
            parent[nodes[i][2]] = i
    seen = [False] * n
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


# ---- test harness ---------------------------------------------------------

def build(vals):
    nodes = [[vals[0], -1, -1]]
    queue = [0]
    head = 0
    i = 1
    while head < len(queue) and i < len(vals):
        cur = queue[head]
        head += 1
        if vals[i] != NULL:
            nodes.append([vals[i], -1, -1])
            nodes[cur][1] = len(nodes) - 1
            queue.append(len(nodes) - 1)
        i += 1
        if i < len(vals) and vals[i] != NULL:
            nodes.append([vals[i], -1, -1])
            nodes[cur][2] = len(nodes) - 1
            queue.append(len(nodes) - 1)
        i += 1
    return nodes


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(vals, k):
    text = "[" + ", ".join("null" if v == NULL else str(v) for v in vals) + "]"
    print(f"{text}, k = {k} -> {find_closest_leaf(build(vals), k)}")


def random_tree(seed, n):
    values = list(range(1, n + 1))
    for i in range(n):
        j = i + next_random(seed) % (n - i)
        values[i], values[j] = values[j], values[i]
    nodes = [[values[0], -1, -1]]
    for i in range(1, n):
        while True:
            p = next_random(seed) % i
            if next_random(seed) % 2 == 0:
                if nodes[p][1] == -1:
                    nodes[p][1] = i
                    break
            elif nodes[p][2] == -1:
                nodes[p][2] = i
                break
        nodes.append([values[i], -1, -1])
    return nodes


def main():
    show([1, 3, 2], 1)
    show([1], 1)
    show([1, 2, 3, 4, NULL, NULL, NULL, 5, NULL, 6], 2)
    show([1, 2, 3, 4, 5, 6, 7], 1)
    show([1, 2, 3, 4, 5, 6, 7], 6)
    show([5, 4, 9, 3, NULL, NULL, 8, 2, NULL, NULL, 7, 1, NULL, NULL, 6], 4)
    show([5, 4, 9, 3, NULL, NULL, 8, 2, NULL, NULL, 7, 1, NULL, NULL, 6], 5)
    show([10, 20, NULL, 30, NULL, 40, 50], 20)
    seed = [742]
    big = random_tree(seed, 1000)
    total = 0
    for k in range(1, 1001):
        total = (total * 131 + find_closest_leaf(big, k)) % 1000000007
    print(f"a random tree of 1000 nodes, every k: checksum {total}")
    path = [[i + 1, i + 1 if i < 999 else -1, -1] for i in range(1000)]
    print(f"a path of 1000 nodes, k at the top -> {find_closest_leaf(path, 1)}")
    total2 = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 15
        tree = random_tree(seed, n)
        k = 1 + next_random(seed) % n
        total2 = (total2 * 131 + find_closest_leaf(tree, k)) % 1000000007
    print(f"300 random trees of 1 to 15 nodes: checksum {total2}")


main()
