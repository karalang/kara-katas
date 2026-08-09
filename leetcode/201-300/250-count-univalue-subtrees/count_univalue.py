"""LeetCode 250 - Count Univalue Subtrees. Python oracle.

Mirrors count_univalue.kara algorithm-for-algorithm: the same index-pool tree
built by the same level-order walk, the same post-order recursion, and the same
deliberate non-short-circuit (both children answered before combining).
"""
import sys

NULL = -1000


def build(vals, null_val):
    """(val, left, right) triples; root is 0. Children always get a HIGHER
    index than their parent -- the pool is filled in BFS order."""
    nodes = []
    n = len(vals)
    if n == 0 or vals[0] == null_val:
        return nodes
    nodes.append([vals[0], -1, -1])
    queue = [0]
    head = 0
    i = 1
    while head < len(queue) and i < n:
        cur = queue[head]
        head += 1
        if i < n and vals[i] != null_val:
            nodes.append([vals[i], -1, -1])
            li = len(nodes) - 1
            nodes[cur][1] = li
            queue.append(li)
        i += 1
        if i < n and vals[i] != null_val:
            nodes.append([vals[i], -1, -1])
            ri = len(nodes) - 1
            nodes[cur][2] = ri
            queue.append(ri)
        i += 1
    return nodes


def count_univalue(vals, null_val=NULL):
    nodes = build(vals, null_val)
    if not nodes:
        return 0
    total = 0

    # Explicit stack rather than recursion so deep chains cannot blow Python's
    # limit; the visit ORDER is identical to the .kara recursion.
    def walk(root):
        nonlocal total
        uni = [False] * len(nodes)
        stack = [(root, False)]
        while stack:
            node, expanded = stack.pop()
            if node == -1:
                continue
            if not expanded:
                stack.append((node, True))
                stack.append((nodes[node][2], False))
                stack.append((nodes[node][1], False))
                continue
            left, right = nodes[node][1], nodes[node][2]
            left_uni = True if left == -1 else uni[left]
            right_uni = True if right == -1 else uni[right]
            ok = left_uni and right_uni
            if left != -1 and nodes[left][0] != nodes[node][0]:
                ok = False
            if right != -1 and nodes[right][0] != nodes[node][0]:
                ok = False
            uni[node] = ok
            if ok:
                total += 1

    walk(0)
    return total


def main():
    cases = [
        [5, 1, 5, 5, 5, NULL, 5],
        [],
        [1],
        [1, 1, 1],
        [1, 1, 2],
        [5, 5, 5, 5, 5, NULL, 5],
        [1, 2, 3, 4, 5, 6, 7],
        [7, 7, 7, 7, 7, 7, 7],
    ]
    for c in cases:
        print(count_univalue(c))


if __name__ == "__main__":
    main()
