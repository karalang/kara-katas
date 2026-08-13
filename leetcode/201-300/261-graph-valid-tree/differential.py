"""LeetCode 261 — differential harness (Python mirror / oracle).

Mirrors differential.kara draw-for-draw: the same LCG, the same order of seed
advances, the same five generator families and the same shuffle, so the printed
digest must match byte for byte.
"""

MASK = 2147483647
DIGEST_MOD = 1000000007


def find(parent, x):
    r = x
    while parent[r] != r:
        r = parent[r]
    c = x
    while parent[c] != r:
        parent[c], c = r, parent[c]
    return r


def valid_union(n, edges):
    parent = list(range(n))
    size = [1] * n
    components = n
    for u, v in edges:
        ra, rb = find(parent, u), find(parent, v)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            parent[ra] = rb
            size[rb] += size[ra]
        else:
            parent[rb] = ra
            size[ra] += size[rb]
        components -= 1
    return components == 1


def valid_bfs(n, edges):
    if len(edges) != n - 1:
        return False
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    queue = [0]
    seen[0] = True
    reached = 1
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        for nb in adj[node]:
            if not seen[nb]:
                seen[nb] = True
                reached += 1
                queue.append(nb)
    return reached == n


def valid_peel(n, edges):
    adj = [[] for _ in range(n)]
    deg = [0] * n
    gone = [False] * n
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
    queue = [s for s in range(n) if deg[s] == 1]
    removed = 0
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if gone[node] or deg[node] != 1:
            continue
        gone[node] = True
        removed += 1
        deg[node] = 0
        for nb in adj[node]:
            if not gone[nb]:
                deg[nb] -= 1
                if deg[nb] == 1:
                    queue.append(nb)
    return n - removed == 1


def main():
    cases = 4000
    seed = 261261

    mismatches = 0
    trues = 0
    exact_count_not_tree = 0
    total_edges = 0
    digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & MASK
        n = (seed // 65536) % 12 + 1
        seed = (seed * 1103515245 + 12345) & MASK
        family = (seed // 65536) % 5

        mat = [[False] * n for _ in range(n)]
        edges = []

        if family <= 3:
            for i in range(1, n):
                seed = (seed * 1103515245 + 12345) & MASK
                p = (seed // 65536) % i
                edges.append([p, i])
                mat[p][i] = True
                mat[i][p] = True

        if family == 1:
            tries = 0
            while tries < 40:
                seed = (seed * 1103515245 + 12345) & MASK
                u = (seed // 65536) % n
                seed = (seed * 1103515245 + 12345) & MASK
                v = (seed // 65536) % n
                if u != v and not mat[u][v]:
                    edges.append([u, v])
                    mat[u][v] = True
                    mat[v][u] = True
                    tries = 40
                else:
                    tries += 1

        if family == 2 and len(edges) > 0:
            seed = (seed * 1103515245 + 12345) & MASK
            drop = (seed // 65536) % len(edges)
            edges = [e for k, e in enumerate(edges) if k != drop]

        if family == 3 and len(edges) > 0:
            seed = (seed * 1103515245 + 12345) & MASK
            drop = (seed // 65536) % len(edges)
            kept = []
            for k, e in enumerate(edges):
                if k != drop:
                    kept.append(e)
                else:
                    mat[e[0]][e[1]] = False
                    mat[e[1]][e[0]] = False
            edges = kept
            tries = 0
            while tries < 40:
                seed = (seed * 1103515245 + 12345) & MASK
                u = (seed // 65536) % n
                seed = (seed * 1103515245 + 12345) & MASK
                v = (seed // 65536) % n
                if u != v and not mat[u][v]:
                    edges.append([u, v])
                    mat[u][v] = True
                    mat[v][u] = True
                    tries = 40
                else:
                    tries += 1

        if family == 4:
            seed = (seed * 1103515245 + 12345) & MASK
            want = n - 1 + (seed // 65536) % 3 - 1
            placed = 0
            tries = 0
            while placed < want and tries < 200:
                seed = (seed * 1103515245 + 12345) & MASK
                u = (seed // 65536) % n
                seed = (seed * 1103515245 + 12345) & MASK
                v = (seed // 65536) % n
                if u != v and not mat[u][v]:
                    edges.append([u, v])
                    mat[u][v] = True
                    mat[v][u] = True
                    placed += 1
                tries += 1

        m = len(edges)
        sh = m - 1
        while sh > 0:
            seed = (seed * 1103515245 + 12345) & MASK
            j = (seed // 65536) % (sh + 1)
            edges[sh], edges[j] = edges[j], edges[sh]
            sh -= 1

        a = valid_union(n, edges)
        b = valid_bfs(n, edges)
        d = valid_peel(n, edges)

        if a != b or a != d:
            mismatches += 1
        if a:
            trues += 1
        if m == n - 1 and not a:
            exact_count_not_tree += 1
        total_edges += m

        digest = (digest * 131 + (1 if a else 0) * 7 + n) % DIGEST_MOD

    print(f"cases {cases}")
    print(f"valid trees {trues}")
    print(f"|E|=n-1 but not a tree {exact_count_not_tree}")
    print(f"edges generated {total_edges}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
