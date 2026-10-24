# Benchmark: LeetCode #958 Check Completeness of a Binary Tree -- the ★
# arm, the first gap, on trees of 100 nodes, LeetCode's largest. Mirrors
# is_complete_tree.kara, .c, .rs and go-seq/.

from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_complete_tree(root):
    queue = deque([root])
    gap = False
    while queue:
        node = queue.popleft()
        if node is None:
            gap = True
        else:
            if gap:
                return False
            queue.append(node.left)
            queue.append(node.right)
    return True


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def new_node():
    return TreeNode(1 + next_random() % 1000)


def side_of(i):
    return (i + 1) % 2


def set_child(parent, side, child):
    if side == 0:
        parent.left = child
    else:
        parent.right = child


def complete_tree(n):
    if n == 0:
        return None
    nodes = [new_node() for _ in range(n)]
    for i in range(1, n):
        set_child(nodes[(i - 1) // 2], side_of(i), nodes[i])
    return nodes[0]


def attach(root, node):
    cur = root
    while True:
        if next_random() % 2 == 0:
            if cur.left is not None:
                cur = cur.left
            else:
                cur.left = node
                return
        else:
            if cur.right is not None:
                cur = cur.right
            else:
                cur.right = node
                return


def random_tree(n):
    if n == 0:
        return None
    root = new_node()
    for _ in range(1, n):
        attach(root, new_node())
    return root


def in_order(root):
    out = [root]
    i = 0
    while i < len(out):
        node = out[i]
        if node.left is not None:
            out.append(node.left)
        if node.right is not None:
            out.append(node.right)
        i += 1
    return out


def make_tree(kind, n):
    if kind == 3:
        return random_tree(n)
    t = complete_tree(n)
    if n < 2:
        return t
    nodes = in_order(t)
    if kind == 1:
        last = nodes[n - 1]
        set_child(nodes[(n - 2) // 2], side_of(n - 1), None)
        parents = []
        sides = []
        for i in range(n - 1):
            if nodes[i].left is None:
                parents.append(nodes[i])
                sides.append(0)
            if nodes[i].right is None:
                parents.append(nodes[i])
                sides.append(1)
        k = next_random() % len(parents)
        set_child(parents[k], sides[k], last)
    elif kind == 2:
        leaves = [i for i in range(1, n) if nodes[i].left is None and nodes[i].right is None]
        i = leaves[next_random() % len(leaves)]
        set_child(nodes[(i - 1) // 2], side_of(i), None)
    elif kind == 4:
        node = nodes[next_random() % n]
        node.left, node.right = node.right, node.left
    return t


def main():
    global seed
    rounds = 4000
    seed = 958
    trees = [make_tree(i % 5, 100) for i in range(200)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(200):
            bit = 1 if is_complete_tree(trees[(r + i) % 200]) else 0
            total += bit
            check = (check * 31 + bit + 1 + i) % 1000000007
    print(f"{rounds} rounds over 200 trees of up to 100 nodes: {total} complete, checksum {check}")


main()
