"""LeetCode 199 — Binary Tree Right Side View (Python mirror / oracle).

BFS by level over an index-pool tree (list of nodes, i64 child indices, -1 = null)
built from a level-order array with a NULL sentinel; the rightmost node per level
is visible. Mirrors the Kāra version.
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = -1
        self.right = -1


def build(vals, null_val):
    nodes = []
    if not vals or vals[0] == null_val:
        return nodes
    nodes.append(Node(vals[0]))
    queue = [0]
    head = 0
    i = 1
    n = len(vals)
    while head < len(queue) and i < n:
        cur = queue[head]
        head += 1
        if i < n and vals[i] != null_val:
            nodes.append(Node(vals[i]))
            li = len(nodes) - 1
            nodes[cur].left = li
            queue.append(li)
        i += 1
        if i < n and vals[i] != null_val:
            nodes.append(Node(vals[i]))
            ri = len(nodes) - 1
            nodes[cur].right = ri
            queue.append(ri)
        i += 1
    return nodes


def right_view(nodes, root):
    result = []
    if root == -1:
        return result
    level = [root]
    while level:
        result.append(nodes[level[-1]].val)
        nxt = []
        for idx in level:
            if nodes[idx].left != -1:
                nxt.append(nodes[idx].left)
            if nodes[idx].right != -1:
                nxt.append(nodes[idx].right)
        level = nxt
    return result


def report(vals, null_val):
    nodes = build(vals, null_val)
    root = 0 if nodes else -1
    print(" ".join(str(v) for v in right_view(nodes, root)))


def main():
    null = -1000
    report([1, 2, 3, -1000, 5, -1000, 4], null)
    report([1, -1000, 3], null)
    report([], null)
    report([1, 2, 3, 4], null)
    report([1, 2], null)


main()
