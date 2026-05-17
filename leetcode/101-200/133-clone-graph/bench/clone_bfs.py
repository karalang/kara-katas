"""Benchmark workload — BFS clone of a 10-regular ring of N=2000 nodes.

Algorithmic mirror of bench/clone_bfs.kara and bench/clone_bfs.rs. See
../README.md § Benchmarks for the choice of N / K and the ring-graph
generator.
"""

from __future__ import annotations

from collections import deque


class Node:
    __slots__ = ("val", "neighbors")

    def __init__(self, val: int) -> None:
        self.val = val
        self.neighbors: list[Node] = []


def clone_graph(root: Node) -> Node:
    visited: dict[int, Node] = {root.val: Node(root.val)}
    queue: deque[Node] = deque([root])
    while queue:
        curr = queue.popleft()
        curr_clone = visited[curr.val]
        for nb in curr.neighbors:
            if nb.val not in visited:
                visited[nb.val] = Node(nb.val)
                queue.append(nb)
            curr_clone.neighbors.append(visited[nb.val])
    return visited[root.val]


def main() -> None:
    N = 2000
    HALF_DEG = 5
    K = 500

    nodes = [Node(i + 1) for i in range(N)]
    for i in range(N):
        for d in range(1, HALF_DEG + 1):
            j = (i + d) % N
            nodes[i].neighbors.append(nodes[j])
            nodes[j].neighbors.append(nodes[i])

    s = 0
    for _ in range(K):
        c = clone_graph(nodes[0])
        s += c.val
    print(s)


if __name__ == "__main__":
    main()
