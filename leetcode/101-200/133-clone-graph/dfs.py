"""LeetCode #133: Clone Graph — DFS / recursive O(N + M).

Each visited original node maps to its clone via a dict[int, Node], keyed by
val (LeetCode guarantees vals are unique 1..n). The map breaks recursion on
cycles: the second visit to a node returns the existing clone instead of
recursing.

Algorithmic mirror of dfs.kara. Output format matches line-for-line so the
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
    visited: dict[int, Node] = {}
    return dfs(root, visited)


def dfs(node: Node, visited: dict[int, Node]) -> Node:
    if node.val in visited:
        return visited[node.val]
    copy = Node(node.val)
    visited[node.val] = copy
    for nb in node.neighbors:
        copy.neighbors.append(dfs(nb, visited))
    return copy


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
