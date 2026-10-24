# LeetCode #987: Vertical Order Traversal of a Binary Tree -- mirror of
# the ★ arm (vertical_traversal.kara), every node's place sorted.
import sys
from collections import deque

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def walk(t, row, col, out):
    if t is not None:
        out.append((col, row, t.val))
        walk(t.left, row + 1, col - 1, out)
        walk(t.right, row + 1, col + 1, out)


def vertical_traversal(root):
    places = []
    walk(root, 0, 0, places)
    places.sort()
    out = []
    last = 0
    for col, _, val in places:
        if not out or col != last:
            out.append([])
            last = col
        out[-1].append(val)
    return out


seed = 987


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while i < len(vals):
        node = queue.popleft()
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals):
            if vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1
    return root


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


def random_tree(n, values):
    root = TreeNode(next_random() % values)
    for _ in range(1, n):
        attach(root, TreeNode(next_random() % values))
    return root


def complete_tree(n):
    nodes = [TreeNode(i) for i in range(n)]
    for i in range(1, n):
        if i % 2 == 1:
            nodes[(i - 1) // 2].left = nodes[i]
        else:
            nodes[(i - 1) // 2].right = nodes[i]
    return nodes[0]


def left_path(n):
    t = TreeNode(0)
    for i in range(1, n):
        t = TreeNode(i % 1001, t, None)
    return t


def fold(check, cols):
    for col in cols:
        check = (check * 31 + len(col)) % 1000000007
        for v in col:
            check = (check * 31 + v) % 1000000007
    return check


def level_order_text(vals):
    return "[" + ", ".join("null" if v is None else str(v) for v in vals) + "]"


def cols_text(cols):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in col) + "]" for col in cols) + "]"


def summary(cols):
    nodes = sum(len(c) for c in cols)
    widest = max(len(c) for c in cols)
    return f"{nodes} nodes in {len(cols)} columns, the widest {widest}, checksum {fold(0, cols)}"


def main():
    N = None
    cases = [
        [3, 9, 20, N, N, 15, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 6, 5, 7],
        [0],
        [5, 4, N, 3, N, 2],
        [1, N, 2, N, 3],
        [1, 2, N, N, 3, 4],
        [1, 2, 3, N, 9, 8],
        [7, 7, 7, 7, 7, 7, 7],
        [3, 1, 4, 0, 2, 2],
    ]
    for c in cases:
        print(f"{level_order_text(c)} -> {cols_text(vertical_traversal(from_level_order(c)))}")
    print(f"the complete tree of 1000 nodes: {summary(vertical_traversal(complete_tree(1000)))}")
    print(f"a path of 1000 nodes to the left: {summary(vertical_traversal(left_path(1000)))}")
    for count, most, values in [(300, 8, 10), (3000, 100, 1001), (3, 1000, 1001)]:
        nodes = 0
        columns = 0
        check = 0
        for _ in range(count):
            n = most if count == 3 else 1 + next_random() % most
            cols = vertical_traversal(random_tree(n, values))
            nodes += n
            columns += len(cols)
            check = fold(check, cols)
        print(f"{count} random trees of {nodes} nodes, values below {values}: {columns} columns, checksum {check}")


main()
