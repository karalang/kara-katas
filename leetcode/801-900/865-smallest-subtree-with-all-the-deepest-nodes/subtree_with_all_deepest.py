# LeetCode #865: Smallest Subtree with all the Deepest Nodes -- Python
# mirror of the ★ arm (one recursive pass).
from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def subtree_with_all_deepest(root):
    return deepest(root)[1]


def deepest(node):
    if node is None:
        return 0, None
    dl, left = deepest(node.left)
    dr, right = deepest(node.right)
    if dl == dr:
        return dl + 1, node
    if dl > dr:
        return dl + 1, left
    return dr + 1, right


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


def to_level_order(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append("null")
    while out and out[-1] == "null":
        out.pop()
    return "[" + ", ".join(out) + "]"


def random_tree(n):
    vals = list(range(n))
    for i in range(1, n):
        j = next_random() % (i + 1)
        vals[i], vals[j] = vals[j], vals[i]
    nodes = []
    for k in range(n):
        node = TreeNode(vals[k])
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
    return nodes[0] if n else None


def size(node):
    return 0 if node is None else 1 + size(node.left) + size(node.right)


def show(vals):
    root = from_level_order(vals)
    print(f"root = {to_level_order(root)} -> {to_level_order(subtree_with_all_deepest(root))}")


def main():
    global seed
    show([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    show([1])
    show([0, 1, 3, None, 2])
    show([1, 2, 3])
    show([1, 2, 3, 4, 5, 6, 7])
    show([0, 1, None, 2, None, 3])
    show([0, None, 1, None, 2, None, 3])
    show([1, 2, 3, 4, None, None, 5])
    show([1, 2, 3, 4, 5, None, 6, 7, None, None, 8])
    show([1, 2, 3, None, 4, 5, None, None, None, 6, 7])
    seed = 865
    for _ in range(4):
        found = subtree_with_all_deepest(random_tree(500))
        val = found.val if found else -1
        print(f"500 nodes -> subtree at {val} with {size(found)} nodes")
    total = check = 0
    for _ in range(1000):
        n = 1 + next_random() % 60
        found = subtree_with_all_deepest(random_tree(n))
        total += size(found)
        for c in to_level_order(found).encode():
            check = (check * 31 + c) % 1000000007
    print(f"1000 random trees: subtrees of {total} nodes in all, checksum {check}")


main()
