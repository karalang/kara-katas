# LeetCode #2277: Closest Node to Path in Tree -- the bench, the ★ arm.


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


# ---- bench harness ---------------------------------------------------------

seed = 2277


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(50):
        edges = [[i, next_random() % i] for i in range(1, 1000)]
        query = []
        for _ in range(1000):
            s = next_random() % 1000
            e = next_random() % 1000
            x = next_random() % 1000
            query.append([s, e, x])
        for a in closest_node(1000, edges, query):
            check = (check * 31 + a) % 1000000007
    print(f"50 trees of 1000: checksum {check}")


main()
