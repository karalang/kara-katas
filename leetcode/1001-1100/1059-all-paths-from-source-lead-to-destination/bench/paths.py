# LeetCode #1059: All Paths from Source Lead to Destination -- the
# benchmark, the same algorithm as paths.kara.

UNSEEN, ON_PATH, DONE = 0, 1, 2


def leads_to_destination(n, edges, source, destination):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    state = [UNSEEN] * n
    stack = [(source, 0)]
    state[source] = ON_PATH
    while stack:
        top = len(stack) - 1
        u, nxt = stack[top]
        if not adj[u] and u != destination:
            return False
        if nxt == len(adj[u]):
            state[u] = DONE
            stack.pop()
            continue
        stack[top] = (u, nxt + 1)
        v = adj[u][nxt]
        if state[v] == ON_PATH:
            return False
        if state[v] == UNSEEN:
            state[v] = ON_PATH
            stack.append((v, 0))
    return True


seed = 1059


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def leaning_graph(n, per_node, back):
    edges = []
    for u in range(n - 1):
        k = next_random() % (per_node + 1)
        for _ in range(k):
            span = min(n - 1 - u, 20)
            edges.append((u, u + 1 + next_random() % span))
        if k == 0 and next_random() % 4 != 0:
            edges.append((u, n - 1))
        if next_random() % back == 0:
            edges.append((u, next_random() % (u + 1)))
    return edges


def main():
    n = 2000
    graphs = [leaning_graph(n, 2, 1000) for _ in range(20)]
    calls = yes = check = 0
    for edges in graphs:
        for source in range(n):
            answer = leads_to_destination(n, edges, source, n - 1)
            if answer:
                yes += 1
            check = (check * 31 + (7 + source % 13 if answer else 3)) % 1000000007
            calls += 1
    print(f"{calls} calls: {yes} lead, checksum {check}")


main()
