# LeetCode #1059: All Paths from Source Lead to Destination -- mirror of
# paths.kara: an iterative depth-first search with three colours.

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


# ---- test harness ---------------------------------------------------------

seed = 1059


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_graph(n, most_edges):
    m = next_random() % (most_edges + 1)
    edges = []
    for _ in range(m):
        u = next_random() % n
        v = next_random() % n
        edges.append((u, v))
    return edges


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


def mix(check, answer, k):
    return (check * 31 + (7 + k % 13 if answer else 3)) % 1000000007


def show_edges(edges):
    return "[" + ", ".join(f"({u}, {v})" for u, v in edges) + "]"


def show(b):
    return "true" if b else "false"


def main():
    examples = [
        (3, [(0, 1), (0, 2)], 0, 2),
        (4, [(0, 1), (0, 3), (1, 2), (2, 1)], 0, 3),
        (4, [(0, 1), (0, 2), (1, 3), (2, 3)], 0, 3),
        (1, [], 0, 0),
        (1, [(0, 0)], 0, 0),
        (2, [(0, 1), (1, 1)], 0, 1),
        (3, [(0, 1), (0, 1), (1, 2), (1, 2)], 0, 2),
        (2, [], 0, 1),
        (3, [(1, 2), (2, 1)], 0, 0),
        (5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 2)], 0, 4),
    ]
    for n, edges, source, destination in examples:
        print(f"{n} {show_edges(edges)} {source} {destination} -> {show(leads_to_destination(n, edges, source, destination))}")
    yes = check = 0
    for k in range(3000):
        n = next_random() % 8 + 1
        edges = random_graph(n, 12)
        source = next_random() % n
        destination = next_random() % n
        answer = leads_to_destination(n, edges, source, destination)
        yes += answer
        check = mix(check, answer, k)
    print(f"3000 random graphs of 1 to 8 nodes: {yes} lead, checksum {check}")
    yes = check = 0
    for k in range(3000):
        n = next_random() % 12 + 1
        edges = leaning_graph(n, 2, 8)
        source = next_random() % n
        answer = leads_to_destination(n, edges, source, n - 1)
        yes += answer
        check = mix(check, answer, k)
    print(f"3000 leaning graphs of 1 to 12 nodes: {yes} lead, checksum {check}")
    yes = check = edge_count = 0
    for k in range(100):
        n = 10000
        edges = leaning_graph(n, 1 + k % 2, 20000 + k * 100)
        edge_count += len(edges)
        answer = leads_to_destination(n, edges, 0, n - 1)
        yes += answer
        check = mix(check, answer, k)
    print(f"100 leaning graphs of 10000 nodes, {edge_count} edges: {yes} lead, checksum {check}")
    n = 2000
    edges = leaning_graph(n, 2, 1000)
    yes = check = 0
    for source in range(n):
        answer = leads_to_destination(n, edges, source, n - 1)
        yes += answer
        check = mix(check, answer, source)
    print(f"2000 nodes, {len(edges)} edges, every source: {yes} lead, checksum {check}")
    path = [(u, u + 1) for u in range(9999)]
    opened = leads_to_destination(10000, path, 0, 9999)
    path.append((9999, 0))
    closed = leads_to_destination(10000, path, 0, 9999)
    print(f"a path of 10000 nodes: {show(opened)}, closed into a cycle: {show(closed)}")


main()
