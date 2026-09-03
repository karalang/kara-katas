"""LeetCode 310 - Minimum Height Trees.

Mirror of minimum_height_trees.kara: peel leaves layer by layer until one or
two nodes remain. Each round shortens the longest path by exactly two — one
from each end — so the process converges on the middle of the diameter, which
is the tree's centre.
"""


def min_height_roots(n: int, adj: list[list[int]]) -> list[int]:
    if n <= 2:
        return list(range(n))

    degree = [len(adj[i]) for i in range(n)]
    alive = [1] * n
    # The current layer of leaves, snapshotted before any removal.
    layer = [i for i in range(n) if degree[i] == 1]

    remaining = n
    while remaining > 2:
        remaining -= len(layer)
        nxt = []
        for v in layer:
            alive[v] = 0
            for w in adj[v]:
                if alive[w] == 1:
                    degree[w] -= 1
                    # A neighbour that just became a leaf belongs to the NEXT
                    # layer, never this one.
                    if degree[w] == 1:
                        nxt.append(w)
        layer = nxt

    return [i for i in range(n) if alive[i] == 1]


def adjacency(n: int, edges: list[int]) -> list[list[int]]:
    adj = [[] for _ in range(n)]
    for k in range(0, len(edges) - 1, 2):
        a, b = edges[k], edges[k + 1]
        adj[a].append(b)
        adj[b].append(a)
    return adj


def report(n: int, edges: list[int]) -> None:
    roots = min_height_roots(n, adjacency(n, edges))
    body = ", ".join(str(v) for v in roots)
    print(f"n={n} -> [{body}]")


def main() -> None:
    # The examples from the LeetCode statement.
    report(4, [1, 0, 1, 2, 1, 3])
    report(6, [3, 0, 3, 1, 3, 2, 3, 4, 5, 4])
    # A single node: it is its own centre.
    report(1, [])
    # Two nodes: both are centres.
    report(2, [0, 1])
    # A path of odd length has ONE centre.
    report(5, [0, 1, 1, 2, 2, 3, 3, 4])
    # A path of even length has TWO.
    report(4, [0, 1, 1, 2, 2, 3])
    # A star: the hub is the only centre.
    report(7, [0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6])
    # A balanced binary tree of 7 nodes.
    report(7, [0, 1, 0, 2, 1, 3, 1, 4, 2, 5, 2, 6])
    # A caterpillar — a spine with legs, where peeling takes several rounds.
    report(9, [0, 1, 1, 2, 2, 3, 3, 4, 1, 5, 2, 6, 3, 7, 0, 8])
    # Labels deliberately scrambled: the answer is about structure, not names.
    report(5, [4, 2, 2, 0, 0, 3, 3, 1])


if __name__ == "__main__":
    main()
