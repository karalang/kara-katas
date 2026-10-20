# LeetCode 814 — Binary Tree Pruning, post-order recursion (mirror of the ★ arm).
import sys
from collections import deque

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def prune_tree(root):
    if root is None:
        return None
    root.left = prune_tree(root.left)
    root.right = prune_tree(root.right)
    if root.val == 0 and root.left is None and root.right is None:
        return None
    return root


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
    if len(vals) == 0 or vals[0] is None:
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


def to_level_order(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is not None:
            out.append(f"{node.val}")
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append("null")
    while out and out[-1] == "null":
        out.pop()
    return "[" + ", ".join(out) + "]"


def show(vals):
    before = to_level_order(from_level_order(vals))
    print(f"root = {before} -> {to_level_order(prune_tree(from_level_order(vals)))}")


def random_tree(n, ones):
    nodes = []
    for k in range(n):
        v = 1 if next_random() % ones == 0 else 0
        node = TreeNode(v)
        if k > 0:
            while True:
                parent = nodes[next_random() % len(nodes)]
                if next_random() % 2 == 0:
                    if parent.left is None:
                        parent.left = node
                        break
                elif parent.right is None:
                    parent.right = node
                    break
        nodes.append(node)
    return None if n == 0 else nodes[0]


def summary(root):
    if root is None:
        return (0, 7)
    ln, lc = summary(root.left)
    rn, rc = summary(root.right)
    return (1 + ln + rn, (lc * 31 + rc * 17 + root.val + 3) % 1000000007)


def main():
    global seed
    show([1, None, 0, 0, 1])
    show([1, 0, 1, 0, 0, 0, 1])
    show([1, 1, 0, 1, 1, 0, 1, 0])
    show([0])
    show([1])
    show([0, 0, 0, None, 0, 0])
    show([0, 0, 1, 0, None, None, 0])
    show([0, None, 0, None, 0, None, 1])
    seed = 814
    n, check = summary(prune_tree(random_tree(200, 10)))
    print(f"200 nodes, one in ten a 1 -> {n} kept, checksum {check}")
    chain = TreeNode(1)
    for k in range(199):
        chain = TreeNode(0, chain if k % 2 == 0 else None, None if k % 2 == 0 else chain)
    n, check = summary(prune_tree(chain))
    print(f"a line of 200 nodes, a 1 at the bottom -> {n} kept, checksum {check}")
    kept = 0
    total = 0
    for r in range(300):
        size = 1 + next_random() % 30
        n, check = summary(prune_tree(random_tree(size, 2 + r % 6)))
        kept += n
        total = (total * 131 + check) % 1000000007
    print(f"300 random rounds of 1 to 30 nodes: {kept} kept, checksum {total}")


main()
