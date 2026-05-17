"""LeetCode #133: Clone Graph — BFS / iterative O(N + M).

Same idea as the DFS variant but uses an explicit queue. Clone the root up
front and seed the visited map with it; for every node we pop, walk its
neighbors, clone any unseen ones (queuing them for later expansion), and
append the existing-or-fresh clone to the current node's clone's neighbor
list.

Algorithmic mirror of bfs.kara. Output format matches line-for-line so the
two can be diffed directly.
"""

from __future__ import annotations

from collections import deque


class Node:
    def __init__(self, val: int, neighbors: list["Node"] | None = None) -> None:
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(root: Node | None) -> Node | None:
    if root is None:
        return None
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


# ---- test harness ----------------------------------------------------------

def build_graph(adj: list[list[int]]) -> Node | None:
    if not adj:
        return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, neighbors in enumerate(adj):
        for v in neighbors:
            nodes[i].neighbors.append(nodes[v - 1])
    return nodes[0]


def print_graph(root: Node | None) -> None:
    if root is None:
        print("(empty)")
        return
    queue = deque([root])
    visited = {root.val}
    while queue:
        curr = queue.popleft()
        nvals: list[int] = []
        for nb in curr.neighbors:
            nvals.append(nb.val)
            if nb.val not in visited:
                visited.add(nb.val)
                queue.append(nb)
        print(f"{curr.val}: {nvals}")


def report(adj: list[list[int]]) -> None:
    original = build_graph(adj)
    cloned = clone_graph(original)
    print_graph(cloned)
    print("---")


def main() -> None:
    report([[2, 4], [1, 3], [2, 4], [1, 3]])       # 4-cycle
    report([[]])                                    # single node, no edges
    report([])                                      # empty graph
    report([[2], [1]])                              # 2 nodes, mutual
    report([[2], [1, 3], [2, 4], [3]])              # path 1-2-3-4


if __name__ == "__main__":
    main()
