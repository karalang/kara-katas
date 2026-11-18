# LeetCode #2277: Closest Node to Path in Tree -- the Python mirror of
# the ★ arm, `closest.kara`, line for line. Its output is byte-identical.


def distances(n, adj, start):
    dist = [-1] * n
    dist[start] = 0
    queue = [start]
    head = 0
    while head < len(queue):
        v = queue[head]
        head += 1
        for w in adj[v]:
            if dist[w] < 0:
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist


def closest_node(n, edges, query):
    adj = [[] for _ in range(n)]
    for e in edges:
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    dist = [distances(n, adj, v) for v in range(n)]
    answer = []
    for start, end, node in query:
        best = start
        for u in range(n):
            if dist[start][u] + dist[u][end] == dist[start][end] and dist[u][node] < dist[best][node]:
                best = u
        answer.append(best)
    return answer


seed = 2277


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def tree(n, reach):
    label = list(range(n))
    for j in range(n - 1, 0, -1):
        r = next_random() % (j + 1)
        label[j], label[r] = label[r], label[j]
    edges = []
    for i in range(1, n):
        parent = i - 1 - next_random() % min(reach, i)
        if next_random() % 2 == 0:
            edges.append([label[i], label[parent]])
        else:
            edges.append([label[parent], label[i]])
    for j in range(len(edges) - 1, 0, -1):
        r = next_random() % (j + 1)
        edges[j], edges[r] = edges[r], edges[j]
    return edges


def queries(n, m):
    out = []
    for _ in range(m):
        a = next_random() % n
        b = next_random() % n
        c = next_random() % n
        out.append([a, b, c])
    return out


def main():
    examples = [
        (7, [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [2, 6]], [[5, 3, 4], [5, 3, 6]]),
        (3, [[0, 1], [1, 2]], [[0, 1, 2]]),
        (3, [[0, 1], [1, 2]], [[0, 0, 0]]),
        (1, [], [[0, 0, 0]]),
        (5, [[0, 1], [1, 2], [2, 3], [3, 4]], [[0, 4, 2], [4, 0, 2], [1, 3, 0]]),
        (5, [[0, 1], [0, 2], [0, 3], [0, 4]], [[1, 2, 3], [3, 3, 4]]),
    ]
    for n, edges, query in examples:
        print(f"{n} {edges} {query} -> {closest_node(n, edges, query)}")
    check = 0
    for t in range(500):
        n = next_random() % 30 + 1
        edges = tree(n, [1, 3, 1000][t % 3])
        m = next_random() % 10 + 1
        query = queries(n, m)
        for a in closest_node(n, edges, query):
            check = (check * 31 + a) % 1000000007
    print(f"500 trees: checksum {check}")
    sums = []
    for reach in [1000, 1]:
        edges = tree(1000, reach)
        query = queries(1000, 1000)
        sums.append(sum(closest_node(1000, edges, query)))
    print(f"1000 nodes: {sums}")


main()
