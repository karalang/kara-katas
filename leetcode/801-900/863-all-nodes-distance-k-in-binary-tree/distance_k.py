# LeetCode #863: All Nodes Distance K in Binary Tree -- Python mirror of the
# ★ arm (parents, then a breadth-first search).
from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def distance_k(root, target, k):
    parent = {}
    start = None
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        if node.val == target:
            start = node
        for child in (node.left, node.right):
            if child:
                parent[child.val] = node
                stack.append(child)
    if start is None:
        return []
    seen = {start.val}
    level = [start]
    for _ in range(k):
        nxt = []
        for node in level:
            near = [c for c in (node.left, node.right) if c]
            if node.val in parent:
                near.append(parent[node.val])
            for m in near:
                if m.val not in seen:
                    seen.add(m.val)
                    nxt.append(m)
        level = nxt
    return sorted(node.val for node in level)


seed = 863


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


def show(vals, target, k):
    root = from_level_order(vals)
    print(f"root = {to_level_order(root)}, target = {target}, k = {k} -> {distance_k(root, target, k)}")


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


def fold(check, found):
    for v in found:
        check = (check * 31 + v + 1) % 1000000007
    return (check * 31 + 1000) % 1000000007


def main():
    example = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
    show(example, 5, 2)
    show([1], 1, 3)
    show(example, 5, 0)
    show(example, 3, 1)
    show(example, 7, 3)
    show(example, 8, 4)
    show(example, 0, 5)
    show(example, 4, 1000)
    show([0, 1, None, 2, None, 3], 2, 2)
    show([0, None, 1, None, 2, None, 3, None, 4], 0, 4)
    big = random_tree(500)
    for k in [1, 3, 10, 1000]:
        target = next_random() % 500
        found = distance_k(big, target, k)
        print(f"500 nodes, target = {target}, k = {k} -> {len(found)} found, checksum {fold(0, found)}")
    queries = 0
    total = 0
    check = 0
    for _ in range(200):
        n = 1 + next_random() % 40
        root = random_tree(n)
        for target in range(n):
            for k in range(6):
                found = distance_k(root, target, k)
                queries += 1
                total += len(found)
                check = fold(check, found)
    print(f"{queries} random queries: {total} nodes found, checksum {check}")


main()
