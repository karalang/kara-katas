# LeetCode #1516 bench: the ★ arm (parent walks and a splice), as move.kara.
import sys

sys.setrecursionlimit(100000)


class Node:
    __slots__ = ("val", "children")

    def __init__(self, val):
        self.val = val
        self.children = []


def parent_of(node, val):
    for child in node.children:
        if child.val == val:
            return node
        found = parent_of(child, val)
        if found is not None:
            return found
    return None


def contains(node, val):
    if node.val == val:
        return True
    for child in node.children:
        if contains(child, val):
            return True
    return False


def move_sub_tree(root, p, q):
    for child in q.children:
        if child.val == p.val:
            return root
    p_parent = parent_of(root, p.val)
    if contains(p, q.val):
        q_parent = parent_of(root, q.val)
        q_parent.children = [c for c in q_parent.children if c.val != q.val]
        q.children.append(p)
        if p_parent is None:
            return q
        i = next(k for k, c in enumerate(p_parent.children) if c.val == p.val)
        p_parent.children[i] = q
    else:
        p_parent.children = [c for c in p_parent.children if c.val != p.val]
        q.children.append(p)
    return root


seed = 1516


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def fold(node, check):
    check = mix(check, node.val)
    for child in node.children:
        check = fold(child, check)
    return check


def main():
    n = 100000
    nodes = [Node(v) for v in range(n)]
    for i in range(1, n):
        parent = (next_random() * 32768 + next_random()) % i
        nodes[parent].children.append(nodes[i])
    root = nodes[0]
    check = 0
    for _ in range(1000):
        p = (next_random() * 32768 + next_random()) % n
        q = (p + 1 + (next_random() * 32768 + next_random()) % (n - 1)) % n
        root = move_sub_tree(root, nodes[p], nodes[q])
        check = mix(check, root.val)
    check = fold(root, check)
    print(f"1000 moves in a tree of 100000 nodes: checksum {check}")


main()
