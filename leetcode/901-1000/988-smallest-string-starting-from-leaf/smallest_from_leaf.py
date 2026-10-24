# LeetCode #988: Smallest String Starting From Leaf -- mirror of the ★
# arm (smallest_from_leaf.kara), a walk carrying the path.
import sys
from collections import deque

sys.setrecursionlimit(20000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def walk(t, path, best):
    path.append(chr(ord("a") + t.val))
    if t.left is None and t.right is None:
        s = "".join(reversed(path))
        if best[0] is None or s < best[0]:
            best[0] = s
    else:
        if t.left is not None:
            walk(t.left, path, best)
        if t.right is not None:
            walk(t.right, path, best)
    path.pop()


def smallest_from_leaf(root):
    best = [None]
    walk(root, [], best)
    return best[0]


seed = 988


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
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


def random_tree(n, letters):
    root = TreeNode(next_random() % letters)
    for _ in range(1, n):
        attach(root, TreeNode(next_random() % letters))
    return root


def complete_tree(n):
    nodes = [TreeNode((i * 7) % 26) for i in range(n)]
    for i in range(1, n):
        if i % 2 == 1:
            nodes[(i - 1) // 2].left = nodes[i]
        else:
            nodes[(i - 1) // 2].right = nodes[i]
    return nodes[0]


def path(n):
    t = TreeNode(0)
    for i in range(1, n):
        t = TreeNode(i % 26, None, t) if i % 2 == 0 else TreeNode(i % 26, t, None)
    return t


def level_order_text(vals):
    return "[" + ", ".join("null" if v is None else str(v) for v in vals) + "]"


def shown(s):
    if len(s) > 20:
        return f"{len(s)} letters, starting {s[:12]}"
    return f'"{s}"'


def main():
    N = None
    cases = [
        [0, 1, 2, 3, 4, 3, 4],
        [25, 1, 3, 1, 3, 0, 2],
        [2, 2, 1, N, 1, 0, N, 0],
        [7],
        [25, 1, 0, N, N, 1],
        [0, 0, 0, 0, N, N, N, 0],
        [3, 1, 1, N, N, 2, 0, N, N, 0, 1],
        [1, 0, 0, 0, N, 0],
        [25, 24, 23, 22],
        [0, 1, 1, 1, N, N, 1, 1],
    ]
    for c in cases:
        print(f"{level_order_text(c)} -> {shown(smallest_from_leaf(from_level_order(c)))}")
    print(f"the complete tree of 8500 nodes: {shown(smallest_from_leaf(complete_tree(8500)))}")
    print(f"a zigzag path of 8500 nodes: {shown(smallest_from_leaf(path(8500)))}")
    for count, most, letters in [(300, 10, 3), (3000, 100, 26), (300, 300, 2), (3, 8500, 26)]:
        nodes = 0
        total = 0
        check = 0
        for _ in range(count):
            n = most if count == 3 else 1 + next_random() % most
            s = smallest_from_leaf(random_tree(n, letters))
            nodes += n
            total += len(s)
            for ch in s:
                check = (check * 31 + ord(ch)) % 1000000007
        print(f"{count} random trees of {nodes} nodes, letters below {letters}: {total} letters, checksum {check}")


main()
