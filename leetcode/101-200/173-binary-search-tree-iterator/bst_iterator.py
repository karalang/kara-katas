"""LeetCode 173 — Binary Search Tree Iterator (Python mirror / oracle).

In-order iteration driven by an explicit stack of the not-yet-visited left spine:
has_next is stack-non-empty, next pops the smallest then pushes its right child's
left spine. Index-pool tree (list of nodes, i64 child indices, -1 = null) to
mirror the Kāra version exactly.
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = -1
        self.right = -1


def insert(nodes, root, val):
    if root == -1:
        nodes.append(Node(val))
        return len(nodes) - 1
    if val < nodes[root].val:
        nodes[root].left = insert(nodes, nodes[root].left, val)
    else:
        nodes[root].right = insert(nodes, nodes[root].right, val)
    return root


def push_left(stack, nodes, start):
    idx = start
    while idx != -1:
        stack.append(idx)
        idx = nodes[idx].left


def build(values):
    nodes = []
    root = -1
    for v in values:
        root = insert(nodes, root, v)
    return nodes


def drive(values):
    nodes = build(values)
    root = 0 if nodes else -1
    stack = []
    push_left(stack, nodes, root)
    out = []
    while stack:
        top = stack.pop()
        out.append(str(nodes[top].val))
        push_left(stack, nodes, nodes[top].right)
    print(" ".join(out))


def main():
    drive([5, 3, 8, 1, 4, 7, 9])
    drive([7, 3, 15, 9, 20])
    drive([42])
    drive([4, 2, 6, 1, 3, 5])


main()
